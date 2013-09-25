from models import CensusTractIncome as Inc, TractScores as Scores, CensusTract as Tracts

# All tracts with populated house transaction median values
inc = Inc.objects.exclude(med_house_txn_2011=None).order_by('-med_inc')
# Income bin left bounds
binl = [0,10000,15000,25000,35000,50000,75000,100000,150000,200000,300000]

# Loop through each tract-income record
#current = 1
#limit = 10
for i in inc:
#    if current > limit:
#        break
    inc_pcts = [ i.inc_lt_10\
        ,i.inc_10_15\
        ,i.inc_15_25\
        ,i.inc_25_35\
        ,i.inc_35_50\
        ,i.inc_50_75\
        ,i.inc_75_100\
        ,i.inc_100_150\
        ,i.inc_150_200\
        ,i.inc_gt_200 ]
#    print u'inc_pcts:' + unicode(inc_pcts)
    unaff_pct = 0.0
    for j in range(len(binl)-1):
#        print u'j:'+unicode(j)
        if i.med_house_txn_2011 > 4*binl[j+1]:
#            print u'med txn $' + unicode(i.med_house_txn_2011) + u'>$' + unicode(4*binl[j+1]) + u'...'
            unaff_pct += inc_pcts[j]
#            print u'unaff_pct'+unicode(unaff_pct)
        else:
#            print u'med txn $' + unicode(i.med_house_txn_2011) + u'<$' + unicode(4*binl[j+1]) + u'...'
            bin_diff = 4 * float(binl[j+1] - binl[j])
#            print u'bin_diff $' + unicode(bin_diff)
            txn_diff = float(i.med_house_txn_2011 - 4*binl[j])
#            print u'txn_diff $' + unicode(txn_diff)
            unaff_pct += inc_pcts[j] * (txn_diff / bin_diff)
#            print u'unaff_pct:' + unicode(unaff_pct) + u' and breaking...'
            break
    aff_pct = 100.0 - unaff_pct
#    print u'aff_pct:' + unicode(aff_pct)
    try: t = Tracts.objects.get(fips=i.fips)
    except: continue
    try: s = Scores.objects.get(census_tract_id=t.id)
    except: continue
    s.affordability = aff_pct
    s.save()
#    current += 1

