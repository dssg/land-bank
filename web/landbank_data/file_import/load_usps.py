import os, csv
from models import VacancyUSPS
from decimal import Decimal
from django.contrib.gis.geos import Point
import datetime

usps_dates = ['032008','062008','092008','122008',\
              '032009','062009','092009','122009',\
              '032010','062010','092010','122010',\
              '032011','062011','092011','122011',\
              '032012','062012','092012','122012',\
              '032013']
files_usps = ['/mnt/ebs/data/usps/USPS_VAC_'+i+'_TRACTSUM_2KX.cook.csv' \
              for i in usps_dates]

def run(verbose = True):
  load_vacancyreport(files_usps, verbose = verbose)

def load_vacancyreport(files_usps, verbose = False):
  for i in range(len(files_usps)):
    f = open(files_usps[i], 'r')
    reader = csv.reader(f)
    reader.next()
    for row in reader:
      year         = int(float(usps_dates[i][2:]))
      quarter      = int(float(usps_dates[i][0:2]))/3
      fips         = None if row[0] =='' else int(float(row[0]))
      naddr_res    = None if row[1] =='' else int(float(row[1]))
      naddr_bus    = None if row[2] =='' else int(float(row[2]))
      naddr_oth    = None if row[3] =='' else int(float(row[3]))
      res_vacant   = None if row[4] =='' else int(float(row[4]))
      bus_vacant   = None if row[5] =='' else int(float(row[5]))
      oth_vacant   = None if row[6] =='' else int(float(row[6]))
      res_vac_avg  = None if row[7] =='' else int(float(row[7]))
      bus_vac_avg  = None if row[8] =='' else int(float(row[8]))
      res_vac_3    = None if row[9] =='' else int(float(row[9]))
      bus_vac_3    = None if row[10]=='' else int(float(row[10]))
      oth_vac_3    = None if row[11]=='' else int(float(row[11]))
      res_vac_3_6  = None if row[12]=='' else int(float(row[12]))
      bus_vac_3_6  = None if row[13]=='' else int(float(row[13]))
      oth_vac_3_6  = None if row[14]=='' else int(float(row[14]))
      res_vac_6_12 = None if row[15]=='' else int(float(row[15]))
      bus_vac_6_12 = None if row[16]=='' else int(float(row[16]))
      oth_vac_6_12 = None if row[17]=='' else int(float(row[17]))
      res_vac_12_24= None if row[18]=='' else int(float(row[18]))
      bus_vac_12_24= None if row[19]=='' else int(float(row[19]))
      oth_vac_12_24= None if row[20]=='' else int(float(row[20]))
      res_vac_24_36= None if row[21]=='' else int(float(row[21]))
      bus_vac_24_36= None if row[22]=='' else int(float(row[22]))
      oth_vac_24_36= None if row[23]=='' else int(float(row[23]))
      res_vac_36   = None if row[24]=='' else int(float(row[24]))
      bus_vac_36   = None if row[25]=='' else int(float(row[25]))
      oth_vac_36   = None if row[26]=='' else int(float(row[26]))
      pqv_is_res   = None if row[27]=='' else int(float(row[27]))
      pqv_is_bus   = None if row[28]=='' else int(float(row[28]))
      pqv_is_oth   = None if row[29]=='' else int(float(row[29]))
      pqv_ns_res   = None if row[30]=='' else int(float(row[30]))
      pqv_ns_bus   = None if row[31]=='' else int(float(row[31]))
      pqv_ns_oth   = None if row[32]=='' else int(float(row[32]))
      res_nostat   = None if row[33]=='' else int(float(row[33]))
      bus_nostat   = None if row[34]=='' else int(float(row[34]))
      oth_nostat   = None if row[35]=='' else int(float(row[35]))
      res_ns_3     = None if row[36]=='' else int(float(row[36]))
      bus_ns_3     = None if row[37]=='' else int(float(row[37]))
      oth_ns_3     = None if row[38]=='' else int(float(row[38]))
      res_ns_3_6   = None if row[39]=='' else int(float(row[39]))
      bus_ns_3_6   = None if row[40]=='' else int(float(row[40]))
      oth_ns_3_6   = None if row[41]=='' else int(float(row[41]))
      res_ns_6_12  = None if row[42]=='' else int(float(row[42]))
      bus_ns_6_12  = None if row[43]=='' else int(float(row[43]))
      oth_ns_6_12  = None if row[44]=='' else int(float(row[44]))
      res_ns_12_24 = None if row[45]=='' else int(float(row[45]))
      bus_ns_12_24 = None if row[46]=='' else int(float(row[46]))
      oth_ns_12_24 = None if row[47]=='' else int(float(row[47]))
      res_ns_24_36 = None if row[48]=='' else int(float(row[48]))
      bus_ns_24_36 = None if row[49]=='' else int(float(row[49]))
      oth_ns_24_36 = None if row[50]=='' else int(float(row[50]))
      res_ns_36    = None if row[51]=='' else int(float(row[51]))
      bus_ns_36    = None if row[52]=='' else int(float(row[52]))
      oth_ns_36    = None if row[53]=='' else int(float(row[53]))
      pqns_is_res  = None if row[54]=='' else int(float(row[54]))
      pqns_is_bus  = None if row[55]=='' else int(float(row[55]))
      pqns_is_oth  = None if row[56]=='' else int(float(row[56]))
      try:
        vacancyreport = VacancyUSPS.objects.get(\
          year         = year         ,\
          quarter      = quarter      ,\
          fips         = fips         ,\
          naddr_res    = naddr_res    ,\
          naddr_bus    = naddr_bus    ,\
          naddr_oth    = naddr_oth    ,\
          res_vacant   = res_vacant   ,\
          bus_vacant   = bus_vacant   ,\
          oth_vacant   = oth_vacant   ,\
          res_vac_avg  = res_vac_avg  ,\
          bus_vac_avg  = bus_vac_avg  ,\
          res_vac_3    = res_vac_3    ,\
          bus_vac_3    = bus_vac_3    ,\
          oth_vac_3    = oth_vac_3    ,\
          res_vac_3_6  = res_vac_3_6  ,\
          bus_vac_3_6  = bus_vac_3_6  ,\
          oth_vac_3_6  = oth_vac_3_6  ,\
          res_vac_6_12 = res_vac_6_12 ,\
          bus_vac_6_12 = bus_vac_6_12 ,\
          oth_vac_6_12 = oth_vac_6_12 ,\
          res_vac_12_24= res_vac_12_24,\
          bus_vac_12_24= bus_vac_12_24,\
          oth_vac_12_24= oth_vac_12_24,\
          res_vac_24_36= res_vac_24_36,\
          bus_vac_24_36= bus_vac_24_36,\
          oth_vac_24_36= oth_vac_24_36,\
          res_vac_36   = res_vac_36   ,\
          bus_vac_36   = bus_vac_36   ,\
          oth_vac_36   = oth_vac_36   ,\
          pqv_is_res   = pqv_is_res   ,\
          pqv_is_bus   = pqv_is_bus   ,\
          pqv_is_oth   = pqv_is_oth   ,\
          pqv_ns_res   = pqv_ns_res   ,\
          pqv_ns_bus   = pqv_ns_bus   ,\
          pqv_ns_oth   = pqv_ns_oth   ,\
          res_nostat   = res_nostat   ,\
          bus_nostat   = bus_nostat   ,\
          oth_nostat   = oth_nostat   ,\
          res_ns_3     = res_ns_3     ,\
          bus_ns_3     = bus_ns_3     ,\
          oth_ns_3     = oth_ns_3     ,\
          res_ns_3_6   = res_ns_3_6   ,\
          bus_ns_3_6   = bus_ns_3_6   ,\
          oth_ns_3_6   = oth_ns_3_6   ,\
          res_ns_6_12  = res_ns_6_12  ,\
          bus_ns_6_12  = bus_ns_6_12  ,\
          oth_ns_6_12  = oth_ns_6_12  ,\
          res_ns_12_24 = res_ns_12_24 ,\
          bus_ns_12_24 = bus_ns_12_24 ,\
          oth_ns_12_24 = oth_ns_12_24 ,\
          res_ns_24_36 = res_ns_24_36 ,\
          bus_ns_24_36 = bus_ns_24_36 ,\
          oth_ns_24_36 = oth_ns_24_36 ,\
          res_ns_36    = res_ns_36    ,\
          bus_ns_36    = bus_ns_36    ,\
          oth_ns_36    = oth_ns_36    ,\
          pqns_is_res  = pqns_is_res  ,\
          pqns_is_bus  = pqns_is_bus  ,\
          pqns_is_oth  = pqns_is_oth   \
        )
      except:
        vacancyreport =  VacancyUSPS(\
          year         = year         ,\
          quarter      = quarter      ,\
          fips         = fips         ,\
          naddr_res    = naddr_res    ,\
          naddr_bus    = naddr_bus    ,\
          naddr_oth    = naddr_oth    ,\
          res_vacant   = res_vacant   ,\
          bus_vacant   = bus_vacant   ,\
          oth_vacant   = oth_vacant   ,\
          res_vac_avg  = res_vac_avg  ,\
          bus_vac_avg  = bus_vac_avg  ,\
          res_vac_3    = res_vac_3    ,\
          bus_vac_3    = bus_vac_3    ,\
          oth_vac_3    = oth_vac_3    ,\
          res_vac_3_6  = res_vac_3_6  ,\
          bus_vac_3_6  = bus_vac_3_6  ,\
          oth_vac_3_6  = oth_vac_3_6  ,\
          res_vac_6_12 = res_vac_6_12 ,\
          bus_vac_6_12 = bus_vac_6_12 ,\
          oth_vac_6_12 = oth_vac_6_12 ,\
          res_vac_12_24= res_vac_12_24,\
          bus_vac_12_24= bus_vac_12_24,\
          oth_vac_12_24= oth_vac_12_24,\
          res_vac_24_36= res_vac_24_36,\
          bus_vac_24_36= bus_vac_24_36,\
          oth_vac_24_36= oth_vac_24_36,\
          res_vac_36   = res_vac_36   ,\
          bus_vac_36   = bus_vac_36   ,\
          oth_vac_36   = oth_vac_36   ,\
          pqv_is_res   = pqv_is_res   ,\
          pqv_is_bus   = pqv_is_bus   ,\
          pqv_is_oth   = pqv_is_oth   ,\
          pqv_ns_res   = pqv_ns_res   ,\
          pqv_ns_bus   = pqv_ns_bus   ,\
          pqv_ns_oth   = pqv_ns_oth   ,\
          res_nostat   = res_nostat   ,\
          bus_nostat   = bus_nostat   ,\
          oth_nostat   = oth_nostat   ,\
          res_ns_3     = res_ns_3     ,\
          bus_ns_3     = bus_ns_3     ,\
          oth_ns_3     = oth_ns_3     ,\
          res_ns_3_6   = res_ns_3_6   ,\
          bus_ns_3_6   = bus_ns_3_6   ,\
          oth_ns_3_6   = oth_ns_3_6   ,\
          res_ns_6_12  = res_ns_6_12  ,\
          bus_ns_6_12  = bus_ns_6_12  ,\
          oth_ns_6_12  = oth_ns_6_12  ,\
          res_ns_12_24 = res_ns_12_24 ,\
          bus_ns_12_24 = bus_ns_12_24 ,\
          oth_ns_12_24 = oth_ns_12_24 ,\
          res_ns_24_36 = res_ns_24_36 ,\
          bus_ns_24_36 = bus_ns_24_36 ,\
          oth_ns_24_36 = oth_ns_24_36 ,\
          res_ns_36    = res_ns_36    ,\
          bus_ns_36    = bus_ns_36    ,\
          oth_ns_36    = oth_ns_36    ,\
          pqns_is_res  = pqns_is_res  ,\
          pqns_is_bus  = pqns_is_bus  ,\
          pqns_is_oth  = pqns_is_oth   \
        )
      vacancyreport.save()
    f.close()
