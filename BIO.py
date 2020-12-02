import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

f = open("BIO_train.txt", "w", encoding = 'utf8')
with open("tsd_train.csv",  encoding="utf8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file 
	for row in csv_reader:
		if row[0].strip() == '[]':
			count = 0
			for word in word_tokenize(row[1]):
				if count == 0:
					f.write(word + '\t' + 'B-toxic\n')
				else:
					f.write(word + '\t' + 'I-toxic\n')
				count += 1
			f.write('\n') 
		elif row[0].strip() == 'spans':
				pass 
		else:
			spans = row[0].strip('][').split(', ') 
			spans = [int(ans) for ans in spans]
			i = 0
			tag = ''
			prev_tag = ''
			for char in row[1]:
				if char == ' ':
					if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'):
						tag = 'I-toxic'
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					prev_tag = tag
					tag = 'newword'
				elif char == '\n':
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					prev_tag = tag
					tag = 'newword'
					
				else:
					if i in spans:
						if tag == 'O':
							f.write('\t'+tag+'\n')	
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
							prev_tag = tag
							tag = 'O'
							f.write(char)
							
							
						else:
							tag = 'O'
							f.write(char)
				i += 1
			if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'):
				tag = 'I-toxic'
			f.write('\t'+tag+'\n')	
			prev_tag = ''
			tag = '' 
			f.write('\n')
			
						

				
				
			
					