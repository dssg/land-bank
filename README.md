#DSSG Cook County Land Bank Project

####Goals
1. Build a usable web interface for both public use and for use by land bank employees that interfaces with a Postgres database in order to organize, query, and access the data in a convenient manner.
2. Create a model that will determine the critera by which the Cook County Land Bank which neighborhoods to help first, which properties in that neighborhood, and their potential new uses.

####Data
- Institute for Housing Studies (IHS) at DePaul University datasets
- Cook County Assessor file
- County shapefile

####Required Software
- GIS software: ArcGIS 10.1 or QGIS
- Postgres 9.1
- PostGIS
- Python 2.7.x
- Numpy  1.7.1
- Sympy  0.7.2

####Setup
- Install Postgres and PostGIS
- Clone the repository and configure Django to enable South and TastyPie, and to interface with your Postgres database.
- Run an initial South migration to create database tables/views:

```
$ python manage.py schemamigration landbank_data --initial
$ python manage.py migrate landbank_data
```


- Modify and run load_*.py scripts with desired input files to populate base tables.

####Our Partners
- DePaul University Institute for Housing Studies 
- The Cook County Land Bank Authority & Board of Directors
- Cook County Commisioner's office
