# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CensusTract'
        db.create_table(u'landbank_data_censustract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geoid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('commarea', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('loc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=3435)),
        ))
        db.send_create_signal('landbank_data', ['CensusTract'])

        # Deleting field 'SummaryStats.total_assmt_med'
        db.delete_column(u'landbank_data_summarystats', 'total_assmt_med')

        # Deleting field 'SummaryStats.bldg_assmt_var'
        db.delete_column(u'landbank_data_summarystats', 'bldg_assmt_var')

        # Deleting field 'SummaryStats.land_assmt_var'
        db.delete_column(u'landbank_data_summarystats', 'land_assmt_var')

        # Deleting field 'SummaryStats.bldg_assmt_med'
        db.delete_column(u'landbank_data_summarystats', 'bldg_assmt_med')

        # Deleting field 'SummaryStats.total_assmt_var'
        db.delete_column(u'landbank_data_summarystats', 'total_assmt_var')

        # Deleting field 'SummaryStats.land_assmt_med'
        db.delete_column(u'landbank_data_summarystats', 'land_assmt_med')


    def backwards(self, orm):
        # Deleting model 'CensusTract'
        db.delete_table(u'landbank_data_censustract')

        # Adding field 'SummaryStats.total_assmt_med'
        db.add_column(u'landbank_data_summarystats', 'total_assmt_med',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'SummaryStats.bldg_assmt_var'
        db.add_column(u'landbank_data_summarystats', 'bldg_assmt_var',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'SummaryStats.land_assmt_var'
        db.add_column(u'landbank_data_summarystats', 'land_assmt_var',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'SummaryStats.bldg_assmt_med'
        db.add_column(u'landbank_data_summarystats', 'bldg_assmt_med',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'SummaryStats.total_assmt_var'
        db.add_column(u'landbank_data_summarystats', 'total_assmt_var',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'SummaryStats.land_assmt_med'
        db.add_column(u'landbank_data_summarystats', 'land_assmt_med',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


    models = {
        'landbank_data.assessor': {
            'Meta': {'object_name': 'Assessor'},
            'attic_desc': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'basement_desc': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'chicago_flag': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'class_desc': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'current_building_assmt': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'current_land_assmt': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'current_total_assmt': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'estim_hunit': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ext_desc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'garage_desc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'pt_type1_cat': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ptype': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'sqft_bldg': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sqft_land': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'type_pt_2_4': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_pt_5': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_pt_condo': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_pt_nonres': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_pt_sf': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_pt_unknown': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ward': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_built': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'landbank_data.auction': {
            'Meta': {'object_name': 'Auction'},
            'addr_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'adj_yd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'adj_yq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'apt': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'buyer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'buyer_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'date_doc': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_rec': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'doc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'reo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'residential': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'seller': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'seller_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yeard': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'yq_doc': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'landbank_data.cashfin': {
            'Meta': {'object_name': 'CashFin'},
            'addr_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'amount_prime': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'apt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'buyer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'buyer_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'date_doc': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_rec': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'doc': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'likely_cash': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'likely_distressed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'residential': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'seller': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'seller_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'landbank_data.censustract': {
            'Meta': {'object_name': 'CensusTract'},
            'commarea': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geoid': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3435'})
        },
        'landbank_data.foreclosure': {
            'Meta': {'object_name': 'Foreclosure'},
            'addr_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'adj_yd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'adj_yq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'apt': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'case_num1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'case_num2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'case_num3': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'city_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'date_doc': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_rec': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'defendant_first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'defendant_last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'filing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'plaintiff': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'residential': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yeard': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'yq_doc': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'landbank_data.mortgage': {
            'Meta': {'object_name': 'Mortgage'},
            'addr_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'adj_yd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'adj_yq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'apt': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'borrower1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'borrower1_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'date_doc': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_rec': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'doc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lender1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'lender1_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'lender2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'lender2_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mort_amt': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'residential': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yeard': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'yq_doc': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'landbank_data.scavenger': {
            'Meta': {'object_name': 'Scavenger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'tax_amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'tax_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'tax_year': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'total_amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'township': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'})
        },
        'landbank_data.summarystats': {
            'Meta': {'object_name': 'SummaryStats'},
            'area_id': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'area_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'bldg_assmt_avg': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3435', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_assmt_avg': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ptype_2_4': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ptype_5': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ptype_condo': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ptype_nonres': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ptype_sf': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'ptype_unknown': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'total_assmt_avg': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'landbank_data.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'addr_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'adj_yd': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'adj_yq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'amount_prime': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'apt': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'business_buyer': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buyer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'buyer_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'ca_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ca_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city_final': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'date_doc': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_rec': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'doc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'gisdate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'houseno': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loc': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3435', 'null': 'True'}),
            'long_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'no_tract_info': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'non_condo': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_index': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'purchase_less_20k': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'residential': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'seller': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'seller_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'tract_fix': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yeard': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'yq_doc': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['landbank_data']