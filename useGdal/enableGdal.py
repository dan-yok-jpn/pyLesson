
# enable GDAL/OGR Python API

import os
import sys

OSGEO_ROOT  = 'C:/OSGeo4W64'

os.environ['PATH']             = OSGEO_ROOT + '/bin;' + os.environ['PATH']
os.environ['GDAL_DATA']        = OSGEO_ROOT + '/share/gdal'
os.environ['GDAL_DRIVER_PATH'] = OSGEO_ROOT + '/bin/gdalplugins'
os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + '/share/epsg_csv'
os.environ['PROJ_LIB']         = OSGEO_ROOT + '/share/proj'

try:
    from osgeo import ogr
except:
    msg  = '\n ERROR: can not find GDAL/OGR mudule.\n'
    msg += '          check Python version of pyd.'
    sys.exit(msg)

# reference
#    https://pcjericks.github.io/py-gdalogr-cookbook/
#    https://gdal.org/python/index.html
#    https://ujicya.jp/blog-mapping/python-gdal-api/
#    https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/
