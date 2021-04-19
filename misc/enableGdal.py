
# enable GDAL/OGR Python API

import sys
import os

OSGEOW_ROOT  = r'C:\OSGeo4W64'
#OSGEOW_ROOT = r'C:\Progra~1\QGIS3~1.14' # C:\Program Files\QGIS 3.14
PYTHONPATH   = OSGEOW_ROOT + r'\apps\Python37'

sys.path.append(PYTHONPATH + r'\lib\site-packages')
os.environ['GDAL_DATA']         = OSGEOW_ROOT + r'\share\gdal'
os.environ['GDAL_DRIVER_PATH']  = OSGEOW_ROOT + r'\bin\gdalplugins'
os.environ['GEOTIFF_CSV']       = OSGEOW_ROOT + r'\share\epsg_csv'
os.environ['PROJ_LIB']          = OSGEOW_ROOT + r'\share\proj'
os.environ['PATH']              = OSGEOW_ROOT + r'\bin;' \
                                + PYTHONPATH  +      ';' \
                                + os.environ['PATH']

from osgeo import ogr, osr, gdal

# reference
#    https://pcjericks.github.io/py-gdalogr-cookbook/
#    https://gdal.org/python/index.html
#    https://ujicya.jp/blog-mapping/python-gdal-api/
#    https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/
