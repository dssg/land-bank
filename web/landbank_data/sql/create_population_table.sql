-- Populate a table with estimated population by interpolating census population
-- across other geometries: Municipality, Comm. Area, Ward
CREATE TABLE population (area_name varchar(100), area_type varchar(50), pop integer);
INSERT INTO  population 
  SELECT m.name, 'Municipality', 
    SUM(p.pop*st_area(st_intersection(m.geom,b.loc))/st_area(b.loc))::int 
    FROM landbank_data_censusblockpopulation p join landbank_data_censusblock b 
    ON (substr(b.fips,1,15)::bigint)=p.fips join landbank_data_municipality m 
    ON st_intersects(m.geom,b.loc) 
    GROUP BY m.geom, m.name
;
INSERT INTO  population 
  SELECT m.area_name, 'Community Area', 
    SUM(p.pop*st_area(st_intersection(m.geom,b.loc))/st_area(b.loc))::int
    FROM landbank_data_censusblockpopulation p join landbank_data_censusblock b 
    ON (substr(b.fips,1,15)::bigint)=p.fips join landbank_data_communityarea m 
    ON st_intersects(m.geom,b.loc) 
    GROUP BY m.geom, m.area_name
;
INSERT INTO  population 
  SELECT m.ward::varchar , 'Chicago Ward' , 
    SUM(p.pop*st_area(st_intersection(m.geom,b.loc))/st_area(b.loc))::int 
    FROM landbank_data_censusblockpopulation p join landbank_data_censusblock b 
    ON (substr(b.fips,1,15)::bigint)=p.fips join landbank_data_ward m 
    ON st_intersects(m.geom,b.loc) 
    GROUP BY m.geom, m.ward
;

INSERT INTO population
  SELECT fips::varchar, 'Census Tract', pop 
  FROM landbank_data_censustractcharacteristics;

