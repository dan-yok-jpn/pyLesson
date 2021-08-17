# https://mattbartos.com/pysheds/extract-river-network.html

from gdal_env import gdal_env
gdal_env() # add DLL path

import os
import sys
import fiona
from pysheds.grid import Grid

def usage():
    msg = '''
 Output polygon showing watershed from DEM

  python {} [(-h|--help)] lat lng [-i dem] [-n name]

  options
    lat :  latitude of lower-end point
    lng :  longitude of lower-end point
    name : place name of lower-end point (defalut: 'watershed')
           if name is 'foo', output polygon to 'foo.sqlite'
    dem:   file name of DEM (default: 'dem.tif')
    -h, --help : show this help'''.\
    format(os.path.basename(sys.argv[0]))
    sys.exit(msg)

def main(lat, lng, dem, name):

    grid = Grid.from_raster(dem, data_name = 'dem')
    grid.resolve_flats(data = 'dem', out_name = 'inflated_dem')
    grid.flowdir('inflated_dem', out_name = 'dir')
    grid.catchment(
        data = 'dir',
        x = lng, y = lat,
        out_name = 'catch',
        recursionlimit = 15000,
        xytype = 'label')
    grid.clip_to('catch')
    shapes = grid.polygonize()
    schema = {'geometry': 'Polygon'}

    poly = name + '.sqlite'
    if os.path.exists(poly):
        os.remove(poly)
    with fiona.open(
            poly, 'w',
            driver = 'SQLite',
            crs = grid.crs.srs,
            schema = schema) as c:
        i = 0
        for shape, _ in shapes:
            rec = {}
            rec['geometry'] = shape
            rec['id'] = str(i)
            c.write(rec)
            i += 1

if __name__ == '__main__':

    # main(35.303004, 139.124508, 'dem.tif', 'karikawa')
    # main(35.277783871786454, 139.15876290356965, 'dem.tif', 'karikawa-bashi')

    if '-h' in sys.argv or '--help' in sys.argv:
        usage()

    if len(sys.argv) == 1:
        main(32.73750, -97.294167, 'dem-sample.tif', 'catchment')
        sys.exit()

    dem, name = 'dem.tif', 'watershed'
    lat, lng = float(sys.argv[1]), float(sys.argv[2])
    if '-i' in sys.argv:
        dem  = sys.argv[sys.argv.index('-i') + 1]
    if '-i' in sys.argv:
        name = sys.argv[sys.argv.index('-n') + 1]

    main(lat, lng, dem, name)
