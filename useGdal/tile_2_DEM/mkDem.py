
from gdal_env import gdal_env
gdal_env() # add DLL directory

import os
import sys
import csv
import requests
import math
import numpy as np
from osgeo import gdal, ogr, osr
from tqdm import tqdm

nodata = -1

def usage():
  msg = '''
Create DEM from elevation-tile

 python {} [(-h|--help)] (lat_sw lng_sw lat_ne lng_ne | poly) [output]

  options
   lat_sw : latitude of south-west corner in degree
   lng_sw : longitude of south-west corner in degree
   lat_ne : latitude of north-east corner in degree
   lng_ne : longitude of north-east corner in degree
   poly   : GIS data for shape of watershed (format : GeoJSON, CS : WGS84)
   output : output file name. default 'dem.tif'
   -h     : show this help'''.\
  format(os.path.basename(sys.argv[0]))
  sys.exit(msg)

def bbox(file_input):

  dataSource = ogr.Open(file_input)
  layer      = dataSource.GetLayer(0)
  feature    = layer.GetFeature(0)
  geometry   = feature.GetGeometryRef()
  envelope   = geometry.GetEnvelope()

  return envelope

def tile(lat_deg, lon_deg, n):

  lat_rad = math.radians(lat_deg)
  xtile = int(n * (lon_deg + 180) / 360)
  ytile = int(n * (1 - math.log(math.tan(lat_rad) +
            (1 / math.cos(lat_rad))) / math.pi) / 2)

  return xtile, ytile

def latlng(xtile, ytile, n):

  lon_deg = 360 * xtile / n - 180
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)

  return lat_deg, lon_deg

def Dem15(raster, i0, j0, url_pre, tx, ty):

  getAll = True
  r = requests.get(url_pre + '{}/{}.txt'.format(tx, ty))
  if not r.status_code == requests.codes.ok:
    return False
  dem = list(csv.reader(r.text.splitlines()))
  for p in range(256):
    i = i0 + p
    for q in range(256):
      s = dem[p][q]
      if s == 'e':
        getAll = False
      else:
        j = j0 + q
        if raster[i][j] == nodata:
          raster[i][j] = float(s)

  return getAll

def Dem14(raster, i0, j0, url_pre, tx15, ty15):

  getAll = True
  tx, ty = tx15 // 2, ty15 // 2
  r = requests.get(url_pre + '{}/{}.txt'.format(tx, ty))
  if not r.status_code == requests.codes.ok:
    return False
  dem = list(csv.reader(r.text.splitlines()))
  ls = range(128) if tx == tx15 / 2 else range(128, 256)
  for p in ls:
    i = i0 + 2 * (p % 128)
    k = i + 1
    for q in ls:
      j = j0 + 2 * (q % 128)
      l = j + 1
      s = dem[p][q]
      if s == 'e':
        getAll = False
      else:
        v = float(s)
        if raster[i][j] == nodata: raster[i][j] = v
        if raster[i][l] == nodata: raster[i][l] = v
        if raster[k][j] == nodata: raster[k][j] = v
        if raster[k][l] == nodata: raster[k][l] = v

  return getAll

def main(lat_sw, lng_sw, lat_ne, lng_ne, dst):

  zoom = 15
  n = math.pow(2, zoom)
  txmin, tymax = tile(lat_sw, lng_sw, n)
  txmax, tymin = tile(lat_ne, lng_ne, n)

  ntx, nty = txmax - txmin + 1, tymax - tymin + 1
  hsize, vsize = 256 * ntx, 256 * nty
  raster = np.full((vsize, hsize), nodata, dtype = np.float64)

  url5a = 'http://cyberjapandata.gsi.go.jp/xyz/dem5a/15/' # airbone lidar
  url5b = 'http://cyberjapandata.gsi.go.jp/xyz/dem5b/15/' # photogrammetry (@20cm)
  url5c = 'http://cyberjapandata.gsi.go.jp/xyz/dem5c/15/' # photogrammetry (@40cm)
  url10 = 'http://cyberjapandata.gsi.go.jp/xyz/dem/14/'   # contour lines of map

  print()
  bar = tqdm(total = ntx * nty)
  for i, ty in enumerate(range(tymin, tymax + 1)):
    i0 = 256 * i
    for j, tx in enumerate(range(txmin, txmax + 1)):
      j0 = 256 * j 

      getAll = Dem15(raster, i0, j0, url5a, tx, ty)
      if not getAll:
        getAll = Dem15(raster, i0, j0, url5b, tx, ty)
        if not getAll:
          getAll = Dem15(raster, i0, j0, url5c, tx, ty)
          if not getAll:
            getAll = Dem14(raster, i0, j0, url10, tx, ty)
    bar.update(ntx)

  lat0, lng0 = latlng(txmin,     tymin,     n) # north-west corner of DEM
  lat1, lng1 = latlng(txmax + 1, tymax + 1, n) # south-east corner of DEM
  trans = [lng0, (lng1 - lng0) / hsize, 0 , lat0, 0, (lat1 - lat0) / vsize]

  srs = osr.SpatialReference()
  srs.ImportFromEPSG(4326)
  driver = gdal.GetDriverByName('GTiff')
  gtif = driver.Create(dst, hsize, vsize, 1, gdal.GDT_Float32)
  gtif.GetRasterBand(1).WriteArray(raster)
  gtif.GetRasterBand(1).SetNoDataValue(nodata)
  gtif.SetGeoTransform(trans)
  gtif.SetProjection(srs.ExportToWkt())
  gtif.FlushCache()

if __name__ == '__main__':

  # main(35.2715777, 139.0034392, 35.3530003, 139.1633717, 'dem.tif')

  if '-h' in sys.argv or '--help' in sys.argv:
    usage()

  try:
    if type(sys.argv[1]) is str:
      lng_sw, lng_ne, lat_sw, lat_ne = bbox(sys.argv[1])
      dst = sys.argv[2] if len(sys.argv) == 6 else 'dem.tif'
    else:
      lat_sw, lng_sw = float(sys.argv[1]), float(sys.argv[2])
      lat_ne, lng_ne = float(sys.argv[3]), float(sys.argv[4])
      dst = sys.argv[5] if len(sys.argv) == 6 else 'dem.tif'
    main(lat_sw, lng_sw, lat_ne, lng_ne, dst)
  except:
    print('ERROR Invalid argument\n', file = sys.stderr)
    usage()