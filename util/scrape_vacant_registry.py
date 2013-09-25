#!/usr/bin/env python2.7
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import sys, pprint, cPickle

# This is where the data will live
bldgs = {}

def parse_resp(response):
  global bldgs
  X, Y, addrs, types = [], [], [], []
  soup = BeautifulSoup(response)
  scripts = soup.find_all('script')
  for script in scripts:
    this = script.string
    if this is None: continue
    if this.find('var xCoordinates =')==-1: continue
    idx1 = this.index('var xCoordinates =')
    idx2 = this.index('var yCoordinates =')
    Xtxt = this[idx1:idx2].split('(')[1].split(')')[0]
    X    = [i.split("'") for i in Xtxt.split(',') if len(i.split("'"))>1]
    idx1 = this.index('var yCoordinates =')
    idx2 = this.index('var pointIDs =')
    Ytxt = this[idx1:idx2].split('(')[1].split(')')[0]
    Y    = [i.split("'") for i in Ytxt.split(',') if len(i.split("'"))>1]
    idx1 = this.index('var pointDescs =')
    idx2 = this.index('var pointTypes =')
    Atxt = this[idx1:idx2].split('(')[1].split(')')[0]
    addrs= [i.split("'")[1] for i in Atxt.split(',') if len(i.split("'"))>1]
    idx1 = this.index('var pointTypes =')
    idx2 = this.index('var centerX =')
    Ttxt = this[idx1:idx2].split('(')[1].split(')')[0]
    types= [i.split("'")[1] for i in Ttxt.split(',') if len(i.split("'"))>1]

    for thisx, thisy, thisaddr, thistype in zip(X, Y, addrs, types):
      if thisaddr not in bldgs.keys():
        bldgs[thisaddr] = {}
      bldgs[thisaddr]['X'] = thisx
      bldgs[thisaddr]['Y'] = thisy
      if 'types' not in bldgs[thisaddr].keys():
        bldgs[thisaddr]['types'] = [thistype]
      else:
        if thistype not in bldgs[thisaddr]['types']: 
          bldgs[thisaddr]['types'].append(thistype)

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

for ca in range(1,78):
  cas = '%02d' % (ca,)
  print cas+' starting'
  address ='https://ipiweb.cityofchicago.org/VBR/MapSearch.aspx?SearchType=CommunityArea&SearchValue='+cas
  response = urllib2.urlopen(address).read()
  parse_resp(response)
  soup = BeautifulSoup(response)
  viewstate = soup.select("#__VIEWSTATEID")[0]['value']
  eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
  
  values = {
  '__EVENTTARGET': 'ctl00$cphMain$cblCaseGroups$2',
  '__EVENTARGUMENT': '',
  '__LASTFOCUS': '',
  '__VIEWSTATEID': viewstate,
  '__VIEWSTATE': '',
  '__EVENTVALIDATION': eventvalidation,
  'ctl00$ctl10$ddlSearchType': '',
  'ctl00$ctl10$txtNumber': '',
  'ctl00$ctl10$ddlDirection': '',
  'ctl00$ctl10$txtStreetName': '',
  'ctl00$ctl10$ddlSuffix': '',
  'ctl00$ctl10$txtCaseNumberSearch': '',
  'ctl00$ctl10$txtCircuitCourtCaseNumberSearch': '',
  'ctl00$ctl10$txtServiceRequestNumberSearch': '',
  'ctl00$ctl10$txtRegistrationNumberSearch': '',
  'ctl00$ctl10$ddlBuildingGrid': 'HEALTH',
  'ctl00$ctl10$ddlCommunityArea': '01',
  'ctl00$ctl10$ddlPoliceDistrict':'01',
  'ctl00$ctl10$ddlWard': '01',
  'ctl00$ctl09$username': '',
  'ctl00$ctl09$password': '',
  'ctl00$cphMain$cblCaseGroups$1': 'DEMO COURT',
  'ctl00$cphMain$cblCaseGroups$2': 'DEMOLISHED',
  'ctl00$cphMain$hdnPopup': ''}
  data = urllib.urlencode(values)
  headers = {
  'Origin': 'https://ipiweb.cityofchicago.org',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Referer': 'https://ipiweb.cityofchicago.org/VBR/MapSearch.aspx?SearchType=CommunityArea&SearchValue='+cas,
  }
  req = urllib2.Request(address,data,headers)
  
  # Read in the response to a HTTP request
  response = urllib2.urlopen(req).read()
  parse_resp(response)
  
  values['__EVENTTARGET']='ctl00$cphMain$cblCaseGroups$3'
  values['ctl00$cphMain$cblCaseGroups$3']='BOARD UP ONLY'
  data = urllib.urlencode(values)
  req = urllib2.Request(address,data,headers)
  response = urllib2.urlopen(req).read()
  parse_resp(response)
  
  values['__EVENTTARGET']='ctl00$cphMain$cblCaseGroups$4'
  values['ctl00$cphMain$cblCaseGroups$4']='WRECKED BY OWNER'
  data = urllib.urlencode(values)
  req = urllib2.Request(address,data,headers)
  response = urllib2.urlopen(req).read()
  parse_resp(response)
  
  values['__EVENTTARGET']='ctl00$cphMain$cblCaseGroups$5'
  values['ctl00$cphMain$cblCaseGroups$5']='SERVICE REQUEST'
  data = urllib.urlencode(values)
  req = urllib2.Request(address,data,headers)
  response = urllib2.urlopen(req).read()
  parse_resp(response)
  
  values['__EVENTTARGET']='ctl00$cphMain$cblCaseGroups$6'
  values['ctl00$cphMain$cblCaseGroups$6']='VACANT'
  data = urllib.urlencode(values)
  req = urllib2.Request(address,data,headers)
  response = urllib2.urlopen(req).read()
  parse_resp(response)
  
  print cas+' done, size '+str(len(bldgs.keys()))

with open('vacant_building_registry.pkl','wb') as f:
  cPickle.dump(bldgs, f)
