# Abandoned property analytics tool

<a href="http://cookcountylandbank.org"><img src="http://dssg.io/img/partners/landbank.jpg" width="400" align="right"></a>

An analytics tool to help the Cook County Land Bank acquire vacant and abandoned properties strategically.

This project is a part of the 2013 [Data Science for Social Good](http://www.dssg.io) fellowship, in partnership with the [Cook County Land Bank](http://www.cookcountylandbank.org) and [DePaul University Institute for Housing Studies](http://www.housingstudies.org/).

*For a quick and gentle overview of the project, check out our [blog post](http://dssg.io/2013/07/11/cook-county-land-bank.html).*

## The problem: vacant and abandoned property
Parts of Cook County have long struggled with vacancy and abandonment, but the recent foreclosure crisis spread these problems into areas which had previously experienced relative stability. 
Many of the properties that went into foreclosure ended up becoming vacant because the residents would abandon the property long before the foreclosure process was completed. 

These abandoned homes can lower property values, serve as magnets for crime and decay, and reduce tax revenues.

**[Read more about the abandoned property problem on our blog](http://dssg.io/2013/07/11/cook-county-land-bank.html)**


## The solution: analytics web tool to target properties
The Cook County Land Bank Authority (CCLBA) was created in January 2013 with the goal of returning these properties to productive use. The agency won't have the resources to invest in every property, and the appropriate policy strategies from community to community.

![web app screenshot](https://raw.github.com/dssg/dssg.github.io/master/img/posts/land-bank-screenshot.png)

Our purpose was to create a web tool to view and understand Cook County's property data, and to analyze it in order to help the CCLBA develop its policy strategies.

1. Build a usable web interface for both public use and for use by land bank employees that interfaces with a Postgres database in order to organize, query, and access the data in a convenient manner.
2. Create a model that will determine the critera by which the Cook County Land Bank which neighborhoods to help first, which properties in that neighborhood, and their potential new uses.

**[Read more about our analysis in the wiki](../../wiki/Analysis)**

## The data: property and building data from Cook County and the City of Chicago
- Property data from the Cook County Assessor and Recorder of Deeds, courtsety of the Institute for Housing Studies
- Cook County parcel shapefile from County GIS department
- City of Chicago open data portal datasets
- ACS demographic data from the Census Bureau
- Brownfield data from the EPA

**[Read more about the data we used in the wiki](../../wiki/Data)**

## Project layout
- `analysis`: exploratory data analsys of real estate and demographic tends in Cook County
- `web`: a django app that implements the analy

## Installation guide

Here's the software you'll need to install:

- GIS software: ArcGIS 10.1 or QGIS
- Postgres 9.1
- PostGIS
- Python 2.7.x
- Numpy  1.7.1
- Sympy  0.7.2

Next, clone the repository and configure Django to enable South and TastyPie, and to interface with your Postgres database.

Then, run an initial South migration to create database tables/views:

```
$ python manage.py schemamigration landbank_data --initial
$ python manage.py migrate landbank_data
```


Finally, modify and run load_*.py scripts with desired input files to populate base tables.

## Contributing to the project
To get involved, please check the [issue tracker](https://github.com/dssg/bikeshare/issues).

To get in touch, email Tom Plagge at tplagge@gmail.com.

## License 

Copyright (C) 2013 [Data Science for Social Good Fellowship at the University of Chicago](http://dssg.io)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
