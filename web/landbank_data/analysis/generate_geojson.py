from models import CommunityArea, Ward, Municipality, CensusTract 
import json

# Set desired output directory for JSON files here

target_directory = 'landbank_data/static/landbank_data/json/'

# Define all models to be used
all_geographies = [{
    'name':'communityarea'
    ,'queryset':CommunityArea.objects.all().values('geom')
    ,'geom_field_name':'geom'
    },{ 
    'name':'ward'
    ,'queryset':Ward.objects.all().values('geom')
    ,'geom_field_name':'geom'
    },{ 
    'name':'municipality'
    ,'queryset':Municipality.objects.all().values('geom')
    ,'geom_field_name':'geom'
    },{ 
    'name':'censustract'
    ,'queryset':CensusTract.objects.all().values('loc')
    ,'geom_field_name':'loc'
    }]  

for g in all_geographies:
    print 'Building GeoJSON for geography type: ' + g['name']
    feature_collection = {'type':'FeatureCollection', 'features':[]}
    areas = g['queryset']
    for a in areas:
        geometry = a[g['geom_field_name']].transform(4326, clone=True)
        geojson = json.loads(geometry.json)
        feature = {'type':'Feature', 'geometry':geojson}
        feature_collection['features'].append(feature)
    # write json to <name>.js
    js_filename = target_directory + g['name'] + '.js'
    js_file = open(js_filename, 'w')
    file_string = 'var ' + g['name'] + '_geojson = ' + json.dumps(feature_collection) + ';'
    js_file.write(file_string)

