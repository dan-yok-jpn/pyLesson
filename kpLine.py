import sys
import json
import csv
import io

def usage():
	msg  = '\n 横断測線の GIS データ (GeoJSON) を出力 \n'
	msg += '\n  使用法 : python {} [-h|--help] 引数_1 引数_2 [引数_3] \n '
	msg += '\n  引　数: @ 必須 \n'
	msg += "\n   @ 引数_1 : 入力ファイル名* ('-' ハイフンの場合は標準入力）"
	msg += '\n   @ 引数_2 : 測地成果/系番号** '
	msg += '\n     引数_3 : 出力ファイル名 \n'
	msg += '\n  注意点 : \n'
	msg += '\n   *    タブ区切りのテキストファイルで以下の様式 \n'
	msg += '\n          測線名    <tab> x座標 <tab> y座標 <tab> x座標 <tab> y座標 '
	msg += '\n   または 測線名*** <tab> 経 度 <tab> 緯 度 <tab> 経 度 <tab> 緯 度 '
	msg += "\n              緯度・経度は度数（実数）ないし 度-分-秒 \n"
	msg += '\n   **   (2000|2011)/[0-19] 例えば 2000/0：jgd2000, 2011/9：jgd2011 CS-IX \n'
	msg += '\n   ***  漢字も可。ただし、文字コードは shift-jis \n'
	msg += '\n  使用法 : \n'
	msg += '\n   python {} kp_someRiver.tsv 2011/9   kp_someRiver.json '
	msg += '\n   python {} kp_someRiver.tsv 2011/9 > kp_someRiver.json '
	msg += '\n   otherProg | python {}  -   2011/9 > kp_someRiver.json \n'
	mod  = sys.argv[0]
	sys.exit(msg.format(mod, mod, mod, mod))

case = 0

def Point(s):
	global case
	if case == 1:
		d, m, s = s.split('-')
		return (float(s) / 60 + float(m)) / 60 + float(d)
	elif case == 2:
		return float(s)
	else: # judge only once at the beginning
		case = 1 if '-' in s else 2
		return Point(s)

def makeDic(src_path, epsg, lonlat):
	if src_path == '-':
		fin = sys.stdin
	else:
		try:
			fin = open(src_path, 'r')
		except:
			sys.exit('\n ERROR : {} no such file'.format(src_path))
	crs  = {'type': 'EPSG', 'properties': {'code': epsg}}
	dic  = {'type': 'FeatureCollection', 'crs': crs, 'features': []}
	rows = csv.reader(fin, delimiter = '\t')
	for columns in rows:
		if len(columns) != 5: break
		name = str(columns[0]).strip()
		if lonlat:
			p1 = [Point(columns[1]), Point(columns[2])]
			p2 = [Point(columns[3]), Point(columns[4])]
		else: # xy  x : n-s, y : w-e
			p1 = [float(columns[2]), float(columns[1])]
			p2 = [float(columns[4]), float(columns[3])]
		p = {'name': name}
		g = {'type': 'LineString', 'coordinates': [p1, p2]}
		f = {'type': 'Feature', 'geometry': g, 'properties': p}
		dic['features'].append(f)
	fin.close()
	return dic

def cnv_2_epsg(arg):
	if   arg == '2000/0' or arg == '2000':
		return ('4612', True)
	elif arg == '2011/0' or arg == '2011': 
		return ('6668', True)
	else:
		try:
			jgd, cs = arg.split('/')
			num = int(cs)
		except:
			sys.exit('\n エラー：引数 ' + arg + ' は不適切')
		test_1 = not jgd in ('2000', '2011')
		test_2 = not (1 <= num and num <= 19)
		if test_1 or test_2:
			sys.exit('\n エラー：引数 ' + arg + ' は不適切')
		if jgd == '2000':
			return (str(num + 2442), False) 
		else:
			return (str(num + 6668), False) 

# dic = makeDic('kpLine.tsv', '2451', False)

if '-h' in sys.argv or '--help' in sys.argv:
	usage()
argc = len(sys.argv)
if argc >= 3:
	epsg, lonlat = cnv_2_epsg(sys.argv[2])
	dic = makeDic(sys.argv[1], epsg, lonlat)
	if argc == 3:
		sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
		json.dump(dic, sys.stdout, ensure_ascii = False, indent = 2)
	else:
		with open(sys.argv[3], 'w', encoding = 'utf-8') as fot:
			json.dump(dic, fot,    ensure_ascii = False, indent = 2)
else:
	usage()
