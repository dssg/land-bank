#!/usr/bin/env python
import psycopg2

# Duplicate this table:
# http://www.housingstudies.org/dataportal/composition/housing-units-composition/community-area/2012/2012/

conn = psycopg2.connect(\
  database = 'landbank',\
  user     = 'postgres',\
  host     = 'localhost',\
  password = 'postgres')

cur = conn.cursor()

select_sql = '''
SELECT DISTINCT ca_name FROM landbank_data_assessor
'''
cur.execute(select_sql)
commareas = cur.fetchall()

for commarea in sorted([i[0] for i in commareas]):

  select_sql = '''
    SELECT pt_type1_cat,SUM(estim_hunit)
    FROM landbank_data_assessor WHERE ca_name=%s
    GROUP BY pt_type1_cat
  '''

  cur.execute(select_sql, (commarea,))
  out=cur.fetchall()
  tot_units = sum([i[1] for i in out])
  sf        = sum([i[1] for i in out if i[0]==1])
  condo     = sum([i[1] for i in out if i[0]==2])
  twotofour = sum([i[1] for i in out if i[0]==3])
  fiveplus  = sum([i[1] for i in out if i[0]==4])

  print('%30s %6.1f %6.1f %6.1f %6.1f' % (commarea, \
    float(sf)/tot_units*100,\
    float(condo)/tot_units*100,\
    float(twotofour)/tot_units*100,\
    float(fiveplus)/tot_units*100))
