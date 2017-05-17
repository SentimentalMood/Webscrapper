#	Author: 	Andrew Thai
#	Project:	Web Scrapper
#	Date:		11/4/2016
#	Purpose: 	To be able to scrap desired information from a website and 
#				output the information in a json file
#	References:	https://www.tutorialspoint.com/python/python_command_line_arguments.htm
#				http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
#				https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
#				http://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return
#
#	Notes:		-Typically, this means sys.argv[1:]. options is the string of option letters that the 
#					script wants to recognize, with options that require an argument followed by a colon 
#					(':'; i.e., the same format that Unix getopt() uses).
#
#
#	Status:		Get all required information in the form of an input so it can be used in different ways
#				Make amount of information serached dynamic
#				Make amount of regex searches dynamic
#				Make amount of fieldnames dynamic

import sys, getopt, urllib, re, csv, json, panda, sql
	
def main(argv):
	urlfile = ''
	outputfile = ''
	
	regex = '<title>(.+?)</title>'
	pattern = re.compile(regex)
	
	regexURL = ('(.+?)$')
	patternURL = re.compile(regexURL)
	

	urlTable = []
	headerTable = []
	fieldnames = ['websites','headers']
	
	try:
		#getopt needs args, options, long options
		opts, args = getopt.getopt(argv,"hu:c:j:r:",["url=","csvfile=","jsonfile=","regex="])
	except getopt.GetoptError:
		print 'ERROR: ', sys.argv[0],' -u <inputfile> -c <csvfile>'
		sys.exit(2)

	#Determine what the options and long options do
	for opt, arg in opts:
	
		#HELP Option
		if opt == '-h':
			print sys.argv[0],' -u <inputfile> -c <csvfile>'
			sys.exit()

		
		#REGEX Option
		elif opt in ("-r", "--regex"):
			regex = arg.split("::")
			for x in range(0, len(regex)):
				pattern[x] = re.compile(regex[x])

		#URL Option
		elif opt in ("-u", "--url"):
			
			urlfile = open(arg, 'r')
			
			for line in urlfile:
				#Open URL Sites
				htmlfile = urllib.urlopen(line[0:len(line)-1])
				htmltext = htmlfile.read()
				
				#URL Title find all, array results
				urlTitle = re.findall(patternURL,line)
				
				#fields find all, array results
				titles = re.findall(pattern,htmltext)
				
				for fieldElements in fieldnames:
					
					urlTable.append(str(urlTitle[0]))
					headerTable.append(str(titles[0]))

			urlfile.close
		#Output csv Option
		elif opt in ("-c", "--csvfile"):
			with open(arg, 'wb') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
				writer.writeheader()
				for x in range (0, len(urlTable)):
					writer.writerow({'websites':str(urlTable[x]), 'headers': str(headerTable[x])})
			csvfile.close
			
		#Output csv Option
		elif opt in ("-j", "--jsonfile"):
			with open(arg, 'wb') as jsonfile:
					json.dump( {'websites':str(urlTable[x]), 'headers': str(headerTable[x])}, jsonfile, indent=2)
				for x in range (0, len(urlTable)):
			jsonfile.close
			
if __name__ == "__main__":
   main(sys.argv[1:])