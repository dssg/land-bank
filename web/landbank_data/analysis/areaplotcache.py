from models import CommunityAreas as CA, Wards as W, CensusTract as CT, AreaPlotCache as Cache, Assessor, PinAreaLookup as PAL
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django_pandas.managers import *

# This script should be run whenever we want to update the area plots
def set_or_update_plot(area_type, area_id, key_name, value, area_label):
    cached_data, was_created = Cache.objects.get_or_create(\
        area_type = area_type\
        ,area_id = area_id\
        )
    if was_created:
        print 'created new cache object for ' + area_type + ' ' + str(area_label)
        obj = {key_name: value}
        try: cached_data.json_str = json.dumps(obj)
        except: print obj 
    else:
        print 'got existing cache object for ' + area_type + ' ' + str(area_label)
        # turn json data into a dict
        try: obj = json.loads(cached_data.json_str)
        except: obj = {}
        obj = {key_name: value}
        try: cached_data.json_str = json.dumps(obj)
        except: print obj 
    # save this instance of AreaPlotCache with new/updated data to database
    cached_data.save()

def run():
    create_community_area_plots()
    create_ward_plots()
    create_census_tract_plots()

def create_community_area_plots():
    # exclude the Loop, no SFHs worth mentioning
    # todo: remove this step after adding null-check in pandas/histogram code
    no_sfh = [32]
    for ca in CA.objects.exclude(area_number__in=no_sfh):
        pins = PAL.objects.filter(community_area_id__exact=ca.id).values('pin')
        properties = Assessor.objects.filter(pin__in=pins)
        save_hist_data_from_properties(properties, 'Community Area', ca.id, ca.area_name)

def create_ward_plots():        
    for w in W.objects.all():
        pins = PAL.objects.filter(ward_id__exact=w.id).values('pin')
        properties = Assessor.objects.filter(pin__in=pins)
        save_hist_data_from_properties(properties, 'Ward', w.id, w.ward)

def create_census_tract_plots():
    for ct in CT.objects.all():
        pins = PAL.objects.filter(census_tract_id__exact=ct.id).values('pin')
        properties = Assessor.objects.filter(pin__in=pins)
        save_hist_data_from_properties(properties, 'Census Tract', ct.id, ct.fips)

def save_hist_data_from_properties(properties, area_type_label, area_fk_id, area_name):
    prop_values= properties.values('ptype', 'ptype_desc','sqft_land', 'sqft_bldg','current_land_assmt','current_building_assmt')
    df=pd.DataFrame.from_records(prop_values)
    sf=df[df['ptype']== 1 ]
    sf['sqft_land_tmp']=sf['sqft_land']
    sf['sqft_land_tmp'][sf['sqft_land'] == 0.0]=np.nan
    sf['sqft_bldg_tmp']=sf['sqft_bldg']
    sf['sqft_bldg_tmp'][sf['sqft_bldg'] == 0.0]=np.nan
    sf['land_assmt_11_psf']=sf['current_land_assmt']/sf['sqft_land_tmp']
    sf['bldg_assmt_11_psf']=sf['current_building_assmt']/sf['sqft_bldg_tmp']
    sf['Msqft_land_11']=(10 ** (-3))*sf['sqft_land']
    sf['Msqft_bldg_11']=(10 ** (-3))*sf['sqft_bldg']
    ap_land_psf=sf['land_assmt_11_psf'].map(lambda x: x if x != np.inf else np.nan)
    ap_bldg_psf=sf['bldg_assmt_11_psf'].map(lambda x: x if x != np.inf else np.nan)

    # Building histogram data
    ap_land_psf_data=ap_land_psf[ap_land_psf.notnull()].T
    n_land_psf, bins_land_psf = np.histogram(ap_land_psf_data, bins = np.linspace(0,np.max(ap_land_psf_data,axis=None),11))
    to_hist = ap_bldg_psf.T.values
    to_hist = to_hist[np.logical_not(np.isnan(to_hist))]
    n_bldg_psf, bins_bldg_psf = np.histogram(to_hist, bins = np.linspace(0,np.max(to_hist),11))
    Msqft_land_data =sf['Msqft_land_11'][ap_land_psf.notnull()].T
    Msqft_bldg_data =sf['Msqft_bldg_11'][ap_bldg_psf.notnull()].T
    n_land_msf, bins_land_msf = np.histogram(Msqft_land_data, bins = np.linspace(0,np.max(Msqft_land_data,axis=None),11))
    n_bldg_msf, bins_bldg_msf = np.histogram(Msqft_bldg_data, bins = np.linspace(0,np.max(Msqft_bldg_data,axis=None),11))

    hist_data=build_dict(area_name,n_land_psf,bins_land_psf,n_bldg_psf,bins_bldg_psf,n_land_msf,bins_land_msf,n_bldg_msf,bins_bldg_msf)
    key_name = 'histData'
    plot_title = area_name
    set_or_update_plot(area_type_label, area_fk_id, key_name, hist_data, plot_title)

def build_dict(area_name,n_land_psf,bins_land_psf,n_bldg_psf,bins_bldg_psf,n_land_msf,bins_land_msf,n_bldg_msf,bins_bldg_msf):
        histData = {}
        histData['title']=area_name
        histData['land_psf']=[]
        for b,v in zip(bins_land_psf,n_land_psf):
            histData['land_psf'].append({'x':np.asscalar(b), 'y':np.asscalar(v)})
            histData['bldg_psf'] = []
        for b,v in zip(bins_bldg_psf,n_bldg_psf):
            histData['bldg_psf'].append({'x':np.asscalar(b), 'y':np.asscalar(v)})
        histData['land_msf'] = []
        for b,v in zip(bins_land_msf,n_land_msf):
            histData['land_msf'].append({'x':np.asscalar(b), 'y':np.asscalar(v)})
        histData['bldg_msf'] = []
        for b,v in zip(bins_bldg_msf,n_bldg_msf):
            histData['bldg_msf'].append({'x':np.asscalar(b), 'y':np.asscalar(v)})
        return histData
