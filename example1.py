#!/usr/bin/env python


import argparse
import sys

from Edif_parser_mod import *

if __name__ == "__main__": 

	parser = argparse.ArgumentParser()
	parser.add_argument('input')	
	args = parser.parse_args()
	
	filename  = args.input

	edif_root = Read_Edif_file(filename)
	
	# getting object in tree from root and "edif.edifversion"	
	obj = edif_root.get_object("edif.edifversion")
	# getting params by indexes
	version = obj.get_params( [0, 1, 2] )
	
	print "Edif version : ", version[0], version[1], version[2]
	
	if ( (version[0]=='2') and (version[1]=='0') and(version[2]=='0') ):
		print ";)"
		# print objects
		print edif_root.get_object("edif.library").output()
	
	sys.exit()

