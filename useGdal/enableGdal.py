
# enable GDAL/OGR Python API

import os
import sys

OSGEO_ROOT = None
for p in os.sys.path:
    P = p.upper()
    if 'OSGEO' in P or 'QGIS' in P:
        i = p[4:].index('\\')
        OSGEO_ROOT = p[: 4 + i]
        break
if OSGEO_ROOT is None:
    msg  = '\n ERROR: can not set OSGEO_ROOT.'
    msg +=          ' please edit this script.'
    sys.exit(msg)

os.environ['PATH']             = OSGEO_ROOT + '/bin;' + os.environ['PATH']
os.environ['GDAL_DATA']        = OSGEO_ROOT + '/share/gdal'
os.environ['GDAL_DRIVER_PATH'] = OSGEO_ROOT + '/bin/gdalplugins'
os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '/share/epsg_csv'
os.environ['PROJ_LIB']         = OSGEO_ROOT + '/share/proj'

try:
    from osgeo import ogr
except:
    sys.exit('\n ERROR: can not import ogr mudule.\n')

# reference
#    https://pcjericks.github.io/py-gdalogr-cookbook/
#    https://gdal.org/python/index.html
#    https://ujicya.jp/blog-mapping/python-gdal-api/
#    https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/
