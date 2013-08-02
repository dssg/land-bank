-- Populates existing CensusTractIncome model with the median 2011 house transaction
update landbank_data_censustractincome cti 
set med_house_txn_2011 = q.med
from
    (select fips, median(adj_amt) med
    from (select fips, txn.buyer, txn.buyer_type, txn.ptype_id, txn.amount_prime::float/count(*)::float as adj_amt
        from landbank_data_pinarealookup pal, landbank_data_censustract ct, landbank_data_transaction txn
        where pal.census_tract_id=ct.id
        and txn.pin=pal.pin
        and txn.yeard=2009
        and txn.ptype_id=1
        group by fips, txn.buyer, txn.buyer_type, txn.ptype_id, txn.amount_prime) adj
    group by fips) as q
where q.fips=cti.fips
