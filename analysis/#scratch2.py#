
In [30]:
import pandas as pd
import numpy as np
df=pd.read_table("/home/evan/Documents/chicago/ihs/cook_2011_semi.dat",sep="\t")
print df.columns
Index([pin1, HOUSENO, DIR, STREET, AGE_11, ATTIC_DESC_11, BASEMENT_DESC_11, CLASS_DESCRIPTION_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11, CURRENT_TOTAL_ASSMT_11, EXT_DESC_11, GARAGE_DESC_11, sqft_bldg_11, sqft_land_11, PTYPE2011, Type1_PT_SF, Type1_PT_Condo, Type1_PT_2_4, Type1_PT_5, Type1_PT_NonRes, Type1_PT_Unknown, PT_Type1_Cat, Adj_Modi_Hunit_2011, LAT_Y, LNG_X, Tract_Fix, No_Tract_Info, CA_num, CA_name, Place00, Ward, ChicagoFlag, GISDate], dtype=object)


In [31]:
ward=df['Ward']
tot_val=df['CURRENT_TOTAL_ASSMT_11']
pin=df['pin1']
house=df['HOUSENO']
direction=df['DIR']
street=df['STREET']
age_11=df['AGE_11']
attic_desc_11=df['ATTIC_DESC_11']
basement_desc_11=df['BASEMENT_DESC_11']
class_description_11=df['CLASS_DESCRIPTION_11']
current_building_assmt_11=df['CURRENT_BUILDING_ASSMT_11']
current_land_assmt_11=df['CURRENT_LAND_ASSMT_11']
current_total_assmt_11=df['CURRENT_TOTAL_ASSMT_11']
ext_desc_11=df['EXT_DESC_11']
garage_desc_11=df['GARAGE_DESC_11']
sqft_bldg_11=df['sqft_bldg_11']

In [32]:
sqft_land_11=df['sqft_land_11']
ptype2011=df['PTYPE2011']
type1_pt_SF=df['Type1_PT_SF']
type1_pt_Condo=df['Type1_PT_Condo']
type1_pt_2_4=df['Type1_PT_2_4']
type1_pt_5=df['Type1_PT_5']
type1_pt_NonRes=df['Type1_PT_NonRes']
type1_pt_Unknown=df['Type1_PT_Unknown']
pt_type1_cat=df['PT_Type1_Cat']
adj_modi_hunit_2011=df['Adj_Modi_Hunit_2011']
lat_Y=df['LAT_Y']
lng_X=df['LNG_X']
tract_fix=df['Tract_Fix']
no_tract_Info=df['No_Tract_Info']
ca_num=df['CA_num']
ca_name=df['CA_name']
place00=df['Place00']
ward=df['Ward']
chicagoflag=df['ChicagoFlag']
gisdate=df['GISDate']


