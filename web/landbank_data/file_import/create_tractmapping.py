from models import CensusTractMapping, CommunityArea, Ward, Municipality, \
  CensusBlock, CensusBlockPopulation, CensusTract, CensusTractCharacteristics, \
  CensusTractIncome, CensusTractOccupancy
from django.contrib.gis.measure import Area

def run():
  # Wipe out the table.
  CensusTractMapping.objects.all().delete()

  # Loop through tracts.
  for tract in CensusTract.objects.all():
    print tract.fips
    try:
      income = CensusTractIncome.objects.get(fips=tract.fips)
      characteristics = CensusTractCharacteristics.objects.get(fips=tract.fips)
      occupancy = CensusTractOccupancy.objects.get(fips=tract.fips)
    except:
      print('Census data not found for '+str(tract.fips))
      continue
    blocks    = [block for block in CensusBlock.objects.filter(loc__intersects=tract.loc) if len(block.fips)==15]
    blockpops = []
    for block in blocks:
      blockpops.append(CensusBlockPopulation.objects.get(fips=block.fips).pop)
    blockoverlaps = [(tract.loc.intersection(i.loc)).area for i in blocks]
    blocks_nonzero = [(blocks[i], blockpops[i]) for i in range(len(blocks)) \
                      if blockoverlaps[i] > 1.0]
    pop = sum([i[1] for i in blocks_nonzero])
    if pop==0: continue

    # OK, now we know which census blocks fall within the tract.
    # Time to find which municipality, ward, and community area those blocks fall inside.
    cas, munis, wards = {}, {}, {}
    for block, blockpop in blocks_nonzero:
      for c in CommunityArea.objects.filter(geom__intersects=block.loc):
        capct = c.geom.intersection(block.loc).area/block.loc.area 
        if capct < 0.01: continue
        if capct > 0.99: capct=1.0
        if c.id not in cas.keys(): cas[c.id] = blockpop*capct
        else: cas[c.id] += blockpop*capct

      for m in Municipality.objects.filter(geom__intersects=block.loc):
        mpct = m.geom.intersection(block.loc).area/block.loc.area 
        if mpct < 0.01: continue
        if mpct > 0.99: capct=1.0
        if m.id not in munis.keys(): munis[m.id] = blockpop*mpct
        else: munis[m.id] += blockpop*mpct

      for w in Ward.objects.filter(geom__intersects=block.loc):
        wpct = w.geom.intersection(block.loc).area/block.loc.area 
        if wpct < 0.01: continue
        if wpct > 0.99: capct=1.0
        if w.id not in wards.keys(): wards[w.id] = blockpop*wpct
        else: wards[w.id] += blockpop*wpct
      
    for k,v in cas.iteritems():
      frac = v/pop
      if frac < 0.01: continue
      if frac > 0.99: frac=1
      entry = CensusTractMapping(\
        fips = tract.fips,\
        communityarea = CommunityArea.objects.get(id=k),\
        communityarea_frac = frac,\
        income = income,\
        characteristics = characteristics,\
        occupancy = occupancy)
      entry.save()
    for k,v in munis.iteritems():
      frac = v/pop
      if frac < 0.01: continue
      if frac > 0.99: frac=1
      entry = CensusTractMapping(\
        fips = tract.fips,\
        municipality = Municipality.objects.get(id=k),\
        municipality_frac = frac,\
        income = income,\
        characteristics = characteristics,\
        occupancy = occupancy)
      entry.save()
    for k,v in wards.iteritems():
      frac = v/pop
      if frac < 0.01: continue
      if frac > 0.99: frac=1
      entry = CensusTractMapping(\
        fips = tract.fips,\
        ward = Ward.objects.get(id=k),\
        ward_frac = frac,\
        income = income,\
        characteristics = characteristics,\
        occupancy = occupancy)
      entry.save()
     
