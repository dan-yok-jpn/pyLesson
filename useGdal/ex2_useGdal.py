
import os
import sys

with open('enableGdal.py') as f:
    exec(f.read()) # import ogr

if os.path.exists('poly4.json'):
    driver = ogr.GetDriverByName('GeoJSON')
    dataSource = driver.Open('poly4.json')
else:
    sys.exit('poly4.json not found. run ex1_useGdal first')

layer = dataSource.GetLayer()
for i, feature in enumerate(layer):
    geometry     = feature.GetGeometryRef()
    geometryType = geometry.GetGeometryType()
    geometryName = ogr.GeometryTypeToName(geometryType)
    print(' feature[{}]'.format(i))
    print( '\ttype : {}'.format(geometryName))
    if geometryName == 'Polygon':
        geom_outer = ogr.ForceToLineString(geometry)
        for j in range(geom_outer.GetPointCount()):
            point = geom_outer.GetPoint(j)
            x, y  = point[0], point[1]
            print('\tcodinates[{}] : \t{}\t{}'.format(j, x, y))

''' above scripts same below
import json

with open('poly4.json', encoding='utf-8') as f:
    data_dict = json.load(f)

for i, point in enumerate(data_dict['coordinates'][0]):
    x, y = point[0], point[1]
    print('\tcodinates[{}] : \t{}\t{}'.format(j, x, y))
'''