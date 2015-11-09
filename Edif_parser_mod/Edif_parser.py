#!/usr/bin/env python

__version__ = '1.0.0'
__author__ = 'THLN47'
__doc__ = 'Edif parser for Python'
__all__ = [
	'EdifObject',
	'Read_Edif_file',
	
	'search_edif_objects',
	'extract_edif_str_param',
	'extract_edif_pt'
	]


import pprint
import os

"""
	@see : https://sexpdata.readthedocs.org/en/latest/
"""
from sexpdata import *


ContextDef = [
	"",
	"acload",
	"after",
	"annotate",
	"apply",
	"arc",
	"array",
	"arraymacro",
	"arrayrelatedinfo",
	"arraysite",
	"atleast",
	"atmost",
	"author",
	"basearray",
	"becomes",
	"between",
	"boolean",
	"booleandisplay",
	"booleanmap",
	"borderpattern",
	"borderwidth",
	"boundingbox",
	"cell",
	"cellref",
	"celltype",
	"change",
	"circle",
	"color",
	"comment",
	"commentgraphics",
	"compound",
	"connectlocation",
	"contents",
	"cornertype",
	"criticality",
	"currentmap",
	"curve",
	"cycle",
	"dataorigin",
	"dcfaninload",
	"dcfanoutload",
	"dcmaxfanin",
	"dcmaxfanout",
	"delay",
	"delta",
	"derivation",
	"design",
	"designator",
	"difference",
	"direction",
	"display",
	"dominates",
	"dot",
	"duration",
	"e",
	"edif",
	"ediflevel",
	"edifversion",
	"enclosuredistance",
	"endtype",
	"entry",
	"exactly",
	"external",
	"fabricate",
	"false",
	"figure",
	"figurearea",
	"figuregroup",
	"figuregroupobject",
	"figuregroupoverride",
	"figuregroupref",
	"figureperimeter",
	"figurewidth",
	"fillpattern",
	"follow",
	"forbiddenevent",
	"globalportref",
	"greaterthan",
	"gridmap",
	"ignore",
	"includefiguregroup",
	"initial",
	"instance",
	"instancebackannotate",
	"instancegroup",
	"instancemap",
	"instanceref",
	"integer",
	"integerdisplay",
	"interface",
	"interfiguregroupspacing",
	"intersection",
	"intrafiguregroupspacing",
	"inverse",
	"isolated",
	"joined",
	"justify",
	"keyworddisplay",
	"keywordlevel",
	"keywordmap",
	"lessthan",
	"library",
	"libraryref",
	"listofnets",
	"listofports",
	"loaddelay",
	"logicassign",
	"logicinput",
	"logiclist",
	"logicmapinput",
	"logicmapoutput",
	"logiconeof",
	"logicoutput",
	"logicport",
	"logicref",
	"logicvalue",
	"logicwaveform",
	"maintain",
	"match",
	"member",
	"minomax",
	"minomaxdisplay",
	"mnm",
	"multiplevalueset",
	"mustjoin",
	"name",
	"net",
	"netbackannotate",
	"netbundle",
	"netdelay",
	"netgroup",
	"netmap",
	"netref",
	"nochange",
	"nonpermutable",
	"notallowed",
	"notchspacing",
	"number",
	"numberdefinition",
	"numberdisplay",
	"offpageconnector",
	"offsetevent",
	"openshape",
	"orientation",
	"origin",
	"overhangdistance",
	"overlapdistance",
	"oversize",
	"owner",
	"page",
	"pagesize",
	"parameter",
	"parameterassign",
	"parameterdisplay",
	"path",
	"pathdelay",
	"pathwidth",
	"permutable",
	"physicaldesignrule",
	"plug",
	"point",
	"pointdisplay",
	"pointlist",
	"polygon",
	"port",
	"portbackannotate",
	"portbundle",
	"portdelay",
	"portgroup",
	"portimplementation",
	"portinstance",
	"portlist",
	"portlistalias",
	"portmap",
	"portref",
	"program",
	"property",
	"propertydisplay",
	"protectionframe",
	"pt",
	"rangevector",
	"rectangle",
	"rectanglesize",
	"rename",
	"resolves",
	"scale",
	"scalex",
	"scaley",
	"section",
	"shape",
	"simulate",
	"simulationinfo",
	"singlevalueset",
	"site",
	"socket",
	"socketset",
	"status",
	"steady",
	"string",
	"stringdisplay",
	"strong",
	"symbol",
	"symmetry",
	"table",
	"tabledefault",
	"technology",
	"textheight",
	"timeinterval",
	"timestamp",
	"timing",
	"transform",
	"transition",
	"trigger",
	"true",
	"unconstrained",
	"undefined",
	"union",
	"unit",
	"unused",
	"userdata",
	"version",
	"view",
	"viewlist",
	"viewmap",
	"viewref",
	"viewtype",
	"visible",
	"voltagemap",
	"wavevalue",
	"weak",
	"weakjoined",
	"when",
	"written"
]	


