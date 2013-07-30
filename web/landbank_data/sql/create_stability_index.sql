-- Creates views and table required to feed stability index to TileMill, etc.

drop view tract_stability_raw_values cascade;
drop view tract_stability_means_stddevs cascade;
drop table tract_stability cascade;
drop table tract_stability_normalized;

create view tract_stability_raw_values as
select f.fips, value.med, highcost.pct_subprime, ownveloc.owner_velocity, investveloc.investor_velocity, ownerpct.owner_pct
from landbank_data_censustract f
left join
(select fips, median(loan_amt) med
    from landbank_data_loanapplication
    where fips is not null
    and action_type=1
    and loan_purpose=1
    and property_type=1
    and year=2009
    group by fips) value on (f.fips=value.fips)
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
where value.med is not null
    and highcost.pct_subprime is not null
    and ownveloc.owner_velocity is not null
    and investveloc.investor_velocity is not null
    and ownerpct.owner_pct is not null;

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

select fips, (stability_score-ss_min)/(ss_max-ss_min) 
from tract_stability,
(select max(stability_score) ss_max, min(stability_score) ss_min from tract_stability) ssmm

select ct.fips, ct.loc
    ,((stability_score-ss_min)/(ss_max-ss_min))*100.0 norm_score 
into tract_stability_normalized
from landbank_data_censustract ct
    left join tract_stability ts
        on ts.fips=ct.fips,
    (select max(stability_score) ss_max, min(stability_score) ss_min 
    from tract_stability) ssmm
order by norm_score desc;
