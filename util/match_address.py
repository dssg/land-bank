#!/usr/bin/env python
# A brute force address-to-PIN converter.

import psycopg2
import sys

###########################################################
def levenshtein(a,b):
  "Calculates the Levenshtein distance between a and b."
  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n
    
  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]                                                                                  
      if a[j-1] != b[i-1]:
          change = change + 1
      current[j] = min(add, delete, change)

  return current[n]

###########################################################

def addr_to_xypin(addr_str, conn):
  # Returns (x, y, pin).

  # Our strategy here is going to be to tokenize the input
  # and try to break it into number, street name, place.
 
  # First get a list of all places (a.k.a. cities)
  cur = conn.cursor()
  places = []
  cur.execute('SELECT DISTINCT placename FROM addresspoints')
  for row in cur:
    places.append(row[0].upper())

  # Tokenize the input.
  addr_str = addr_str.replace(',',' ')
  addr_split = [i.upper() for i in addr_str.split()]

  # Unpack some abbreviations.
  abbreviations = {
    'N':   'NORTH',
    'E':   'EAST',
    'S':   'SOUTH',
    'W':   'WEST',
    'AVE': 'AVENUE',
    'ST':  'STREET',
    'PL':  'PLACE',
    'CTR': 'CENTER', 
    'PKWY':'PARKWAY',
    'HWY': 'HIGHWAY',
    'BLVD':'BOULEVARD',
    'RD':  'ROAD',
    'SQ':  'SQUARE',
    'WY':  'WAY',
    'HTS': 'HEIGHTS',
  }
  for key,val in abbreviations.iteritems():
    if key in addr_split:
      addr_split[addr_split.index(key)] = val

  # Remove state, country, and zip code if they exist.
  for iterstrip in range(1,6):
    # Check for country
    if addr_split[-1]=='US' or addr_split[-1]=='USA':
      addr_split=addr_split[:-1]
    # Check for ZIP
    if len(addr_split[-1])==5:
      try:
        int(addr_split[-1])
        addr_split=addr_split[:-1]
      except:
        pass
    # Check for ZIP+4
    if len(addr_split[-1])==10:
      try:
        int(addr_split[-1][0:5])
        int(addr_split[-1][6:])
        addr_split=addr_split[:-1]
      except:
        pass
    # Check for state
    if addr_split[-1]=='IL':
      addr_split=addr_split[:-1]

  # Identify the place name (Oak Brook, Chicago, etc.)
  # The goal is to set placename = 'CHICAGO'
  # and addrname to '1060 WEST ADDISON STREET'.
  placename = None
  addrname  = addr_split
  if addr_split[-1] in places:
    placename  = addr_split[-1]
    addrname = addr_split[:-1]
  elif ' '.join(addr_split[-2:]) in places:
    placename  = ' '.join(addr_split[-2:])
    addrname = addr_split[:-2]
  elif ' '.join(addr_split[-3:]) in places:
    placename  = ' '.join(addr_split[-3:])
    addrname = addr_split[:-3]
  else:
    # OK, not an exact match. Search using levenshtein distance.
    mindist = 9e9
    for nwords in range(1,4):
      for place in places:
        dist = levenshtein(' '.join(addr_split[-nwords:]),place)
        if dist < mindist:
          placename = place
          mindist = dist
          addrname = addr_split[:-nwords]

  # Get a list of unique street names.
  streets = []
  cur.execute('SELECT DISTINCT stnamecom FROM addresspoints '+\
              'WHERE upper(placename)=%s AND stnamecom IS NOT NULL',\
              (placename,))
  for row in cur:
    streets.append(row[0].upper())
  
  # Same as above; this time, try to split '1060 W ADDISON' into
  # '1060' and 'W ADDISON'.
  streetname = None
  streetnum  = addrname
  mindist = 9e9
  for nwords in range(1,len(addrname)+1):
    if ' '.join(addrname[-nwords:]) in streets:
      streetname = ' '.join(addrname[-nwords:])
      streetnum  = addrname[:-nwords]

  # No exact match, do levenshtein.
  if streetname==None: 
    for nwords in range(1,len(addrname)+1):
      for street in streets:
        dist = levenshtein(' '.join(addrname[-nwords:]),street)
        if dist < mindist:
          streetname = street
          mindist = dist
          streetnum = addrname[:-nwords]

  # OK, now try to identify the closest match to the street number.
  addrnums = []
  cur.execute('SELECT DISTINCT addrnocom FROM addresspoints '+\
              'WHERE upper(placename)=%s AND stnamecom=%s AND addrnocom IS NOT NULL',\
              (placename, streetname))
  for row in cur:
    addrnums.append(row[0])

  addrnum = None
  for nwords in range(1,len(streetnum)+1):
    if ' '.join(streetnum[-nwords:]) in addrnums:
      addrnum  = ' '.join(streetnum[-nwords:])

  if addrnum==None: 
    for nwords in range(1,len(streetnum)+1):
      for addr in addrnums:
        dist = levenshtein(' '.join(streetnum[-nwords:]),addr)
        if dist < mindist:
          addrnum = addr
          mindist = dist

  # Now we have a match, so let's get a PIN.
  cur.execute('SELECT ST_X(geom), ST_Y(geom), pin FROM addresspoints '+\
              'WHERE upper(placename)=%s AND stnamecom=%s AND '+\
              'addrnocom=%s',\
              (placename, streetname,addrnum))

  # Decide on the return value.
  retval = []
  for row in cur:
    retval.append(row)
  if len(retval) == 0:
    print 'Address not found!'
    return None
  if len(retval) > 1:
    print 'Ambiguous address!'
    print retval
    return retval[0]
  return retval[0]

if __name__ == '__main__':
  conn = psycopg2.connect(host = 'localhost',\
                          user = 'postgres',\
                          password = 'postgres',\
                          dbname = 'landbank')

  print addr_to_xypin(' '.join(sys.argv[1:]),conn)

