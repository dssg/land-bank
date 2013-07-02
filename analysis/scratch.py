# age_11_nospace_nona=age_11_nospace.dropna()
# age_11_nospace_nona_int=age_11_nospace_nona.map(int)
# age_11_nospace_nona_int.mean()
# age_11_nospace=age_11.map(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
#attic_desc_11=attic_desc_11.str.strip()
attic_desc_11[:10]

current_building_assmt_11=current_building_assmt_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
current_land_assmt_11=current_land_assmt_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x) 
current_total_assmt_11=current_total_assmt_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)

# current_building_assmt_11_nona=current_building_assmt_11.dropna()
# current_land_assmt_11_nona=current_land_assmt_11.dropna()
# current_total_assmt_11_nona=current_total_assmt_11.dropna()


# current_building_assmt_11_nona_int=current_building_assmt_11_nona.map(int)
# current_land_assmt_11_nona_int=current_land_assmt_11_nona.map(int)
# current_total_assmt_11_nona_int=current_total_assmt_11_nona.map(int)
ext_desc_11=ext_desc_11.map(str.strip)
garage_desc_11=garage_desc_11.map(str.strip)
sqft_bldg_11=sqft_bldg_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
#sqft_bldg_11=sqft_bldg_11.dropna()
#sqft_bldg_11=sqft_bldg_11.map(int)
sqft_land_11=sqft_land_11.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
ca_num=ca_num.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)
ca_name=ca_name.map(str.strip)

attic_desc_11=attic_desc_11.map(str.strip)
basement_desc_11=basement_desc_11.map(str.strip)
class_description_11=class_description_11.map(str.strip)
chicagoflag=chicagoflag.map(lambda x: np.nan if isinstance(x, basestring) and (x.isspace() or (x == 'LETTER PROPERTY')) else x)

ward
ward.plot(kind='bar',stacked=True)
cook_house_stock_properties[:10]

chicago_house_properties=cook_house_stock_properties[ chicagoflag == 1]
chicago_house_properties_nona=chicago_house_properties.dropna()


cook_house_stock_properties[:10]
xoca_num[:10]



cook_house_stock_properties['CA_name'].count()
chicago_house_properties['Ward'].count()
chicago_house_properties[:10]
chicago_house_properties_nona['Ward'].count()

chicago_house_properties_nona.columns
chicago_house_properties_nona['CA_num']=chicago_house_properties_nona['CA_num'].map(int)
chicago_house_properties_nona['sqft_bldg_11']=chicago_house_properties_nona['sqft_bldg_11'].map(int)
chicago_house_properties_nona['sqft_land_11']=chicago_house_properties_nona['sqft_land_11'].map(int)
chicago_house_properties_nona['CURRENT_TOTAL_ASSMT_11']=chicago_house_properties_nona['CURRENT_TOTAL_ASSMT_11'].map(int)
chicago_house_properties_nona['CURRENT_BUILDING_ASSMT_11']=chicago_house_properties_nona['CURRENT_BUILDING_ASSMT_11'].map(int)
chicago_house_properties_nona['CURRENT_LAND_ASSMT_11']=chicago_house_properties_nona['CURRENT_LAND_ASSMT_11'].map(int)


chicago_house_properties_ward_counts=chicago_house_properties_nona.groupby('Ward').count()
chicago_house_properties_ward_counts[:10]
#chicago_house_properties_ward_counts=chicago_house_properties_nona.groupby('Ward').count()
chicago_house_properties_ward_means=chicago_house_properties_nona.groupby('Ward').mean()
# chicago_house_properties_ward_median=chicago_house_properties_nona.median()
# chicago_house_properties_ward_std=chicago_house_properties_nona_std.std()

chicago_house_properties_ward_means[:10]
chicago_house_properties_ward_means
chicago_house_properties_nona_46=chicago_house_properties_nona[chicago_house_properties_nona['Ward'] == 46]
chicago_house_properties_nona_46['Ward'].count()
chicago_house_properties_nona_46[:10]
cook_house_stock_properties.groupby('ca_name').mean()
cook_house_stock_properties.groupby('ca_name').median()
import matplotlib.pyplot as plt


ward.corr(tot_val)

df.corr()
