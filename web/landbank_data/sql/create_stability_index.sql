drop view tract_stability_raw_values cascade;
drop view tract_stability_means_stddevs cascade;
drop table tract_stability cascade;
drop table tract_stability_normalized;
truncate table landbank_data_tractscores;
alter sequence landbank_data_tractscores_id_seq restart;

create view tract_stability_raw_values as
select f.fips
    ,case when txns.med is null then case when mort.med is null then loans.med else mort.med end else txns.med end
    ,case when highcost.pct_subprime is null then 0.0 else highcost.pct_subprime end
    ,case when ownveloc.owner_velocity is null then 0.0 else ownveloc.owner_velocity end
    ,case when investveloc.investor_velocity is null then 0.0 else investveloc.investor_velocity end
    ,case when ownerpct.owner_pct is null then 0.0 else ownerpct.owner_pct end
from landbank_data_censustract f
left join
(select fips, median(adj_amt) med
from (select fips, txn.buyer, txn.buyer_type, txn.ptype_id, txn.amount_prime::float/count(*)::float as adj_amt
        from landbank_data_pinarealookup pal, landbank_data_censustract ct, landbank_data_transaction txn
        where pal.census_tract_id=ct.id
        and txn.pin=pal.pin
        and txn.yeard=2009
        and txn.ptype_id in (1,2,3)
        group by fips, txn.buyer, txn.buyer_type, txn.ptype_id, txn.amount_prime) adj_txns
    group by fips) txns on (f.fips=txns.fips)
left join
(select ct.fips, median(mort_amt) med
    from landbank_data_pinarealookup pal, landbank_data_censustract ct, landbank_data_mortgage mort
    where pal.census_tract_id=ct.id
    and mort.pin=pal.pin
    and mort.ptype_id in (1,2,3)
    and mort.yeard=2009
    group by ct.fips) mort on (f.fips=mort.fips)
left join
(select fips, median(loan_amt) med
    from landbank_data_loanapplication loans
    where loans.fips is not null
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and year=2009
    group by loans.fips) loans on (f.fips=loans.fips)
left join
    (select fips, count(rate_spread)::float/count(*)::float as pct_subprime
    from landbank_data_loanapplication
    where fips is not null
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and year=2009
    group by fips) highcost on (f.fips=highcost.fips)
left join
    (select loans.fips
        ,sum(case when loans.owner_occ=true then 1 else 0 end)::float / census.owner_occ::float as owner_velocity
    from landbank_data_loanapplication loans, landbank_data_censustractoccupancy census
    where loans.fips is not null
    and loans.fips = census.fips
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and loans.owner_occ=true
    and year=2009
    and census.owner_occ>=100
    group by loans.fips
        ,census.owner_occ) ownveloc on (f.fips=ownveloc.fips)
left join 
    (select loans.fips
        ,sum(case when loans.owner_occ=false then 1 else 0 end)::float / census.renter_occ::float as investor_velocity
    from landbank_data_loanapplication loans, landbank_data_censustractoccupancy census
    where loans.fips is not null
    and loans.fips = census.fips
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and loans.owner_occ=false
    and year=2009
    and census.renter_occ>=100
    group by loans.fips
        ,census.renter_occ) investveloc on (f.fips=investveloc.fips)
left join
    (select fips
        ,sum(case when owner_occ=true then 1 else 0 end)::float / count(*)::float as owner_pct
    from landbank_data_loanapplication
    where fips is not null
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and year=2009
    group by fips) ownerpct on (f.fips=ownerpct.fips)

create view tract_stability_aggregates as
select
     avg(med) med_u
    ,stddev_samp(med) med_s
    ,max(med) med_max
    ,min(med) med_min
    ,avg(pct_subprime) pct_subprime_u
    ,stddev_samp(pct_subprime) pct_subprime_s
    ,max(pct_subprime) pct_subprime_max
    ,min(pct_subprime) pct_subprime_min
    ,avg(owner_velocity) owner_velocity_u
    ,stddev_samp(owner_velocity) owner_velocity_s
    ,max(owner_velocity) owner_velocity_max
    ,min(owner_velocity) owner_velocity_min
    ,avg(investor_velocity) investor_velocity_u
    ,stddev_samp(investor_velocity) investor_velocity_s
    ,max(investor_velocity) investor_velocity_max
    ,min(investor_velocity) investor_velocity_min
    ,avg(owner_pct) owner_pct_u
    ,stddev_samp(owner_pct) owner_pct_s
    ,max(owner_pct) owner_pct_max
    ,min(owner_pct) owner_pct_min
from tract_stability_raw_values;

select q.fips,
    0.6 * q.value
  - 0.4 * highcost
  + 0.3 * ownveloc
  + 0.1 * investveloc
  + 0.2 * ownerpct
    as stability_score
    ,ct.loc
into tract_stability
from
landbank_data_censustract ct
left join 
    (select fips
        ,(med-med_u)/med_s as value
        ,(pct_subprime-pct_subprime_u)/pct_subprime_s highcost
        ,(owner_velocity-owner_velocity_u)/owner_velocity_s ownveloc
        ,(investor_velocity-investor_velocity_u)/investor_velocity_s investveloc
        ,(owner_pct-owner_pct_u)/owner_pct_s ownerpct
    from tract_stability_raw_values, tract_stability_aggregates) q
on ct.fips = q.fips;

select ct.fips
    ,ct.loc
    ,((stability_score-ss_min)/(ss_max-ss_min))*100.0 norm_score 
into tract_stability_normalized
from landbank_data_censustract ct
    left join tract_stability ts
        on ts.fips=ct.fips,
    (select max(stability_score) ss_max, min(stability_score) ss_min 
    from tract_stability) ssmm
order by norm_score desc;

insert into landbank_data_tractscores (census_tract_id, stability)
(select ct.id census_tract_id, tsn.norm_score stability
from tract_stability_normalized tsn, landbank_data_censustract ct
where tsn.fips=ct.fips);
