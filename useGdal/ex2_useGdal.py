import os
import sys

with open('enableGdal.py') as f:
    exec(f.read()) # import ogr

def info(filename):

    drivers = {
        '.geojson': 'GeoJSON',
        '.json':    'GeoJSON',
        '.shp':     'ESRI ShapeFile',
        '.kml':     'KML',
        '.sqlite':  'SQLite',
        '.gpkg':    'GPKG'
    }

    if os.path.exists(filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext in drivers:
            driver = ogr.GetDriverByName(drivers[ext])
        else:
            sys.exit("sorry, '.{}' not support".format(ext))
        dataSource = driver.Open(filename)
    else:
        sys.exit('{} not found.'.format(filename))

    layer = dataSource.GetLayer()
    for i, feature in enumerate(layer):
        geometry     = feature.GetGeometryRef()
        geometryType = geometry.GetGeometryType()
        geometryName = ogr.GeometryTypeToName(geometryType)
        print(' feature[{}]'.format(i))
        print( '\ttype : {}'.format(geometryName))
        if   geometryName == 'Polygon':
            geom = ogr.ForceToLineString(geometry)
        elif geometryName == 'Point':
            geom = geometry
        else:
            continue
        for j in range(geom.GetPointCount()):
            point = geom.GetPoint(j)
            x, y  = point[0], point[1]
            print('\tcodinates[{}] : \t{}\t{}'.format(j, x, y))

if __name__ == '__main__':

    if len(sys.argv) == 2:
        info(sys.argv[1])
