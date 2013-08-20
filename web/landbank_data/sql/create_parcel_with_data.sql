-- Should be run before deploying
-- The /aggregate_geom.html page has ajax calls
-- that hit this table for map interaction
create table parcel_with_data as
(select
  parcel.pin14 pin,
  ass.address, ass.property_type,
  mort.mort_date, mort.mort_borrower, mort.mort_lender, mort.mort_amt,
  fc.fc_date, fc.fc_plaintiff,
  txn.txn_date, txn.txn_amt,
  vac.vac_request_date,
  scav.scav_tax_year, scav.scav_tax_amt, scav.scav_tot_amt,
  brown.brown_grant_types,
  cmap.cmap_name,
  cmap.cmap_status,
  cmap.cmap_area,
  cmap.cmap_desc,
  cmap.cmap_url,
  parcel.wkb_geometry
from
parcel left join (select
  pin,
  initcap(lda.houseno || ' ' || direction || ' ' || lda.street) as address,
    case when lda.ptype_desc is not null then initcap(lda.ptype_desc) else null end
  as property_type
FROM landbank_data_assessor lda
  where lda.houseno != '0'
  and lda.houseno != '' 
  and lda.houseno is not null
  and lda.direction != '') ass on parcel.pin14=ass.pin
left join (select distinct on (pin)
  last_value(pin) OVER wnd as pin,
  last_value(date_doc::date::text) OVER wnd as mort_date,
  last_value(initcap(borrower1)) OVER wnd as mort_borrower,
  last_value(initcap(lender1)) OVER wnd as mort_lender,
  last_value(mort_amt) OVER wnd as mort_amt
FROM landbank_data_mortgage
WINDOW wnd AS (
  PARTITION BY pin ORDER BY date_doc
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)) mort on parcel.pin14=mort.pin
left join (select distinct on (pin)
  last_value(pin) OVER wnd as pin,
  last_value(filing_date::date::text) OVER wnd as fc_date,
  last_value(initcap(plaintiff)) OVER wnd as fc_plaintiff
FROM landbank_data_foreclosure
WINDOW wnd AS (
  PARTITION BY pin ORDER BY filing_date
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)) fc on (parcel.pin14=fc.pin)
left join (select distinct on (pin)
  last_value(pin) OVER wnd as pin,
  last_value(date_doc::date::text) OVER wnd as txn_date,
  last_value(amount_prime) OVER wnd as txn_amt
FROM landbank_data_transaction txn
WINDOW wnd AS (
  PARTITION BY pin ORDER BY date_doc
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)) txn on (parcel.pin14=txn.pin)
left join (select distinct on (initcap(houseno||' '||direction||' '||street))
  last_value(initcap(houseno||' '||direction||' '||street)) OVER wnd as vac_address,
  last_value(request_date::date::text) OVER wnd as vac_request_date
FROM landbank_data_vacancy311
WINDOW wnd AS (
  PARTITION BY initcap(houseno||' '||direction||' '||street) ORDER BY request_date
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)) vac on (ass.address=vac.vac_address)
left join (select distinct on (pin)
  last_value(pin) OVER wnd as pin,
  last_value(tax_year) OVER wnd as scav_tax_year,
  last_value(tax_amount) OVER wnd as scav_tax_amt,
  last_value(total_amount) OVER wnd as scav_tot_amt
FROM landbank_data_scavenger
WINDOW wnd as (
  PARTITION BY pin ORDER BY tax_year
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)) scav on (parcel.pin14=scav.pin)
left join (select
  pin,
  array_to_string(array_agg(distinct granttype),', ','') as brown_grant_types
  from landbank_data_brownfield where pin is not null group by pin
) brown on (parcel.pin14=brown.pin)
left join (select
  name cmap_name,
  status cmap_status,
  study_area cmap_area,
  short_descr cmap_desc,
  url cmap_url,
  loc
  FROM landbank_data_cmapplan
) cmap on (ST_Intersects(cmap.loc,parcel.wkb_geometry))
)
;
create index parcel_with_data_gist on parcel_with_data using gist (wkb_geometry);
create index pin_idx on parcel_with_data (pin);
