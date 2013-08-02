-- Copies affordability index joined with geometry into an unmanaged table, for mapping purposes
drop table tract_affordability;
select loc, affordability 
into tract_affordability 
from landbank_data_censustract tract 
left join landbank_data_tractscores scores 
on (tract.id=scores.census_tract_id);
