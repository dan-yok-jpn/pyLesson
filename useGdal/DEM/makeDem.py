# coding:utf-8

import os
import sys
import re
import glob
import subprocess

# https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-G04-d.html

try:
    from gdal_env import gdal_env
    my_env = gdal_env()
    from osgeo import ogr
except:
    sys.exit('\n could not import osgeo.')

def getDriverFromExtension(filename):
    ext = os.path.splitext(filename)[1].upper()
    if ext in ('.JSON', '.GEOJSON'):
        return 'GeoJSON'
    elif ext == '.SHP':
        return 'ESRI ShapeFile'
    return None

def rectangle(xmin, ymin, xmax, ymax):
    pts = ogr.Geometry(ogr.wkbLinearRing)
    pts.AddPoint(xmin, ymin)
    pts.AddPoint(xmin, ymax)
    pts.AddPoint(xmax, ymax)
    pts.AddPoint(xmax, ymin)
    pts.AddPoint(xmin, ymin)
    geom = ogr.Geometry(ogr.wkbPolygon)
    geom.AddGeometry(pts)
    return geom

def main(basinFile, demFiles):

    driverName = getDriverFromExtension(basinFile)
    if driverName is not None:
        ds = ogr.GetDriverByName(driverName).Open(basinFile)
    else:
        fmt = '{} is not GeoJSON and is not ShapeFile also'
        sys.exit('fmt'.format(basinFile))

    if os.path.exists('dem.tif'): os.remove('dem.tif')

    batch = open('tmp.bat', 'w')
    bin  = my_env.OSGEO_ROOT + "\\bin;"
    bin += my_env.OSGEO_ROOT + "\\apps\\Python37"
    print('@echo off\nsetlocal\nset path={}'.format(bin), file=batch)

    layer  = ds.GetLayer()
    extent = layer.GetExtent()
    basin  = rectangle(extent[0], extent[2], extent[1], extent[3])

    dx,  dy  = 1 / 320., 1 / 480. # 5th order mesh (resolution approx. 250 m)
    dx_, dy_ = dx - 1e-8, dy - 1e-8
    files = []
    for demFile in demFiles:

        mesh  = re.search('_[0-9]+-', demFile)[0][1:5]   # 1st order mesh
        south = float(int(mesh[:2]) / 1.5 + 1e-8)        #  (resolution approx. 80 km)
        west  = float(mesh[2:]) + 100

        xmin = max(extent[0], west)
        xmax = min(extent[1], west  + 1.0)
        ymin = max(extent[2], south)
        ymax = min(extent[3], south + 4.0 / 6)
        xmin = int( xmin / dx ) * dx
        xmax = int((xmax + dx_) / dx) * dx # just inside
        ymin = int( ymin / dy ) * dy
        ymax = int((ymax + dy_) / dy) * dy

        cell = rectangle(xmin, ymin, xmax, ymax)
        if cell.Intersects(basin) is None: continue

        dst  = mesh + '.tif'
        cmd  = 'gdal_rasterize -of GTiff -a_srs EPSG:4612 -q '
        cmd += '-l G04-d-11_{}'.format(mesh)
        cmd += '-jgd_ElevationAndSlopeAngleFifthMesh -a G04d_002 '
        cmd += '-tr {} {} '.format(dx, dy)
        cmd += '-te {} {} {} {} '.format(xmin, ymin, xmax, ymax)
        cmd += '/vsizip/G04-d-11_{}-jgd_GML.zip/'.format(mesh)
        cmd += 'G04-d-11_{}-jgd_ElevationAndSlopeAngleFifthMesh.shp '.format(mesh)
        cmd += '{}'.format(dst)
        print(cmd, file=batch)
        files.append(dst)

    cmd = 'python {} -q -o dem.tif'.format(
        my_env.OSGEO_ROOT + "\\apps\\Python37\\Scripts\\gdal_merge.py"
    )
    for f in files: cmd += ' ' + f
    print(cmd, file=batch)
    batch.close()

    cp = subprocess.run('tmp.bat', shell=True)
    if cp.returncode == 0:
        print('\n dem.tif was created', file=sys.stderr)
    else:
        print('\n dem.tif was NOT created', file=sys.stderr)

    os.remove('tmp.bat')
    for f in reversed(files):
        os.remove(f)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('\n Usage : python {} dataset_of_basin'.format(sys.argv[0]))

    basinFile = sys.argv[1]
    demFiles  = glob.glob('G04-d-11_*-jgd_GML.zip')

    main(basinFile, demFiles)