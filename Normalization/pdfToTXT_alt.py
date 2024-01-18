"""
PDF to TXT script.
This alternative script is based on pypdf.
In some cases it may be better to use this one
because of the format of some PDF files.


Author: Alan Emilio P. Leon

Email: alan.contacto.leon@gmail.com

"""

# PyPDF library used for the conversion
from pypdf import PdfReader
import argparse
import os

hp = {
	
		"source"	: None,
		"target"	: None,
		"verbose"	: True
	}


def parseCLA( ):
	parser = argparse.ArgumentParser(description='Transforms PDF files into txt files')

	parser.add_argument('-s', nargs='?', default=None, type=str, help='The source text file')
	parser.add_argument('-t', nargs='?', default=None, type=str, help='The target filtered text file')
	parser.add_argument('-v', nargs='?', default=True, type=bool, help='Verbose output')

	args = vars(parser.parse_args())

	# Extract source and target file name and location
	hp["source"] = args['s']
	hp["target"] = args['t']
	hp["verbose"] = args['v']

	if (hp["source"] == None or hp["target"] == None):
		print("source and/or target files not specified")
		exit(0)

def loadSource():
    files = list()
    for file in os.listdir(hp["source"]):

#a: There was a ValueError and to avoid them I added a little bit of extra code.

        parts = file.split(".")			#splits file name into array using the "." as a marker
        if len(parts) >= 2:				#if there are no dots, then the file doesn't even have extension
            tmp = ".".join(parts[:-1])	#everything except last element is sent to a temporary variable
            val = parts[-1] 			##Last element of the parts array is saved in val
            if val.lower() == "pdf":	#.lower method to avoid using OR. Checks if the last element in the file name is "txt"
                files.append(file)		
    return files

# (I have to implement a for-loop )

# Set the file to convert



# Opens the file (names it's variable "f")
def PDFConverter(sourceFile,targetFile):
    read = PdfReader(sourceFile)

    with open(targetFile, 'w', encoding="utf-8") as f:

        # Array to join the pages
        parts = []

        # For loop to append the pages into single array
        for i in range(0,len(read.pages)): 
            page = read.pages[i]
            parts.append(page.extract_text())

        # Write the array data into the document
        f.write("".join(parts))


parseCLA()

files = loadSource()

for file in files:
    source = hp["source"] + file
    target = hp["target"] + file[:-4] + ".txt"
    
    if hp["verbose"] == True:
        print(F"Converting {source} into {target}")
    PDFConverter(source,target)

# Just for debuggin reasons
print("Done")