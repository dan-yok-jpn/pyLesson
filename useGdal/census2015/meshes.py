# encoding:utf-8

import os
import sys
import numpy as np
import sqlite3

try:
    from gdal_env import gdal_env
    gdal_env()
    from osgeo import ogr
except:
    sys.exit('\n ERROR: can not import ogr mudule.\n')

deltas = None

def usage():

    f = sys.stderr
    f.write('\n Create a database of regional mesh code that covers the basin\n')
    f.write('\n Usage : python {0} [Options] file_input \n'\
        .format(os.path.basename(__file__)))
    f.write('''
 Options :
   -# : order of regional mesh (range : 1-5, default : 5)
   -g, --geometry : output meshes by GeoJSON format (defalut : False)
   -q, --quiet : show nothing to console (defalut : False)
   -db_off : not create database (default : False)
   -h, --help : show this help

 file_input :
   GeoJSON format polygon dada (CRS : JGD2000 or JGS2011)''')

    sys.exit(1)

def parseArgs():

    help = ' please run with option -h or --help.'
    argc = len(sys.argv)
    if argc == 1 or '-h' in sys.argv or '--help' in sys.argv:
        usage()

    i, order, file_input = 1, 5, ''
    geom, quiet, db_on = False, False, True
    while i < argc:
        opt = sys.argv[i]
        if opt[:1] == '-':
            if   opt == '-g' or opt == '--geometry':
                geom = True
            elif opt == '-q' or opt == '--quiet':
                quiet = True
            elif opt == '-db_off':
                db_on = False
            else:
                try:
                    order = int(opt[1:])
                    if not order in range(1, 6):
                        sys.exit('\n order must be in range 1 to 5.' + help)
                except: 
                    sys.exit('\n `{0}` no such option.'.format(opt) + help)
        else:
            file_input = opt
        i += 1

    if file_input == '':
        sys.exit('\n No path to file specified.' + help)
    elif not os.path.exists(file_input):
        sys.exit('\n {0} no such file.'.format(file_input) + help)

    return file_input, order, geom, quiet, db_on

def Delta():

    deltas = np.ndarray((5, 2))
    deltas[0] = [1, 40 / 60.]    # 1st 80km
    deltas[1] = deltas[0] /  8    # 2nd 10km
    deltas[2] = deltas[1] / 10    # 3rd  1km
    deltas[3] = deltas[2] /  2    # 4th 500m
    deltas[4] = deltas[3] /  2    # 5th 250m
    return deltas

def lonlat_2_mesh(lon, lat, order):

    (lonDiv, lonMod) = divmod(lon - 100 + 1e-9, deltas[0][0])
    (latDiv, latMod) = divmod(lat       + 1e-9, deltas[0][1])
    mesh = '{:2d}{:2d}'.format(int(latDiv), int(lonDiv))

    for i in range(1, order):
        (lonDiv, lonMod) = divmod(lonMod, deltas[i][0])
        (latDiv, latMod) = divmod(latMod, deltas[i][1])
        if i < 3:
            mesh += '{:1d}{:1d}'.format(int(latDiv), int(lonDiv))
        else:
            if latDiv < 1: mesh += '1' if lonDiv < 1 else '2'
            else:          mesh += '3' if lonDiv < 1 else '4'

    return mesh

def mesh_2_lonlat(mesh):

    w = [0] * 10
    for i, c in enumerate(mesh): w[i] = int(c)

    lon, lat = 100, 0
    if w[9] != 0:
        if w[9] % 2: lon += deltas[4][0]
        if w[9] > 2: lat += deltas[4][1]
    if w[8] != 0:
        if w[8] % 2: lon += deltas[3][0]
        if w[8] > 2: lat += deltas[3][1]
    lon += w[5] * deltas[1][0] + w[7] * deltas[2][0]
    lat += w[4] * deltas[1][1] + w[6] * deltas[2][1]
    lon += (w[2] * 10 + w[3]) * deltas[0][0]
    lat += (w[0] * 10 + w[1]) * deltas[0][1]

    return (lon, lat)

def main():

    file_input, order, geom, quiet, db_on = parseArgs()

    global deltas
    deltas = Delta()

    dataSource = ogr.Open(file_input)
    layer      = dataSource.GetLayer(0)
    feature    = layer.GetFeature(0)
    geometry   = feature.GetGeometryRef()
    envelope   = geometry.GetEnvelope()

    lonStep = deltas[order - 1][0]
    latStep = deltas[order - 1][1]
    lonMin  = lonStep * int(envelope[0] / lonStep)
    lonMax  = lonStep * int(envelope[1] / lonStep + 1)
    latMin  = latStep * int(envelope[2] / latStep)
    latMax  = latStep * int(envelope[3] / latStep + 1)

    hasTbl = False
    if db_on:
        dbname = 'temp.db'
        tbname = 'mesh{}'.format(order)
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        cur.execute("select * from sqlite_master where type='table'")

        tables = [columns[1] for columns in cur.fetchall()]
        for table in tables:
            if table == tbname:
                hasTbl = True
                break

        if not hasTbl:
            cur.execute('drop table if exists {}'.format(tbname))
            cur.execute('''
                CREATE TABLE {} (
                    code TEXT PRIMARY KEY
                )'''.format(tbname))

    if geom:
        fName = tbname + '_' + file_input
        outDriver = ogr.GetDriverByName('GeoJSON')
        outDataSource = outDriver.CreateDataSource(fName)
        outLayer = outDataSource.CreateLayer('meshes', geom_type=ogr.wkbPolygon)
        idField = ogr.FieldDefn("code", ogr.OFTString)
        outLayer.CreateField(idField)
        featureDefn = outLayer.GetLayerDefn()
        outFeature = ogr.Feature(featureDefn)

    fmt  = 'POLYGON (({:.6f} {:.6f},{:.6f} {:.6f},{:.6f} {:.6f},'
    fmt +=           '{:.6f} {:.6f},{:.6f} {:.6f}))'
    for ys in np.arange(latMin, latMax, latStep):
        yn = ys + latStep
        for xw in np.arange(lonMin, lonMax, lonStep):
            xe = xw + lonStep
            wkt = fmt.format(xw, ys, xe, ys, xe, yn, xw, yn, xw, ys)
            cell = ogr.CreateGeometryFromWkt(wkt)
            if cell.Intersects(geometry):
                code = lonlat_2_mesh(xw, ys, order)
                if db_on:
                    if not hasTbl:
                        insert = 'INSERT INTO {}(code) values({})'.format(
                            tbname, code)
                        cur.execute(insert)
                if not quiet:
                    print(code)
                if geom:
                    outFeature.SetGeometry(cell)
                    outFeature.SetField("code", code)
                    outLayer.CreateFeature(outFeature)
    if db_on:
        if not hasTbl:
            conn.commit()
            conn.close()

    if geom:
        outFeature = None
        outDataSource = None

if __name__ == '__main__':

    main()