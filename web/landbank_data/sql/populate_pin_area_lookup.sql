-- Deletes all rows from pin area lookup table and restarts primary key at 1
truncate landbank_data_pinarealookup;
alter sequence landbank_data_pinarealookup_id_seq restart;
-- Re-populates pin area lookup table with primary key, if applicable, of the 
-- ward, community area and census tract containing each property (represented
--  by its PIN)
insert into landbank_data_pinarealookup 
    (pin, ward_id, community_area_id, census_tract_id)
    select assessor.pin
        ,pin_ward.ward_id
        ,pin_ca.community_area_id
        ,pin_tract.census_tract_id
    from landbank_data_assessor as assessor
    left join
        (select lda.pin
            ,ldw.id as ward_id
        from landbank_data_assessor as lda
            ,landbank_data_wards as ldw
        where ST_Intersects(lda.loc, ldw.geom)) as pin_ward
    on (assessor.pin = pin_ward.pin)
    left join
        (select lda.pin
            ,ldca.id as community_area_id
        from landbank_data_assessor as lda
            ,landbank_data_communityareas as ldca
        where ST_Intersects(lda.loc, ldca.geom)) as pin_ca
    on (assessor.pin = pin_ca.pin)
    left join
        (select lda.pin
            ,ldc.id as census_tract_id
        from landbank_data_assessor as lda
            ,landbank_data_censustract as ldc
        where ST_Intersects(lda.loc, ldc.loc)) as pin_tract
    on (assessor.pin = pin_tract.pin)
    order by assessor.pin asc;
