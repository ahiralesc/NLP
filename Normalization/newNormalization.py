#!/usr/bin/env python

# Copyright Hash-LSH Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#########################################################################    ##
#
# Author: Adan Hirales Carbajal
# Email : adan.hirales@cetys.mx
#
#########################################################################    ##


import argparse
import re
import pandas as pd
import os
from normalization import FilterFactory, loadRawData, writeRawData, Trie
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

medicTrie = Trie()
humanTrie = Trie()
medicTrie.read_trie("/root/homeDir/mosby/corpus/mosbyTrie.csv")
humanTrie.read_trie("/root/homeDir/mosby/corpus/humanTrie.csv")



hp = {
	
		"filters" 	: [],
		"source"	: None,
		"target"	: None,
		"verbose"	: False
	}


def parseCLA( ):
	parser = argparse.ArgumentParser(description='Applies text normalization filters in the order in which filters are specified to the target text file.')

	parser.add_argument('-rmcc', nargs='?', default=-1, type=int, help='Replace unicode control characters [ \\t\\n\\r\\f\\v] with a single white space.')
	parser.add_argument('-rmpc', nargs='?', default=-1, type=int, help='Replace punctuation characters [!"#$%%&\'()*+, -./:;<=>?@[\]^_`{|}~]')
	parser.add_argument('-rmnc', nargs='?', default=-1, type=int, help='Remove numeric characters [0-9]')
	parser.add_argument('-rmsc', nargs='?', default=-1, type=int, help='Remove special characters except: a-zA-Z0-9 áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:')
	parser.add_argument('-ttlc', nargs='?', default=-1, type=int, help='Transform strings to lower case')
	parser.add_argument('-regex', nargs='?', default=-1, type=int, help='Label string patterns that match regular expressions')
	parser.add_argument('-s', nargs='?', default=None, type=str, help='The source text file')
	parser.add_argument('-t', nargs='?', default=None, type=str, help='The target filtered text file')
	parser.add_argument('-v', nargs='?', default=False, type=bool, help='Verbose output')

	args = vars(parser.parse_args())

	# Extract switches and sort them
	switches = dict(list(args.items())[:6])
	switches = {k:v for k, v in sorted(switches.items(), key=lambda v: int(v[1]))}

	for k, v in switches.items():
		if v != -1:
			hp["filters"].append(k)

	# Extract source and target file name and location
	hp["source"] = args['s']
	hp["target"] = args['t']
	hp["verbose"] = args['v']

	if (hp["source"] == None or hp["target"] == None):
		print("source and/or target files not specified")
		exit(0);



def loadSource():
	files = list()
	for file in os.listdir(hp["source"]):

#a: There was a ValueError and to avoid them I added a little bit of extra code.

		parts = file.split(".")			#splits file name into array using the "." as a marker
		if len(parts) >= 2:				#if there are no dots, then the file doesn't even have extension
			tmp = ".".join(parts[:-1])	#everything except last element is sent to a temporary variable
			val = parts[-1] 			##Last element of the parts array is saved in val
			if val.lower() == "txt":	#.lower method to avoid using OR. Checks if the last element in the file name is "txt"
				files.append(file)		
	return files


def all_lower(my_list):
	return [x.lower() for x in my_list]

def tokenFix(file):
	
	"""
 
	Token fix is a new function that is used to correct any conversion errors during the
	.pdf to .txt convertion. It uses a dual-trie that checks if a the token is a word in the dictionary and
	needs to be edited. 
	
	fNone (file object) and non (list object) are used for testing, in order to write the tokens that
	are not found even after spliting.
	
	The file can later be sorted.
	
	"""
	fNone = open("/root/homeDir/mosby/corpus/nonefound.txt", "a", encoding="utf-8")
	fNone.write(file)
	fNone.close	
 
	print(file)
	i = 0
	non = []
	
	tokens = word_tokenize(loadRawData(file))
	tokens = all_lower(tokens)
	
	while i != len(tokens):
	
  
		
		token = tokens[i]
		

		
		index = tokens.index(token)
		
		if(not (token in medicTrie.trie or token in humanTrie.trie)):

   
			TokenSplit = re.split(r"([^a-zA-Z]+)", tokens[i])
			
			TokenSplit = list(filter(None, TokenSplit))
			
			
			"""
   			Checks if any element of the splitted token is in the dual-trie
   			If it is, then the splitted token is inserted into the main tokens list
			If it isn't, then the token is written in the non list.

      		"""
			if any((t in medicTrie.trie or t in humanTrie.trie) for t in TokenSplit):
   
				tokens[index] = TokenSplit[0]
				
				if(len(TokenSplit) != 1):
					for split in TokenSplit[1:]:
					
						tokens.insert(index, split)
						i += 1
			else:
				non.append(token)
	
		i += 1
  
		# A little print statement used to know the progress of the convertion
		if(i % 1000 == 0):
			print(F"{i} / {len(tokens)}")

	fNone = open("/root/homeDir/mosby/corpus/nonefound.txt", "a", encoding="utf-8")
	fNone.write("\n".join(nonFound for nonFound in non))
	fNone.close

	return tokens

def normalize( source, target  ):


	newsource = target[:-4] + ".txt"

	dt = " ".join(tokenFix(source))
	fileWrite = open(newsource, "w", encoding="utf-8")
	fileWrite.write("".join(dt))
	fileWrite.close()
 
	pdf = pd.DataFrame( data = { 'data': [ dt ] }, index=[0] )

	# filter creation phase
	filters = dict()
	filter_factory = FilterFactory()
	for name in hp["filters"]:
		filters[name] = filter_factory.create(name)

	# Data normalization phase
	for _name, _filter in filters.items():
		pdf = _filter.apply(pdf,"data")

	# Storage phase
	writeRawData( target, pdf.loc[0,'data'] )
	

# main thread of execution
# 1. parser command line arguments
parseCLA( )
# 2. load the file dataset 
files = loadSource()
# 3. normalize files in the dataset
for file in files:
	#Para archivo en directorio.
	source = hp["source"] + file
 	#Nombre de la fuente
	target = hp["target"] + file
	#Nombre del output
	if hp['verbose'] == True :
		print("Normalizing {}, writting output to {}".format(file, target))
  #Func. normalize
	normalize( source, target )

