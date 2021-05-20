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
				'properties': {'img': src, 'caption': '', 'time': info['time']}
			}
			features.append(feature)

	if len(features) == 0:
		sys.exit('\n Failed to get GPS information.')

	geojson['bbox'] = boundBox(points)

	with open(dir + '/clickMe.html', 'w', encoding = 'utf-8') as f:
		s = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>View Photos on Map</title><link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"/><script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script><script src="exif.js"></script><style>body{padding: 0; margin: 0}html, body, #map{height: 100%; width: 100%}.caption{font-weight: bold}.leaflet-popup-content{width: 200px;}.thumbnail{max-width:200px; max-height:200px}</style></head><body><div style="text-align:right;"><input id="save" type="button" value="saveCange"></div><div id="map"></div><script>var btn=document.getElementById("save");btn.disabled=true;btn.addEventListener("click", ()=>{var contents=\'var geojson=\'; contents +=JSON.stringify(geojson, "", 2);var blob=new Blob([contents],{type: "text.plain"});var a=document.createElement("a");document.body.appendChild(a);a.href=URL.createObjectURL(blob);a.download="exif.js";a.style="display: none";a.click();URL.revokeObjectURL(a.href);btn.disabled=true;});var map=L.map(\'map\');L.tileLayer(\'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png\',{attribution: "<a href=\'https://maps.gsi.go.jp/development/ichiran.html\' target=\'_blank\'>地理院タイル</a>"}).addTo(map);bbox=geojson.bbox;southWest=[bbox[0][1], bbox[0][0]];northEast=[bbox[1][1], bbox[1][0]];map.fitBounds([southWest, northEast]);L.geoJSON(geojson) .bindPopup((layer)=>{var prop=layer.feature.properties; var img=prop.img;var html=\'<input type="text" id="caption" value="\' + prop.caption + \'" class="caption" placeholder="--caption--">\';html +="<p>" + prop.time + "</p>"; html +="<a href=\'" + img + "\' target=\'_blank\' download>"; html +="<img class=\'thumbnail\' src=\'" + img + "\'></a>"; return html;}) .on(\'popupclose\', function(ev){var elem=document.getElementById("caption"); if(elem){var caption=elem.value; var properties=ev.layer.feature.properties; if(properties.caption !=caption){properties.caption=caption; btn.disabled=false;}}}) .addTo(map);</script></body></html>'
		f.write(s)

	with open(dir + '/exif.js', 'w', encoding = 'utf-8') as f:
		f.write('var geojson=' + json.dumps(geojson, indent=2) + ';')

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