from models import CommunityArea, Ward, Municipality, CensusTract, IndicatorCache
import json

# Set desired output directory for JSON files here

target_directory = 'landbank_data/static/landbank_data/json/'

# Define all models to be used
all_geographies = [{
    'name':'communityarea'
    ,'indicator_alias':'Community Area'
    ,'queryset':CommunityArea.objects.all()
    ,'specific_fields':[{
        'column_name':'area_number'
        ,'display_name':'#'
        },{
        'column_name':'area_name'
        ,'display_name':'Area Name'
        }]
    },{
    'name':'ward'
    ,'indicator_alias':'Ward'
    ,'queryset':Ward.objects.all()
    ,'specific_fields':[{
        'column_name':'ward'
        ,'display_name':'Ward'
        },{
        'column_name':'alderman'
        ,'display_name':'Alderman'
        }]
    },{
    'name':'municipality'
    ,'indicator_alias':'Municipality'
    ,'queryset':Municipality.objects.all()
    ,'geom_field_name':'geom'
    ,'specific_fields':[{
        'column_name':'name'
        ,'display_name':'Name'
        }]
    },{
    'name':'censustract'
    ,'indicator_alias':'Census Tract'
    ,'queryset':CensusTract.objects.all()
    ,'specific_fields':['fips']
    ,'specific_fields':[{
        'column_name':'fips'
        ,'display_name':'FIPS Code'
        }]
    }]  

indicator_columns = [{
    'indicator_name':'foreclosure_rate'
    ,'display_name':'Foreclosure Rate'
    },{
    'indicator_name':'vacancy_usps'
    ,'display_name':'Vacancy Rate'
    },{
    'indicator_name':'med_inc'
    ,'display_name':'Median Income'
    }]

for g in all_geographies:
    print 'Building JSON for geography type: ' + g['name']
    table_data = []
    areas = g['queryset']
    for a in areas:
        row_data = []
        # load all specific fields
        for sf in g['specific_fields']:
            row_data.append(getattr(a,sf['column_name']))
        # load all indicator values
        for ic in indicator_columns:
            indicator_value = getattr(IndicatorCache.objects.filter(
                 area_type__exact=g['indicator_alias']
                 ,indicator_name__exact=ic['indicator_name']
                 ,area_id__exact=a.id)\
                 .order_by('-indicator_date')[:1][0]\
             ,'indicator_value'\
            )
            if isinstance(indicator_value, float):
                indicator_value = round(indicator_value,3)
            row_data.append(indicator_value)
             
        table_data.append(row_data)
    output_obj = {"aaData":table_data}
    output_json = json.dumps(output_obj)
    # write json to <name>.js
    js_filename = target_directory + g['name'] + '_table.json'
    js_file = open(js_filename, 'w')
    js_file.write(output_json)

