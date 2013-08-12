CREATE TABLE IF NOT EXISTS countylimits AS (
  SELECT ST_Union(loc) geom FROM landbank_data_censustract);
DELETE FROM landbank_data_municipality USING countylimits 
  WHERE ST_Area(ST_Intersection(landbank_data_municipality.geom, countylimits.geom)) = 0;