In [33]:
df['ca_name']=ca_name.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
df['Ward']=df['Ward'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace()) else x)
df['AGE_11']=age_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace()) else x)
df['CURRENT_BUILDING_ASSMT_11']=df['CURRENT_BUILDING_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
df['CURRENT_LAND_ASSMT_11']=df['CURRENT_LAND_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x) 
df['CURRENT_TOTAL_ASSMT_11']=df['CURRENT_TOTAL_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)


In [34]:
cook_house_stock_properties=pd.concat([ward,chicagoflag,ca_name,ca_num,sqft_bldg_11,sqft_land_11,age_11,current_total_assmt_11,current_building_assmt_11,current_land_assmt_11],join='outer',axis=1)
chicago_house_properties=cook_house_stock_properties[ chicagoflag == 1]

In [35]:
#Drop na's
cook_house_stock_properties=cook_house_stock_properties.dropna()

In [36]:
cook_house_stock_properties?


In [37]:
cook_house_stock_properties.columns
Out [37]:
Index([Ward, ChicagoFlag, CA_name, CA_num, sqft_bldg_11, sqft_land_11, AGE_11, CURRENT_TOTAL_ASSMT_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11], dtype=object)

In [38]:
#process integers
cook_house_stock_properties['CA_num']=cook_house_stock_properties['CA_num'].map(int)
cook_house_stock_properties['sqft_bldg_11']=cook_house_stock_properties['sqft_bldg_11'].map(int)
cook_house_stock_properties['sqft_land_11']=cook_house_stock_properties['sqft_land_11'].map(int)


In [39]:
cook_house_stock_properties['CURRENT_BUILDING_ASSMT_11']=cook_house_stock_properties['CURRENT_BUILDING_ASSMT_11'].map(int)
cook_house_stock_properties['CURRENT_LAND_ASSMT_11']=cook_house_stock_properties['CURRENT_LAND_ASSMT_11'].map(int)
cook_house_stock_properties['CURRENT_TOTAL_ASSMT_11']=cook_house_stock_properties['CURRENT_TOTAL_ASSMT_11'].map(int)


In [40]:
cook_house_stock_properties.columns
Out [40]:
Index([Ward, ChicagoFlag, CA_name, CA_num, sqft_bldg_11, sqft_land_11, AGE_11, CURRENT_TOTAL_ASSMT_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11], dtype=object)

In [ ]:
cook_house_stock_properties['CA_name']=cook_house_stock_properties['CA_name'].map(str.strip)
cook_sums=cook_house_stock_properties.groupby('CA_name').sum()

In [ ]:
cook_sums['CURRENT_TOTAL_ASSMT_11']

In [ ]:
print cook_sums['CURRENT_TOTAL_ASSMT_11'][:15]

In [ ]:
cook_sums['CURRENT_TOTAL_ASSMT_11'].plot(kind="bar",stacked='True')

In [ ]:



In [30]:
import pandas as pd
import numpy as np
df=pd.read_table("/home/evan/Documents/chicago/ihs/cook_2011_semi.dat",sep="\t")
print df.columns
Index([pin1, HOUSENO, DIR, STREET, AGE_11, ATTIC_DESC_11, BASEMENT_DESC_11, CLASS_DESCRIPTION_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11, CURRENT_TOTAL_ASSMT_11, EXT_DESC_11, GARAGE_DESC_11, sqft_bldg_11, sqft_land_11, PTYPE2011, Type1_PT_SF, Type1_PT_Condo, Type1_PT_2_4, Type1_PT_5, Type1_PT_NonRes, Type1_PT_Unknown, PT_Type1_Cat, Adj_Modi_Hunit_2011, LAT_Y, LNG_X, Tract_Fix, No_Tract_Info, CA_num, CA_name, Place00, Ward, ChicagoFlag, GISDate], dtype=object)


In [31]:
ward=df['Ward']
tot_val=df['CURRENT_TOTAL_ASSMT_11']
pin=df['pin1']
house=df['HOUSENO']
direction=df['DIR']
street=df['STREET']
age_11=df['AGE_11']
attic_desc_11=df['ATTIC_DESC_11']
basement_desc_11=df['BASEMENT_DESC_11']
class_description_11=df['CLASS_DESCRIPTION_11']
current_building_assmt_11=df['CURRENT_BUILDING_ASSMT_11']
current_land_assmt_11=df['CURRENT_LAND_ASSMT_11']
current_total_assmt_11=df['CURRENT_TOTAL_ASSMT_11']
ext_desc_11=df['EXT_DESC_11']
garage_desc_11=df['GARAGE_DESC_11']
sqft_bldg_11=df['sqft_bldg_11']

In [32]:
sqft_land_11=df['sqft_land_11']
ptype2011=df['PTYPE2011']
type1_pt_SF=df['Type1_PT_SF']
type1_pt_Condo=df['Type1_PT_Condo']
type1_pt_2_4=df['Type1_PT_2_4']
type1_pt_5=df['Type1_PT_5']
type1_pt_NonRes=df['Type1_PT_NonRes']
type1_pt_Unknown=df['Type1_PT_Unknown']
pt_type1_cat=df['PT_Type1_Cat']
adj_modi_hunit_2011=df['Adj_Modi_Hunit_2011']
lat_Y=df['LAT_Y']
lng_X=df['LNG_X']
tract_fix=df['Tract_Fix']
no_tract_Info=df['No_Tract_Info']
ca_num=df['CA_num']
ca_name=df['CA_name']
place00=df['Place00']
ward=df['Ward']
chicagoflag=df['ChicagoFlag']
gisdate=df['GISDate']


In [33]:
df['ca_name']=ca_name.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
df['Ward']=df['Ward'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace()) else x)
df['AGE_11']=age_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace()) else x)
df['CURRENT_BUILDING_ASSMT_11']=df['CURRENT_BUILDING_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
df['CURRENT_LAND_ASSMT_11']=df['CURRENT_LAND_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x) 
df['CURRENT_TOTAL_ASSMT_11']=df['CURRENT_TOTAL_ASSMT_11'].map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)


In [34]:
cook_house_stock_properties=pd.concat([ward,chicagoflag,ca_name,ca_num,sqft_bldg_11,sqft_land_11,age_11,current_total_assmt_11,current_building_assmt_11,current_land_assmt_11],join='outer',axis=1)
chicago_house_properties=cook_house_stock_properties[ chicagoflag == 1]

In [35]:
#Drop na's
cook_house_stock_properties=cook_house_stock_properties.dropna()

In [36]:
cook_house_stock_properties?


In [37]:
cook_house_stock_properties.columns
Out [37]:
Index([Ward, ChicagoFlag, CA_name, CA_num, sqft_bldg_11, sqft_land_11, AGE_11, CURRENT_TOTAL_ASSMT_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11], dtype=object)

In [38]:
#process integers
cook_house_stock_properties['CA_num']=cook_house_stock_properties['CA_num'].map(int)
cook_house_stock_properties['sqft_bldg_11']=cook_house_stock_properties['sqft_bldg_11'].map(int)
cook_house_stock_properties['sqft_land_11']=cook_house_stock_properties['sqft_land_11'].map(int)


In [39]:
cook_house_stock_properties['CURRENT_BUILDING_ASSMT_11']=cook_house_stock_properties['CURRENT_BUILDING_ASSMT_11'].map(int)
cook_house_stock_properties['CURRENT_LAND_ASSMT_11']=cook_house_stock_properties['CURRENT_LAND_ASSMT_11'].map(int)
cook_house_stock_properties['CURRENT_TOTAL_ASSMT_11']=cook_house_stock_properties['CURRENT_TOTAL_ASSMT_11'].map(int)


In [40]:
cook_house_stock_properties.columns
Out [40]:
Index([Ward, ChicagoFlag, CA_name, CA_num, sqft_bldg_11, sqft_land_11, AGE_11, CURRENT_TOTAL_ASSMT_11, CURRENT_BUILDING_ASSMT_11, CURRENT_LAND_ASSMT_11], dtype=object)

In [ ]:
cook_house_stock_properties['CA_name']=cook_house_stock_properties['CA_name'].map(str.strip)
cook_sums=cook_house_stock_properties.groupby('CA_name').sum()

In [ ]:
cook_sums['CURRENT_TOTAL_ASSMT_11']

In [ ]:
print cook_sums['CURRENT_TOTAL_ASSMT_11'][:15]

In [ ]:
cook_sums['CURRENT_TOTAL_ASSMT_11'].plot(kind="bar",stacked='True')

In [ ]:


