
# enable GDAL/OGR Python API

import sys
import os

OSGEO_ROOT  = r'C:\OSGeo4W64'
#OSGEO_ROOT = r'C:\Progra~1\QGIS3~1.14' # C:\Program Files\QGIS 3.14

parent_directory_of_osgeo = OSGEO_ROOT + r'\apps\Python37\lib\site-packages'
parent_directory_of_gdal  = OSGEO_ROOT + r'\bin;' # gdal***.dll

sys.path.append(     parent_directory_of_osgeo)
os.environ['PATH'] = parent_directory_of_gdal + os.environ['PATH']

os.environ['GDAL_DATA']        = OSGEO_ROOT + r'\share\gdal'
os.environ['GDAL_DRIVER_PATH'] = OSGEO_ROOT + r'\bin\gdalplugins'
os.environ['GEOTIFF_CSV']      = OSGEO_ROOT + r'\share\epsg_csv'
os.environ['PROJ_LIB']         = OSGEO_ROOT + r'\share\proj'

try:
    from osgeo import ogr, osr, gdal
except:
    msg  = ' ERROR: canno tfind GDAL/OGR mudule.\n'
    msg += '        check Python version of pyd.'
    sys.exit(msg)

# reference
#    https://pcjericks.github.io/py-gdalogr-cookbook/
#    https://gdal.org/python/index.html
#    https://ujicya.jp/blog-mapping/python-gdal-api/
#    https://ujicya.jp/blog-mapping/workflow-of-python-geospatial-development/
