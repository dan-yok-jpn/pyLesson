# coding:utf-8

import sys, os, glob
import xml.etree.ElementTree as ET 

def usage(progname):

	s1  = '\n 電子成果品の業務管理ファイル（index_d.xml）と'
	s1 += '報告書管理ファイル（report.xml）から主要な項目を抽出して画面に表示する \n'
	print(s1, file=sys.stderr)

	print('  使用法 : python {0} [--help] [directory] \n'.format(progname),
		file=sys.stderr)

	s2  = '    --help    : このヘルプを表示 \n'
	s2 += '    directory : index_d.xml を探索するトップ・ディレクトリ'
	s2 += ' (カレント・ディレクトリの場合、省略可) \n'
	print(s2, file=sys.stderr)

	print('  使用例 : python {0} .\収集資料\電子納品'.format(progname),
		file=sys.stderr)

	sys.exit()

def parseReport(path):

	print('【報告書】')
	root = ET.fromstring(open(path + '/REPORT.XML').read())
	s = ''
	for item in root.findall('報告書ファイル情報'):
		obj   = item.find('報告書ファイル日本語名')
		docEN = item.find('報告書ファイル名').text
		docJP = obj.text if not obj is None else ''
		print('\t{0}\t{1}'.format(docEN, docJP))
		for org in item.findall('報告書オリジナルファイル情報'):
			obj   = org.find('報告書オリジナルファイル日本語名')
			docEN = org.find('報告書オリジナルファイル名').text
			docJP = obj.text if not obj is None else ''
			s += '\t{0}\t{1}\n'.format(docEN, docJP)
	print('【報告書オリジナル】')
	print(s)

	return

def parseEachSurvey(xmlFile, id):

	root = ET.fromstring(open(xmlFile).read())
	for item in root.findall('測量成果情報'):
		obj = item.find('測量細区分フォルダ名')
		if obj is None: continue
		subFolder = obj.text
		if subFolder == id:
			folder  = item.find('測量成果区分フォルダ名').text + '/'
			folder += subFolder
			title   = item.find('測量成果名称').text
			print('\t\t【{}】'.format(title))
			for f in item.iter('成果ファイル情報'):
				obj    = f.find('測量成果ファイル名副題')
				nameEN = f.find('測量成果ファイル名').text
				nameJP = obj.text if not obj is None else ''
				print('\t\t\t{}/{}\t{}'.format(folder, nameEN, nameJP))

def parseSurvey(path):

	xmlFiles = {
		'基準点測' : '/KITEN/SURV_KTN.XML' ,
		'水準測量' : '/SUIJUN/SURV_SJN.XML',
		'地形測量' : '/CHIKEI/SURV_CHI.XML',
		'路線測量' : '/ROSEN/SURV_RSN.XML',
		'河川測量' : '/KASEN/SURV_KSN.XML',
		'応用測量' : '/OTHERSOYO/SURV_OYO.XML'
	}

	print('【測量成果】')
	root = ET.fromstring(open(path + '/SURVEY.XML').read())
	obj  = root.find('場所情報').find('区域情報')
	print('\t【平面直角座標系】{}'.format(obj.find('平面直角座標系').text))
	for item in root.findall('測量情報'):
		category    = item.find('測量区分').text
		subCategory = item.find('測量細区分').text
		id = item.find('測量記録フォルダパス名').text.split('/')[3]
		print('\t【{}／{}】'.format(category, subCategory))
		xmlFile = path + xmlFiles[category[0:4]]
		parseEachSurvey(xmlFile, id)
	return

def parseIndex(base, filename):

	root    = ET.fromstring(open(filename).read())
	child   = root.find('業務件名等')
	title   = child.find('業務名称').text
	sFrom   = child.find('履行期間-着手').text
	sTo     = child.find('履行期間-完了').text
	company = root.find('受注者情報').find('受注者名').text
	summary = root.find('業務情報').find('業務概要').text

	print('【業務名】{0}'.format(title))
	print('【工　期】{0}～{1}'.format(sFrom, sTo))
	print('【受注者】{0}'.format(company))
	print('【概　要】{0}'.format(summary))

	report = base + '/REPORT'
	if os.path.exists(report):
		parseReport(report)

	survey = base + '/SURVEY'
	if os.path.exists(survey):
		parseSurvey(survey)

	print('---------------------------------------')

def findIndex(base):

	filename = base + '/INDEX_D.XML'
	if os.path.exists(filename):
		parseIndex(base, filename)
		return

	for f in glob.glob(base + '/*'):
		if os.path.isdir(f):
			findIndex(f) # recursive

if __name__ == '__main__':

	if '--help' in sys.argv:
		usage(sys.argv[0])

	if len(sys.argv) == 2:
		root = sys.argv[1]
		if not os.path.exists(root):
			sys.exit('\n {0} no such directory.'.format(base))
	else:
		root = '.'

	findIndex(root)
