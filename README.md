#DSSG Cook County Land Bank Project

<a href="http://cookcountylandbank.org"><img src="http://dssg.io/img/partners/landbank.jpg" width="350" align="right"></a>

An analytics tool to help the Cook County Land Bank acquire vacant and abandoned properties strategically.

This project is a part of the 2013 [Data Science for Social Good](http://www.dssg.io) fellowship, in partnership with the [Cook County Land Bank](http://www.cookcountylandbank.org) and [DePaul University Institute for Housing Studies](http://www.housingstudies.org/).

### The problem: vacant and abandoned property

### The solution: analytics web tool to target properties
1. Build a usable web interface for both public use and for use by land bank employees that interfaces with a Postgres database in order to organize, query, and access the data in a convenient manner.
2. Create a model that will determine the critera by which the Cook County Land Bank which neighborhoods to help first, which properties in that neighborhood, and their potential new uses.

### The data: property and building data from Cook County and the City of Chicago
- Property data from the Cook County Assessor and Recorder of Deeds, courtsety of the Institute for Housing Studies
- Cook County parcel shapefile from County GIS department
- City of Chicago open data portal datasets
- ACS demographic data from the Census Bureau
- Brownfield data from the EPA

### Project layout
Coming soon!

### Installation guide

1. Here's the software you'll need to install:

- GIS software: ArcGIS 10.1 or QGIS
- Postgres 9.1
- PostGIS
- Python 2.7.x
- Numpy  1.7.1
- Sympy  0.7.2

2.  Next, clone the repository and configure Django to enable South and TastyPie, and to interface with your Postgres database.
3.  Run an initial South migration to create database tables/views:

```
$ python manage.py schemamigration landbank_data --initial
$ python manage.py migrate landbank_data
```


4. Modify and run load_*.py scripts with desired input files to populate base tables.
