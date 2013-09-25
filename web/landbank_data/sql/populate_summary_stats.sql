-- Deletes all rows from summary stats table and restarts primary key at 1
truncate landbank_data_summarystats;
alter sequence landbank_data_summarystats_id_seq restart;
-- Re-populates summary stats table
insert into landbank_data_summarystats
    (area_type
    ,area_number
    ,area_name
    ,ptype_id
    ,count
    ,bldg_assmt_avg
    ,land_assmt_avg
    ,total_assmt_avg
    ,bldg_sqft_avg
    ,land_sqft_avg
    ,ppsf_avg)
    (select 
        'Community Area' as area_type
        ,ldca.area_number::bigint as area_number
        ,ldca.area_name as area_name
        ,lda.pt_type1_cat as ptype
        ,count(*)
        ,avg(current_building_assmt) as bldg_assmt_avg
        ,avg(current_land_assmt) as land_assmt_avg
        ,avg(current_total_assmt) as total_assmt_avg
        ,case when avg(sqft_bldg)>0 then avg(sqft_bldg) else null end as bldg_sqft_avg
        ,avg(sqft_land) as land_sqft_avg
        ,avg(case when (type_pt_sf=1 and sqft_bldg>0) then current_building_assmt/sqft_bldg else null end)*10 as ppsf_avg
    from landbank_data_communityarea as ldca
        ,landbank_data_assessor as lda
        ,landbank_data_pinarealookup as ldpal
    where ldca.id = ldpal.community_area_id
        and ldpal.pin = lda.pin
    group by area_number, 
        area_type 
        ,area_name
        ,pt_type1_cat
    order by area_number, ptype asc)
    UNION ALL
    (select 
        'Ward' as area_type
        ,ldw.ward::bigint as area_number
        ,ldw.alderman as area_name
        ,lda.pt_type1_cat as ptype
        ,count(*)
        ,avg(current_building_assmt) as bldg_assmt_avg
        ,avg(current_land_assmt) as land_assmt_avg
        ,avg(current_total_assmt) as total_assmt_avg
        ,case when avg(sqft_bldg)>0 then avg(sqft_bldg) else null end as bldg_sqft_avg
        ,avg(sqft_land) as land_sqft_avg
        ,avg(case when (type_pt_sf=1 and sqft_bldg>0) then current_building_assmt/sqft_bldg else null end)*10 as ppsf_avg
    from landbank_data_ward as ldw
        ,landbank_data_assessor as lda
        ,landbank_data_pinarealookup as ldpal
    where ldw.id = ldpal.ward_id
        and ldpal.pin = lda.pin
    group by area_number, 
        area_type 
        ,area_name
        ,pt_type1_cat
    order by area_number, ptype asc)
    UNION ALL
    (select 
        'Census Tract' as area_type
        ,ldc.fips as area_number --already a bigint
        ,null as area_name
        ,lda.pt_type1_cat as ptype
        ,count(*)
        ,avg(current_building_assmt) as bldg_assmt_avg
        ,avg(current_land_assmt) as land_assmt_avg
        ,avg(current_total_assmt) as total_assmt_avg
        ,case when avg(sqft_bldg)>0 then avg(sqft_bldg) else null end as bldg_sqft_avg
        ,avg(sqft_land) as land_sqft_avg
        ,avg(case when (type_pt_sf=1 and sqft_bldg>0) then current_building_assmt/sqft_bldg else null end)*10 as ppsf_avg
    from landbank_data_censustract as ldc
        ,landbank_data_assessor as lda
        ,landbank_data_pinarealookup as ldpal
    where ldc.id = ldpal.census_tract_id
        and ldpal.pin = lda.pin
    group by area_number, 
        area_type 
        ,area_name
        ,pt_type1_cat
    order by area_number, ptype asc);
