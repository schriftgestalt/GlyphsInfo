#MenuTitle: write simple GlyphData
# -*- coding: utf-8 -*-

import codecs

infos = GSGlyphsInfo.sharedManager().glyphInfos()
# or:
# infos = GSGlyphsInfo.alloc().initWithLocalFile_(NSURL.fileURLWithPath_("path to custom GlyphData.xml file"))

f = codecs.open("GlyphData.xml", "w", "utf-8")
fIdeo = codecs.open("GlyphData_Ideographs.xml", "w", "utf-8")

def writeHeader(f):
	f.write('<?xml version="1.0" encoding="UTF-8" ?>\n\
<!DOCTYPE glyphData [\n\
<!ELEMENT glyphData (glyph)+>\n\
<!ELEMENT glyph EMPTY>\n\
<!ATTLIST glyph\n\
	unicode			CDATA		#IMPLIED\n\
	name			CDATA		#REQUIRED\n\
	category		CDATA		#REQUIRED\n\
	subCategory		CDATA		#IMPLIED\n\
	case			CDATA		#IMPLIED\n\
	script			CDATA		#IMPLIED\n\
	description		CDATA		#REQUIRED\n\
	production		CDATA		#IMPLIED\n\
	altNames		CDATA		#IMPLIED>\n\
]>\n\
<glyphData>\n')

writeHeader(f)
writeHeader(fIdeo)

disabledGlyphs = ["brevecomb_acutecomb",
				"brevecomb_gravecomb",
				"brevecomb_hookabovecomb",
				"brevecomb_tildecomb",
				"circumflexcomb_acutecomb",
				"circumflexcomb_gravecomb",
				"circumflexcomb_hookabovecomb", 
				"circumflexcomb_tildecomb",
				"idotaccent.sc", 
				"i.sc",
				]
forcedGlyphs = ["ringcenter-ar"]

def printInfo(info):
	string = '	<glyph '
	if info.unicode:
		string += 'unicode="' + info.unicode + '" '
	string += 'name="' + info.name + '" '
# 	if info.sortName:
# 		string += 'sortName="' + info.sortName + '" '
	if info.category:
		string += 'category="' + info.category + '" '
	if info.subCategory and info.subCategory != "Other":
		string += 'subCategory="' + info.subCategory + '" '
	if info.case > 0:
		string += 'case="'+GSGlyphInfo.stringFromCase_(info.case) + '" '
	if info.script:
		string += 'script="' + info.script + '" '
	if info.productionName:
		string += 'production="' + info.productionName + '" '
	if info.altNames:
		string += 'altNames="' + ", ".join(info.altNames) + '" '
	if info.desc:
		string += 'description="' + info.desc + '" '
	
	string += '/>\n'
	return string
	
count = 0
for info in infos:
	name = info.name;
	isUniName = False
	try:
		if name.startswith("uni"):
			isUniName = True
		elif name.startswith("u") and int(name[1:], 16) > 0:
			isUniName = True
	except:
		pass
	if info.script == "han" and isUniName:
		fIdeo.write(printInfo(info))
	elif (info.name in disabledGlyphs or info.name.endswith(".case") or (info.script == "arabic" and info.unicode is None)) and (info.name not in forcedGlyphs):
		continue
	else:
		f.write(printInfo(info))
	count += 1

print("Written %d entries" % count)
f.write('</glyphData>\n')
fIdeo.write('</glyphData>\n')

f.close()
fIdeo.close()