class contextObj(object):
	def __init__(self, enumName, listValueNames):
		listValueTyped = [ type(".".join((enumName, nameValue)), (), {}) 
			for nameValue in listValueNames ]
		self.dictAttrib = dict( zip(listValueNames, listValueTyped) )
		self.dictReverse = dict( zip(listValueTyped, listValueNames) )

	def getValue(self, name):
		try:
			ret = self.dictAttrib[name]
		except KeyError:
			print "*** ERROR unkwnon object '",name,"'"
			ret = None
		return ret
		
	def getName(self, value):
		try:	
			ret = self.dictReverse[value]
		except KeyError:
			print "*** ERROR unkwnon type '",value,"'"
			ret = None
		return ret		
		
	
context_obj = contextObj("Context", ContextDef)	 




class EdifObject(object):

	def __init__(self, name):
		global context_obj
		self.context = context_obj.getValue(name.lower())
		#pprint.pprint(self.context)
		self.params = []
	
	def add_param(self, param):
		#print "add param(",param,")"
		self.params.append(param)
	

	def get_param(self, index):
		return self.params[index]
	
	def get_params(self):
		return self.params
	
	def get_params(self, indexes):
		result = []
		for index in indexes:
			result.append( self.get_param(index) )
		return result
		
	def get_nb_param(self):
		return len(self.params)
	
	def output(self):
		global context_obj
		#print self.context,

		string = "\n( "+context_obj.getName(self.context)
		for param in self.params:
			if (type(param)==EdifObject):
				string += param.output()
			else:
				string += " "+param
		string += ")"
		
		return string

	def get_context(self):
		return context_obj.getName(self.context)
	
	def __get_object(self, context_name):
		for item in self.params:
			if (type(item)==EdifObject):
				if (context_name.lower()==item.get_context()):
					return item
		return None

	def get_object(self, context_path, abort_on_error=False):
		context_list = context_path.split(".")
		#print context_list
		current_obj = self
		for context_name in context_list:
			tmp_obj = current_obj.__get_object(context_name)
			if (tmp_obj==None):
				if (abort_on_error):
					print "*** ERROR : key '%s' unkwnon in '%s' !" % (context_name, current_obj.get_context())
					sys.exit()
				else:
					return None		
			else:
				current_obj = tmp_obj
		return current_obj
	
	def get_object_param(self, context_name, param0):
		obj = self.get_object(context_name)
		if (obj!=None):
			if (obj.get_param(0)==param0):
				return obj
		return None
		
	def find_objects(self, context_name, result):
		
		for item in self.params:
			if (type(item)==EdifObject):
				if (context_name.lower()==item.get_context()):
					result.append( item )
				item.find_objects(context_name, result)
		return
		
	def __str__(self):
		s = str(type(self))
		#s = self.__name__
		s += "_"
		s += self.get_context()
		return s
	
	
	
	
def Edif_parse_recurs(data, parent_obj, level=0):		
	"""
	"""			
	if (isinstance(data, list)):		
		items = data				
		#print len(items), "item(s) at level",level
		next_level = level+1
		
		current_obj = None
		ix=0
		for item in items:
					
			if (ix==0):
				name = dumps(item)
				current_obj = EdifObject(name)				
			else:
				if (current_obj!=None):					
					Edif_parse_recurs(item, current_obj, next_level)			
			ix+=1	
		ret = current_obj
	else:
		ret = dumps(data)
	
	parent_obj.add_param(ret)	

	return 

	
def Read_Edif_file(filename):

	if (os.path.exists(filename) == False):
		print ('Le fichier '+filename+' n\'existe pas')
		return None
	file = open(filename, 'r')
	content = file.read()
	file.close()
	
	data = loads(content)
		
	edif_root = EdifObject("")
	Edif_parse_recurs(data, edif_root, 0)	
		
	return edif_root	
	
	

		
		
		
		
"""
	utils functions below ...
"""		
		
def search_edif_objects(parent_obj, context_name):
	objects = []
	parent_obj.find_objects(context_name, objects)
	return objects
		
		
def extract_edif_str_param(object, index):
	p1 = object.get_param(index)
	if (type(p1)==unicode):
		string = p1
		return [string, string]
	else:
		param_type = p1.get_context()
		if (param_type=="rename"):
			definition = p1.get_param(0)
			string = p1.get_param(1)
			return [definition, string]
		elif (param_type=="name"):
			string = p1.get_param(0)		
			return [p1, string]
	return None			
	

	
	
	
def extract_edif_pt(pt):
	if (pt!=None):
		pt_x = int(pt.get_param(0))
		pt_y = int(pt.get_param(1))
		return [pt_x, pt_y]
	else:
		return None	
	
