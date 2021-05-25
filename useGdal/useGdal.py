import os
import sys

def setenv():
	OSGEO_ROOT = None
	for p in os.sys.path:
		P = p.upper()
		if 'OSGEO' in P or 'QGIS' in P:
			i = p[4:].index('\\') # windows
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
