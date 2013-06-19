#!/usr/bin/env python2.7

# Plotting & numeric libraries
import matplotlib,pylab
import numpy as np
# Geo libraries
from osgeo import gdal,ogr,osr
# Standard crap
import sys, csv, random
import httplib,json
import cPickle

datadir = '/mnt/ebs/data/census/'

class comm_areas:
  # Info about community areas, pre-saved to Pickle file.
  # Nothing fancy, just taken off the Chicago data portal.
  def __init__(self):
    f         = open(datadir + 'comm_areas.p','rb')
    self.data = cPickle.load(f)

class census:
  # A class that encapsulates a decadal census and makes it somewhat easier to use.
  # Each census object can have several dictionaries. All should have census.data,
  # which is the tract-level decadal census. Users may also optionally fill:
  # census.acs_data   : selected american community survey / long form data
  # census.block_data : data aggregated to blocks -- warning, very large.
  # census.data10     : pre-2010 data aggregated to the 2010 tract boundaries.
  # census.acs_data10 : same deal with the long form data.
  def __init__(self, year):
    # Initialize variables
    self.year      = year
    self.data      = {}
    self.acs_data  = None
    self.ca        = comm_areas()
    geo_file,data_file = None,None

    # Read in the shapefiles and data, which are slightly different
    # depending on the year.
    if year == 2000:
      geo_file  = datadir+'censustracts.2000/Census_Tracts.shp'
      data_file = datadir+'censustractdata.2000/DEC_00_SF1_DP1_with_ann.csv'
    elif year == 2010:
      geo_file  = datadir+'censustracts.2010/CensusTractsTIGER2010.shp'
      data_file = datadir+'censustractdata.2010/DEC_10_SF1_SF1DP1_with_ann.csv'
    else:
      raise ValueError('Year '+str(self.year)+' not known')

    # Load the geometry
    self.load_geo(geo_file)
    # And the tract-level data.
    self.load_data(data_file)

  def load_geo(self,geo_file):
    # Read in the tract-level shapefile.
    self.geo_file  = ogr.Open(geo_file)
    self.geo_layer = self.geo_file.GetLayer(0)

    # Declare the coordinate transform from lat/long to the Chicago projection.

    # City limits, used for chopping out the area taken up by water.
    g=ogr.Open(datadir+'CityLimits/City_Boundary.shp')
    l=g.GetLayer(0)
    citylimits=l[0]
    g=citylimits.GetGeometryRef()
    cl=g.GetGeometryRef(0)
    
    # Loop through census tracts.
    for i in range(self.geo_layer.GetFeatureCount()):
      f = self.geo_layer.GetFeature(i)

      tractid,g,caid = None,None,None

      # Again, things are slightly different by year.
      # There are also a few aggravating special cases to handle.
      if self.year == 2000:
        tractid = f.GetFieldAsString('CENSUS_T_1')
        caid    = f.GetFieldAsString('TRACT_COMM')
        g       = f.GetGeometryRef()
        if tractid=='17031840000': continue
        if tractid=='17031000000': continue
        if tractid=='17031770902': continue
        if tractid=='17031821402': continue

      elif self.year==2010:
        tractid = f.GetFieldAsString('GEOID10')
        caid    = f.GetFieldAsString('COMMAREA')
        g       = f.GetGeometryRef()
        if tractid=='17031770902': continue

      # Fill the geometric fields and the community area fields.
      if not tractid in self.data.keys(): self.data[tractid]={}
      self.data[tractid]['geo']    = g.Clone()
      self.data[tractid]['area']   = g.Intersection(cl).Area()
      self.data[tractid]['ca_num'] = caid
      for ca,ca_num in zip(self.ca.data.keys(),[i['num'] for i in self.ca.data.values()]):
        if ca_num==caid: self.data[tractid]['ca'] = ca

      # Handle the special case where community area ID is not given. Then we want the
      # community area with > 10% overlap, which always happens to be unique.
      if caid=='0':
        for ca in self.ca.data.keys():
          if self.ca.data[ca]['geo'].Intersection(g).Area() >= 0.1*g.Area():
            self.data[tractid]['ca_num']=self.ca.data[ca]['num']
            self.data[tractid]['ca']=ca

      # Another annoying special case.
      if tractid=='17031810501' and self.year==2000:
        self.data[tractid]['ca_num'] = '81'
        self.data[tractid]['ca']     = 'OHARE'
        

  def load_raw_data(self,data_file):
    # Load the raw data into the data dictionary initialized by the geo loader.
    # You can always get the data for a given tract by referring to the metadata
    # to find the column number, and then looking at data[tract]['raw'][column]
    with file(data_file,'r') as csvfile:
      f = csv.reader(csvfile)
      f.next()

      for row in f:
        if row[1] not in self.data.keys(): continue
        self.data[row[1]]['raw']=[]
        for j in range(3,len(row)):
          try:
            self.data[row[1]]['raw'].append(float(row[j]))
          except:
            self.data[row[1]]['raw'].append(-1.0)
        self.data[row[1]]['raw'] = np.array(self.data[row[1]]['raw'])

  def get_legend(self):
    # Declare some human-readable names for these guys, and define the way
    # they get aggregated. This is the "easy way" to get the most useful fields.
    retval={}
    retval['POP_TOT']    = { 2000:  0,  2010: 0,    'pop1_avg2_hu3':1 }
    retval['POP_18PLUS'] = { 2000:  34, 2010: 42,   'pop1_avg2_hu3':1 } 
    retval['POP_65PLUS'] = { 2000:  44, 2010: 48,   'pop1_avg2_hu3':1 }
    retval['MEDIAN_AGE'] = { 2000:  32, 2010: 38,   'pop1_avg2_hu3':2 }
    retval['POP_MALE']   = { 2000:  2,  2010: 50,   'pop1_avg2_hu3':1 }
    retval['POP_WHITE']  = { 2000:  52, 2010: 154,  'pop1_avg2_hu3':1 }
    retval['POP_BLACK']  = { 2000:  54, 2010: 156,  'pop1_avg2_hu3':1 }
    retval['POP_AMIND']  = { 2000:  56, 2010: 158,  'pop1_avg2_hu3':1 }
    retval['POP_ASIAN']  = { 2000:  58, 2010: 160,  'pop1_avg2_hu3':1 }
    retval['POP_MRACE']  = { 2000:  86, 2010: 188,  'pop1_avg2_hu3':1 }
    retval['POP_WHITENH']= { 2000: 114, 2010: 244,  'pop1_avg2_hu3':1 }
    retval['POP_HISP']   = { 2000: 102, 2010: 212,  'pop1_avg2_hu3':1 }
    retval['HOUSEHOLDS'] = { 2000: 142, 2010: 298,  'pop1_avg2_hu3':1 }
    retval['HHSIZE']     = { 2000: 166, 2010: 332,  'pop1_avg2_hu3':2 }
    retval['HUNITS']     = { 2000: 170, 2010: 336,  'pop1_avg2_hu3':3 }
    retval['HOCC']       = { 2000: 172, 2010: 338,  'pop1_avg2_hu3':3 }
    retval['HOOCC']      = { 2000: 184, 2010: 360,  'pop1_avg2_hu3':3 }
    retval['HROCC']      = { 2000: 186, 2010: 366,  'pop1_avg2_hu3':3 }
    return retval

  def load_data(self,data_file):
    # Load the raw data, then pick out a few useful fields and name them.
    # So, to get the non-Hispanic white population in a given tract, you can
    # ask for data[tract]['POP_WHITENH'].
    self.load_raw_data(data_file)
    legend=self.get_legend()

    for i in self.data.keys():
      for j in legend.keys():
        self.data[i][j] = self.data[i]['raw'][legend[j][self.year]]


  # The block geo and data loaders are pretty much just like the tract ones.
  # I'm going to use that as an excuse to not comment the code.
  def load_block_geo(self,geo_file=datadir+'censusblocks.2010/CensusBlockTIGER2010.shp'):
    self.block_data={}
    self.geo_file=ogr.Open(geo_file)
    self.geo_layer=self.geo_file.GetLayer(0)

    g=ogr.Open(datadir+'CityLimits/City_Boundary.shp')
    l=g.GetLayer(0)
    citylimits=l[0]
    g=citylimits.GetGeometryRef()
    cl=g.GetGeometryRef(0)

    cas=comm_areas()
    for i in range(self.geo_layer.GetFeatureCount()):
      f=self.geo_layer.GetFeature(i)
      tractid,blockid,g,caid=None,None,None,None
      blockid=f.GetFieldAsString('GEOID10')
      tractid=blockid[:-4]
      if tractid not in self.data.keys(): continue
      if not blockid in self.block_data.keys(): self.block_data[blockid]={}
      g=f.GetGeometryRef()
      self.block_data[blockid]['geo']=g.Clone()
      self.block_data[blockid]['area']=g.Intersection(cl).Area()
      self.block_data[blockid]['ca']=self.data[tractid]['ca']
      if not cas.data[self.data[tractid]['ca']]['geo'].Contains(g):
        for cakey,caval in zip(cas.data.keys(),cas.data.values()):
          if caval['geo'].Contains(g):
            self.block_data[blockid]['ca']=cakey
            break

  def load_block_data(self,data_file=datadir+'censusblockdata.2010/DEC_10_SF1_QTP6_with_ann.csv'):
    with file(data_file,'r') as csvfile:
      f=csv.reader(csvfile)
      labels=f.next()[3:]
      f.next()
      for row in f:
        if row[1] not in self.block_data.keys(): continue
        self.block_data[row[1]]['raw']=[]
        for j in range(3,len(row)):
          try:
            self.block_data[row[1]]['raw'].append(float(row[j]))
          except:
            self.block_data[row[1]]['raw'].append(-1.0)
        self.block_data[row[1]]['raw']=np.array(self.block_data[row[1]]['raw'])
        self.block_data[row[1]]['POP_TOT']=self.block_data[row[1]]['raw'][labels.index('HD01_S01')]
        self.block_data[row[1]]['POP_WHITE']=self.block_data[row[1]]['raw'][labels.index('HD01_S04')]
        self.block_data[row[1]]['POP_BLACK']=self.block_data[row[1]]['raw'][labels.index('HD01_S08')]
        self.block_data[row[1]]['POP_ASIAN']=self.block_data[row[1]]['raw'][labels.index('HD01_S16')]
        self.block_data[row[1]]['POP_WHITENH']=\
          self.block_data[row[1]]['raw'][labels.index('HD01_S04')] - \
          self.block_data[row[1]]['raw'][labels.index('HD01_S05')] 
        self.block_data[row[1]]['POP_BLACKNH']=\
          self.block_data[row[1]]['raw'][labels.index('HD01_S08')] - \
          self.block_data[row[1]]['raw'][labels.index('HD01_S09')] 
        self.block_data[row[1]]['POP_ASIANNH']=\
          self.block_data[row[1]]['raw'][labels.index('HD01_S16')] - \
          self.block_data[row[1]]['raw'][labels.index('HD01_S17')] 
        self.block_data[row[1]]['POP_HISP']=\
          self.block_data[row[1]]['raw'][labels.index('HD01_S03')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S07')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S11')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S15')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S19')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S19')] + \
          self.block_data[row[1]]['raw'][labels.index('HD01_S23')] 
    
  def load_acs_data(self):
    # The ACS/long form data are a little different. There are three files I'll be loading
    # in, and we'll access the i'th column of the j'th file by
    # self.acs_data[tract][prefix[i]+'_' + header[j]].
    # That is to say, self.acs_data[tract]['DP03_HC02_VC54'] is the column labeled
    # HC02_VC54 in file DP03.
    # You can back out what's what by looking at the metadata or annotated files.
    self.acs_data={}
    files=[datadir+'acs.2011/ACS_10_5YR_DP02_with_ann.csv',\
           datadir+'acs.2011/ACS_10_5YR_DP03_with_ann.csv',\
           datadir+'acs.2011/ACS_10_5YR_DP04_with_ann.csv']
    # For 2000 and prior, "ACS" is actually the long-form decadal census.
    if self.year==2000:
      files=[datadir+'longform.2000/DEC_00_SF3_DP2_with_ann.csv',\
             datadir+'longform.2000/DEC_00_SF3_DP3_with_ann.csv',\
             datadir+'longform.2000/DEC_00_SF3_DP4_with_ann.csv']
    prefixes=['DP02','DP03','DP04']

    # We'll loop through all the census tracts and copy the geometry, etc
    # into a dictionary for the ACS.
    for f,prefix in zip(files,prefixes):
      with open(f,'r') as csvfile:
        fcsv=csv.reader(csvfile)
        legend=fcsv.next()
        for row in fcsv:
          if row[1] not in self.data.keys(): continue
          if row[1] not in self.acs_data.keys(): 
            self.acs_data[row[1]]={}
            self.acs_data[row[1]]['geo']=self.data[row[1]]['geo']
            self.acs_data[row[1]]['ca']=self.data[row[1]]['ca']
          # And now we'll create dictionary entries for each item.
          for j in range(3,len(row)):
            try:
              self.acs_data[row[1]][prefix+'_'+legend[j]]=float(row[j])
            except:
              self.acs_data[row[1]][prefix+'_'+legend[j]]=-1

  def aggregate_to_10(self,rel_file=datadir+'il17trf.txt'):
    # Take the 2000 data and put it into the 2010 tract boundaries.
    if self.year == 2010: 
      return
    legend=self.get_legend()
    # These will be our new data dictionaries.
    self.data10={}
    if self.acs_data != None:
      self.acs_data10 = {}

    # Parse the tract relation file.
    with file(rel_file,'r') as csvfile:
      f=csv.reader(csvfile)
      for row in f:
        geoid00=row[3]
        geoid10=row[12]
        areapct00pt=float(row[20])
        arealandpct00pt=float(row[21])
        areapct10pt=float(row[22])
        arealandpct10pt=float(row[23])
        pop10pt=int(row[24])
        poppct00=float(row[25])
        poppct10=float(row[26])
        hu10pt=int(row[27])
        hupct00=float(row[28])
        hupct10=float(row[29])
        if geoid00 not in self.data.keys(): continue

        if geoid10 not in self.data10.keys(): 
          self.data10[geoid10]={}
          for j in legend.keys(): self.data10[geoid10][j]=0.0
        for k,kval in zip(legend.keys(),legend.values()):
          if kval['pop1_avg2_hu3']==1:
            self.data10[geoid10][k] = self.data10[geoid10][k] + \
              self.data[geoid00][k] * poppct00/100.0
          elif kval['pop1_avg2_hu3']==2:
            self.data10[geoid10][k] = self.data10[geoid10][k] + \
              self.data[geoid00][k] * hupct00/100.0
            if k+'_wt' not in self.data10[geoid10].keys():
              self.data10[geoid10][k+'_wt']=0.0
            self.data10[geoid10][k+'_wt']=self.data10[geoid10][k+'_wt']+hupct00/100.0
          else:
            self.data10[geoid10][k] = self.data10[geoid10][k] + \
              self.data[geoid00][k] * hupct00/100.0
          
        if self.acs_data != None:
          if geoid10 not in self.acs_data10.keys():
            self.acs_data10[geoid10]={}
            for k in self.acs_data[geoid00].keys():
              if k=='geo' or k=='ca': continue
              if k not in self.acs_data10[geoid10].keys(): 
                self.acs_data10[geoid10][k]=0.0
              self.acs_data10[geoid10][k] = self.acs_data10[geoid10][k] + \
                self.acs_data[geoid00][k] * poppct00/100.0

    # Handle the data we originally gave nice names in our ''legend''.
    for k,kval in zip(legend.keys(),legend.values()):
      for i in self.data10.keys():
        if kval['pop1_avg2_hu3']!=2: continue
        if self.data10[i][k+'_wt']==0:
          self.data10[i][k]=0.0
        else:
          self.data10[i][k]=self.data10[i][k]/self.data10[i][k+'_wt']
        self.data10[i].pop(k+'_wt')
