# LSStools-py
---
Python based functions for interacting with LSS load file format.  
This package is currently being updated semi-regularly to add new features.
---
## Install and import
To install the package first clone the repository and cd to the .whl file
```
git clone https://github.com/Hbm1g18/lsstools-py  
cd lsstools-py  
cd dist  
```  
Now install the package using pip  
```
pip install *.whl
```  
From there using the package within python can be done as follow  
```
from lsstools import *
```
---
## Examples  
Below are a few examples of using lsstools-py for obtaining quick information and other products from an LSS linework load file.  
  
```
from lsstools import *  
file = "lss_test_data/linework.001"
```
```
lssinfo(file)  
-------------
Bounding box for linework.001:
[272324.613, 345198.942, 273281.621, 345870.142]
Z-value information:
Min-z: 511.917
Max-z: 641.725
Avg-z: 576.0556438613932
Feature codes in linework.001:
['ACT', 'BB', 'BBD', 'BFC', 'BRH', 'BRK', 'BT', 'BTI', 'CB', 'CBD', 'CBL', 'CBR', 'CR', 'CRK', 'CT', 'CTI', 'L', 'LQY', 'LTI', 'QFL', 'QFR', 'RD', 'S', 'SFC', 'SRK', 'STI', 'TB', 'TK']

feature_to_dxf(file, 'brk', 'baseofrock.dxf')
---------------------------------------------
Output saved as <_io.TextIOWrapper name='baseofrock.dxf' mode='w' encoding='UTF-8'>

lss_to_csv(file, 'gcps.csv')
-----------------------------
Load file converted to CSV and saved as: gcps.csv

boundaryjson(file, 'boundary')
-------------------------------
Boundary produced and saved at: boundary.geojson

countfeature(file, 'brk')
-------------------------
162
```
---
## Functions  
See below table for full list of functions  

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
|checkfileformat()|file_path|none|Checks to see if input file is recognised load file format. Supports .001 to .009|
|read_data()|file_path|Link & Point structs|Parses load file data into appropriate structs|
|featurecodes()|file_path|List|Returns a list of unique feature codes within load file|
|boundingbox()|file_path|List [min_x, min_y, max_x, max_y]|Returns lower left and upper right bounding box based on survey data|
|z_info()|file_path|Float values: min_z, max_z, avg_z|Returns min, max and average of z-values within input file|
|lssinfo()|file_path|Prints information|Returns general information on input load file|
|querysurvey()|file_path, string|List of structs|Returns all links/points for a given feature code within load file|
|countfeature()|file_path, string|Int value|Returns total number of features with given code in load file|
|feature-to_dxf()|file_path, string, output_dir|.dxf file|Generates points/polyline DXF file of given feature code and retains 3D information|
|feature_to_geojson()|file_path, string, output_dir|.geojson file|Generates GeoJSON file for given feature code and stores 3D data as "elevation" property|
|lss_to_csv()|file_path, output_dir|.csv file|Converts all data within load file to .csv format|
|boundinggeom()|file_path|json string|Produces geojson string bounding geometry for given load file|
|convex_hull_2d()|points|list of dictionaries|Computes 2D convex hull using Andrew's monotone chain algorithm. Returns hull as list of point dictionaries.|
|hull_to_geojson()|list of point dictionaries|geojson string|Converts a list of point dictionaries and forms geojson feature collection of convex hull.|
|boundaryjson()|file_path, output_dir|.geojson file|Generates a .GeoJSON file for the convex hull of a given load file|
