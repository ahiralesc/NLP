""""

Author: Alan Emilio P. Leon

Email: alan.contacto.leon@gmail.com

PDF-TO-TXT python script (Based on pymupdf)

"""



import fitz                             #pymupdf
import os
import argparse

hp = {
	
		"source"	: None,
		"target"	: None,
		"verbose"	: True
	}


# Credits to Dr. Hirales for argument parser function.

def parseCLA( ):
	parser = argparse.ArgumentParser(description='Transforms PDF files into txt files')

	parser.add_argument('-s', nargs='?', default=None, type=str, help='The source directory for PDFs')
	parser.add_argument('-t', nargs='?', default=None, type=str, help='The target directory for TXTs')
	parser.add_argument('-v', nargs='?', default=True, type=bool, help='Verbose output')

	args = vars(parser.parse_args())

	# Extract source and target file name and location
	hp["source"] = args['s']
	hp["target"] = args['t']
	hp["verbose"] = args['v']

	if (hp["source"] == None or hp["target"] == None):
		print("source and/or target files not specified")
		exit(0)

def loadSource(dir):
    files = list()
    
    for file in os.listdir(dir):
        parts = file.split(".")			#splits file name into array using the "." as a marker
        if len(parts) >= 2:				#if there are no dots, then the file doesn't even have extension
            val = parts[-1] 			##Last element of the parts array is saved in val
            if val.lower() == "pdf":	#.lower method to avoid using OR. Checks if the last element in the file name is "txt"
                files.append(file)		
    return files


def convertion(sourcefile, targetfile):
    
    rect = fitz.Rect(0,50,612,725)
    
    with open(targetfile, 'w',encoding='utf-8') as f:
        doc = fitz.open(sourcefile)
        for i in range(2004,2006):
            
            page = doc[i]
            block = page.get_text("dict",flags=16+1+2+8)["blocks"]
            
            for parag in block:
                
                for line in parag["lines"]:
                    
                    for letter in line["spans"]:

                        
                        if letter["bbox"] in rect:
                            
                            # Uses a check to see if the word is a super/subscript.
                            # If it is, it writes a ^ so it doesn't merge with words or numbers 
                            
                            if letter["flags"] & 2 ** 0:
                                f.write(' ^ '+ letter["text"])
                                continue
                            
                            f.write(' ^ '+ letter["text"])
                            

                            

                    
                    
                    f.write(chr(32))
                f.write(chr(12))

        

def main():

    parseCLA()
    
    
    files = loadSource(hp["source"])

    for file in files:
        
        sourcefile = hp["source"] + file
        targetfile = hp["target"] + file[:-4] + '.txt'
        
        
        if(hp["verbose"]):
            print(F"Converting {file}")
        
        convertion(sourcefile,targetfile)
    
    
    
if __name__ == "__main__":
    main()
    
