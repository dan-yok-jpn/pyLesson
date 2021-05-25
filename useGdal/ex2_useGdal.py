import os
import sys
import useGdal

try:
    useGdal.setenv()
    from osgeo import ogr
except:
    sys.exit('\n ERROR: can not import ogr mudule.\n')

def info(filename):

    drivers = {
        '.geojson': 'GeoJSON',
        '.json':    'GeoJSON',
        '.shp':     'ESRI ShapeFile',
        '.kml':     'KML',
        '.sqlite':  'SQLite',
        '.gpkg':    'GPKG'
    }

    if not os.path.exists(filename):
        sys.exit('{} not found.'.format(filename))

    ext = os.path.splitext(filename)[1].lower()
    if ext in drivers:
        driver = ogr.GetDriverByName(drivers[ext])
    else:
        sys.exit("sorry, '.{}' not support".format(ext))

    dataSource = driver.Open(filename)

    layer = dataSource.GetLayer()
    for i, feature in enumerate(layer):
        geometry     = feature.GetGeometryRef()
        geometryType = geometry.GetGeometryType()
        geometryName = ogr.GeometryTypeToName(geometryType)
        print(' feature[{}]'.format(i))
        print( '\t type : {}'.format(geometryName))
        if   geometryName == 'Polygon':
            geom = ogr.ForceToLineString(geometry)
        elif geometryName == 'LineString' or \
             geometryName == 'Point':
            geom = geometry
        else:
            continue
        for j in range(geom.GetPointCount()):
            point = geom.GetPoint(j)
            x, y  = point[0], point[1]
            print('\t codinates[{}] : \t{}\t{}'.format(j, x, y))

if __name__ == '__main__':

    if len(sys.argv) == 2:
        info(sys.argv[1])
