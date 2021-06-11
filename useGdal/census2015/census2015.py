import os
import sys
import pandas as pd
import sqlite3

'''
CAUTION !!!!
THIS MODULE IS ADAPT ONLY CENSUS 2015

https://www.e-stat.go.jp/help/data-definition-information/shuroku/T000876.pdf
'''
preFix = "tblT000876Q" # statsId = T000876, aggregateUnit = Q

dbname = 'temp.db'
if not os.path.exists(dbname):
    sys.exit("ERROR : {} no such file.".format(dbname))

conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("select * from sqlite_master where type='table'")

c, ready = 0, False
tables = [columns[1] for columns in cur.fetchall()]
for table in tables:
    if table == "mesh1" or table == "mesh5":
        c += 1
    if table == "polulatin":
        ready = True

if c != 2:
    msg  = '\n ERROR : non exists table(s) to use in this module\n'
    msg += '  run `meshes.py -1 foo.geojson` and\n'
    msg += '      `meshes.py -5 foo.geojson` before run this module'
    sys.exit(msg)

if not ready:
    cur.execute("select * from mesh1")
    mesh1 = [ columns[0] for columns in cur.fetchall() ]
    cur.execute("drop table if exists population")
    for mesh in mesh1:
        zip_file = preFix + mesh + '.zip'
        if not os.path.exists(zip_file):
            print("ERROR : {} not found".format(zip_file), file=sys.stderr)
            cur.execute("drop table if exists population")
            break
        df = pd.read_csv(
            zip_file,
            encoding = 'shift_jis',
            skiprows = 2,
            header   = None,
            usecols  = [0, 4],
            names    = ['code', 'population'],
            dtype    = {'code': str, 'population': int}
        )
        df.to_sql('population', conn, if_exists='append')
        del df

sql = '''
    select sum(population)
        from mesh5
        join population
            on mesh5.code = population.code
'''
population = cur.execute(sql).fetchone()[0]
print('\n Population : {:,}'.format(population))

cur.close()
conn.close()