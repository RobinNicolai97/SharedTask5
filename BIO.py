import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

f = open("BIO_train.txt", "w", encoding = 'utf8')
with open("tsd_train.csv",  encoding="utf8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file 
	for row in csv_reader:
		if row[0].strip() == '[]':
			i = 0
			tag = ''
			prev_tag = ''
			string = ''
			for char in row[1]:
				if char == ' ':
					if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic' or prev_tag == 'newword'):
						tag = 'I-toxic'
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					string = ''
					prev_tag = tag
					tag = 'newword'
				elif char == '\n':
					if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic' or prev_tag == 'newword'):
						tag = 'I-toxic'
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					prev_tag = tag
					tag = 'newword'
					string = ''
					
				else:
					if not char.isalpha():
						if 'https' in string[0:8]:
							tag = 'B-toxic'
							f.write(char)
						else:
							if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic' or prev_tag == 'newword'):
								tag = 'I-toxic'
							if tag != 'newword':
								f.write('\t'+tag+'\n')
							string = ''
							prev_tag = tag
							tag = 'B-toxic'
							f.write(char)								
					else:	
						tag = 'B-toxic'
						f.write(char)
				string += char
			if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic' or prev_tag == 'newword'):
				tag = 'I-toxic'
			f.write('\t'+tag+'\n')	
			prev_tag = ''
			tag = '' 
			string = ''
			f.write('\n')
			
			f.write('\n') 
		elif row[0].strip() == 'spans':
				pass 
		else:
			spans = row[0].strip('][').split(', ') 
			spans = [int(ans) for ans in spans]
			i = 0
			tag = ''
			prev_tag = ''
			string = ''
			for char in row[1]:
				if char == ' ':
					if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'):
						tag = 'I-toxic'
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					string = ''
					prev_tag = tag
					tag = 'newword'
				elif char == '\n':
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					prev_tag = tag
					tag = 'newword'
					string = ''
					
				else:
					if i in spans:
						if tag == '0':
							f.write('\t'+tag+'\n')	
							string = ''
							prev_tag = tag
							tag = 'B-toxic'
							f.write(char)
							
					
						else:
							tag = 'B-toxic'
							f.write(char)
					else:
						if tag == 'B-toxic':
							if prev_tag == 'B-toxic' or prev_tag == 'I-toxic':
								tag = 'I-toxic'
							f.write('\t'+tag+'\n')	
							string = ''
							prev_tag = tag
							tag = '0'
							f.write(char)	
						else:
							if not char.isalpha():
								if 'https' in string[0:8]:
									tag = '0'
									f.write(char)
								else:
									if tag != 'newword':
										f.write('\t'+tag+'\n')
									string = ''
									prev_tag = tag
									tag = '0'
									f.write(char)								
							else:	
								tag = '0'
								f.write(char)
				i += 1
				string += char
			if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'):
				tag = 'I-toxic'
			f.write('\t'+tag+'\n')	
			prev_tag = ''
			tag = '' 
			string = ''
			f.write('\n')
			
						

				
				
			
					