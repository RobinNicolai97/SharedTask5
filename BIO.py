import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

f = open("BIO_train.txt", "w", encoding = 'utf8')
with open("tsd_train.csv",  encoding="utf8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file 
	for row in csv_reader:
		if row[0].strip() == '[]':  #full messages
			i = 0 # I explained the code I wrote in the part for non-full messages. To understand what I did, please check those comments!
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
						if len(string) >0 and not string[-1].isalpha():
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
		elif row[0].strip() == 'spans': #skip first line of file.
				pass 
		else:  # non full messages 
			spans = row[0].strip('][').split(', ') 
			spans = [int(ans) for ans in spans]
			i = 0
			tag = ''
			prev_tag = ''
			string = '' #with string I kept track of the interpunction and urls. 
			for char in row[1]:
				if char == ' ': # This code builds up a file char by char. Space is assumed to be start of new word. Thus: round up old word, give tag and start new.
					if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'): #if prev is B, then next is I.
						tag = 'I-toxic'
					if tag != 'newword': #to prevent double newline when using two spaces consecutive. 
						f.write('\t'+tag+'\n')	
					string = '' 
					prev_tag = tag
					tag = 'newword'
				elif char == '\n': #equivalent to spaces one, but no option for I-toxic. I don't believe it's the same span after a newline thats why. 
					if tag != 'newword':
						f.write('\t'+tag+'\n')	
					prev_tag = tag
					tag = 'newword'
					string = ''
					
				else:
					if i in spans:
						if tag == '0': #when you find toxic when the current word was already non toxic, its a different span. Thus, start new word.
							f.write('\t'+tag+'\n')	
							string = ''
							prev_tag = tag
							tag = 'B-toxic'
							f.write(char)
							
					
						else: #if not, no problem and just continue
							tag = 'B-toxic'
							f.write(char)
					else:
						if tag == 'B-toxic': # if the character is not in span but the word is toxic, char is not part of word. Newline!
							if prev_tag == 'B-toxic' or prev_tag == 'I-toxic':
								tag = 'I-toxic'
							f.write('\t'+tag+'\n')	
							string = ''
							prev_tag = tag
							tag = '0'
							f.write(char)	
						else:
							if not char.isalpha(): # the only way I could deal with interpunction, not perfect.
								if 'https' in string[0:8]: # if urls, no newline after interpunction.
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
								if len(string) >0 and not string[-1].isalpha(): #if the first character of word is interpunction, its probably not part of the word. 
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
			#new message! 
			if tag == 'B-toxic' and ( prev_tag == 'B-toxic' or prev_tag == 'I-toxic'):
				tag = 'I-toxic'
			f.write('\t'+tag+'\n')	
			prev_tag = ''
			tag = '' 
			string = ''
			f.write('\n')
			
						

				
				
			
					