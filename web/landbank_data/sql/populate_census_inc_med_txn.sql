-- Populates existing CensusTractIncome model with the median 2011 house transaction
update landbank_data_censustractincome cti
set med_house_txn_2011 = q.med
from
    (select fips, median(txn.amount_prime) med
    from landbank_data_pinarealookup pal, landbank_data_censustract ct, landbank_data_transaction txn
    where pal.census_tract_id=ct.id
    and txn.pin=pal.pin
    and txn.yeard=2011
    and txn.ptype_id in (1,2,3)
    group by fips) as q
where q.fips=cti.fips
