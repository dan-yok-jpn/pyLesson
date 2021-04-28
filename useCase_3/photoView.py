# coding:utf-8

import sys
import os
import glob
import json
import imghdr
from PIL import Image
from PIL.ExifTags import TAGS as ExifTags

def usage():
	s  = '\n Create a web content named clickMe.html '
	s += '(displays a photo by clicking a marker on the map) '
	s += "in the directory 'path_to_jpegs'. \n"
	s += '\n  Usage : python {} [( -h | --help | path_to_jpegs )] \n'
	s += "\n If you omit 'path_to_jpegs', assign current directory for it. \n"
	sys.exit(s.format(sys.argv[0]))

def dms_2_deg(dms):
	return (dms[2] / 60. + dms[1]) / 60 + dms[0] 

def getExif(file):

	if imghdr.what(file) != 'jpeg':
		return False, {}

	im = Image.open(file)
	try:
		exif = {
			ExifTags[k]: v
			for k, v in im._getexif().items()
				if k in ExifTags # except non-standard
		}
	except AttributeError:
		return False, {}

	# Standard Exif Tags
	# https://www.exiv2.org/tags.html
	GPSInfo = exif['GPSInfo']
	DateTimeOriginal = exif['DateTimeOriginal']
	GPSLongitude     = GPSInfo[4]
	GPSLatitude      = GPSInfo[2]
	info = {
		'name': os.path.basename(file),
		'time': DateTimeOriginal,
		'lnglat': (dms_2_deg(GPSLongitude), dms_2_deg(GPSLatitude))
	}
	return True, info

def boundBox(points):

	lngs,lats = [], []
	for point in points:
		lngs.append(point[0])
		lats.append(point[1])
	return [[min(lngs), min(lats)], [max(lngs), max(lats)]]

def main(dir = '.'):

	files = glob.glob(dir + '/*')
	geojson = {'type': 'FeatureCollection', 'features': []}
	features = geojson['features']
	points = []
	for f in files:
		if os.path.isdir(f):
			continue
		hasGPS, info = getExif(f)
		if hasGPS:
			src = info['name']
			points.append(info['lnglat'])
			feature = {
				'type': 'Feature',
			    'geometry': {'type': 'Point', 'coordinates': info['lnglat']},
				'properties': {'src': src, 'time': info['time']}
			}
			features.append(feature)

	if len(features) == 0:
		sys.exit('\n Failed to get GPS information.')

	geojson['bbox'] = boundBox(points)

	with open(dir + '/clickMe.html', 'w', encoding = 'utf-8') as f:
		s  = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>photoView</title><link rel="stylesheet"href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"></script><style>body {padding: 0; margin: 0}html, body, #map {height: 100%; width: 100%;}  textarea {font-weight: bold;}.leaflet-popup-content {width: 200px;}.thumbnail {max-width:200px; max-height:200px}</style></head><body><div id="map"></div><script>var map=L.map("map");L.tileLayer("https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png").addTo(map);'
		s += 'var geojson=' + json.dumps(geojson) + ';'
		s += 'var bbox=geojson.bbox;var southWest=[bbox[0][1],bbox[0][0]];var northEast=[bbox[1][1],bbox[1][0]];map.fitBounds([southWest,northEast]);L.geoJSON(geojson).bindPopup((layer)=>{var prop=layer.feature.properties;var src=prop.src;var html="<p><b>"+prop.src+"</b><br>"+prop.time+"</p>";html+="<a href=\'"+src+"\' target=\'_blank\' download>";html+="<img class=\'thumbnail\' src=\'"+ src+"\'></a>";return html;}).addTo(map);</script></body></html>'
		f.write(s)

if __name__ == '__main__':

	if '-h' in sys.argv or '--help' in sys.argv:
		usage()

	if len(sys.argv) == 1:
		main()
	else:
		dir = sys.argv[1]
		if not '\\' in dir:
			dir = '.\\' + dir
		if os.path.isdir(dir):
			main(dir)
		else:
			sys.exit('\n {} no such directory.'.format(dir))