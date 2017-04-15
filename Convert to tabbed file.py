# -*- coding: utf-8 -*-

inputFilePath = "/Path/To/File/GlyphData.txt"

import sys, os

if len(sys.argv) > 1:
	inputFilePath = sys.argv[1]

if len(inputFilePath) < 5:
	print "Please supply a path to a file. This can be either a GlyphData.xml or a tab separated .txt file"
	exit()

if not os.path.isfile(inputFilePath):
	print "Could not find file at path:", inputFilePath
	exit()

# This list defineds the columns and ordering in the tabbed file.
fields = ["unicode",
		"name",
		#"unicode2",
		"sortName",
		"sortNameKeep",
		"decompose",
		"category",
		"subCategory",
		"script",
		"production",
		"altNames",
		"description",
		"anchors",
		"accents"]

def writeTabbedHeader(File):
	line = "\t".join(fields)+"\n"
	File.write(line)
	
def writeTabbedContent(inputFilePath, outFile):
	import xml.etree.ElementTree
	tree = xml.etree.ElementTree.parse(inputFilePath).getroot()
	i = 0
	for node in tree.iter():
		if node.tag != "glyph":
			continue
		nodeAttribs = dict(node.attrib)
		attribs = []
		for field in fields:
			attrib = nodeAttribs.get(field, "")
			if field == "unicode" and len(attrib) > 0:
				attrib = "\"%s\"" % attrib # Excel and Number import is as numbers anyway but you got to try
			attribs.append(attrib)
			try:
				nodeAttribs.pop(field)
			except:
				pass
		if len(nodeAttribs) > 0:
			print "Attributes not written:", node.attrib["name"], nodeAttribs
		line = "\t".join(attribs)+"\n"
		outFile.write(line.encode("utf-8"))

def writeDataHeader(File):
	File.write('<?xml version="1.0" encoding="UTF-8" ?>\n\
<!DOCTYPE glyphData [\n\
<!ELEMENT glyphData (glyph)+>\n\
<!ELEMENT glyph EMPTY>\n\
<!ATTLIST glyph\n\
	unicode			CDATA		#IMPLIED\n\
	name			CDATA		#REQUIRED\n\
	sortName		CDATA		#IMPLIED\n\
	sortNameKeep	CDATA		#IMPLIED\n\
	category		CDATA		#REQUIRED\n\
	subCategory		CDATA		#IMPLIED\n\
	script			CDATA		#IMPLIED\n\
	description		CDATA		#REQUIRED\n\
	production		CDATA		#IMPLIED\n\
	altNames		CDATA		#IMPLIED\n\
	decompose		CDATA		#IMPLIED\n\
	anchors			CDATA		#IMPLIED\n\
	accents			CDATA		#IMPLIED>\n\
]>\n\
<glyphData>\n')

def writeDataContent(inputFilePath, outFile):
	import codecs
	inFile = codecs.open(inputFilePath, "r", "utf-8")
	
	fields = inFile.readline().strip('\n').split("\t")
	print "Reading Fields:",", ".join(fields)
	for line in inFile:
		attribs = line.strip('\n').split("\t")
		line = u'	<glyph '
		for idx, field in enumerate(fields):
			attrib = attribs[idx]
			if len(attrib) > 0:
				attrib = attrib.strip("\"")
				line += u'%s="%s" ' % (field, attrib)
		line += '/>\n'
		outFile.write(line.encode("utf-8"))
	outFile.write('</glyphData>\n')
	inFile.close()

if inputFilePath[-4:] == ".xml":
	print "To Tabbed", inputFilePath
	outputFilePath = inputFilePath[:-4]+".txt"
	outputFile = open(outputFilePath, "w")
	writeTabbedHeader(outputFile)
	writeTabbedContent(inputFilePath, outputFile)
	outputFile.close()
elif inputFilePath[-4:] == ".txt":
	print "To XML: ", inputFilePath
	outputFilePath = inputFilePath[:-4]+"_new.xml"
	outputFile = open(outputFilePath, "w")
	writeDataHeader(outputFile)
	writeDataContent(inputFilePath, outputFile)
	outputFile.close()
	
	
