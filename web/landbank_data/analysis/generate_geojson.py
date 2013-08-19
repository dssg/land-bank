from models import CommunityArea, Ward, Municipality, CensusTract, IndicatorCache
import json

# Set desired output directory for JSON files here
target_directory = 'landbank_data/static/landbank_data/json/'
heat_map_bins = 5

# 0th element in "specific fields" list is assumed to be the "id" field
all_geographies = [{
    'name':'communityarea'
    ,'queryset':CommunityArea.objects.all()#.values('geom')
    ,'geom_field_name':'geom'
    ,'specific_fields':[{
        'column_name':'area_number'
        ,'display_name':'#'
        },{ 
        'column_name':'area_name'
        ,'display_name':'Area Name'
        }]
    },{ 
    'name':'ward'
    ,'queryset':Ward.objects.all()
    ,'geom_field_name':'geom'
    ,'specific_fields':[{
        'column_name':'ward'
        ,'display_name':'#'
        },{ 
        'column_name':'alderman'
        ,'display_name':'Alderman'
        }]  
    },{ 
    'name':'municipality'
    ,'queryset':Municipality.objects.all()
    ,'geom_field_name':'geom'
    ,'specific_fields':[{
        'column_name':'name'
        ,'display_name':'Name'
        }]  
    },{ 
    'name':'censustract'
    ,'queryset':CensusTract.objects.all()
    ,'geom_field_name':'loc'
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
    print 'Building GeoJSON for geography type: ' + g['name']
    feature_collection = {'type':'FeatureCollection', 'features':[]}
    areas = g['queryset']
    areas_count = areas.count()
    for a in areas:
        feature_id = g['name'] + '_' + str(getattr(a, g['specific_fields'][0]['column_name']))
        geometry = getattr(a,g['geom_field_name']).transform(4326, clone=True)
        geojson = json.loads(geometry.json)
        data = {'id':feature_id,'color_id':a.color_id}
        #for sf in g['specific_fields']:
        #    data[sf['display_name']] = getattr(a, sf['column_name'])
        # todo: add map coloration ID based on binning...
        feature = {'type':'Feature', 'data': data, 'geometry':geojson}
        feature_collection['features'].append(feature)
    # write json to <name>.js
    js_filename = target_directory + g['name'] + '_geojson.js'
    js_file = open(js_filename, 'w')
    file_string = 'var ' + g['name'] + '_geojson = ' + json.dumps(feature_collection) + ';'
    js_file.write(file_string)
