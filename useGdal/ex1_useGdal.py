
with open('enableGdal.py') as f:
	exec(f.read()) # import ogr

wkt1 = "POLYGON ((135 36, 137 36, 137 38, 135 38, 135 36))"
wkt2 = "POLYGON ((136 37, 138 37, 138 39, 136 39, 136 37)))"

poly1 = ogr.CreateGeometryFromWkt(wkt1)
poly2 = ogr.CreateGeometryFromWkt(wkt2)

poly3 = poly1.Intersection(poly2)
poly4 = poly1.Union(poly2)

with open('poly3.json', 'w') as f:
	print('{}'.format(poly3.ExportToJson()), file=f)

with open('poly4.json', 'w') as f:
	print('{}'.format(poly4.ExportToJson()), file=f)
