#!/usr/bin/env python3
"""
python3 main.py

Simple dictionary lookup for bad words, outputs a .txt file with character offsets.
"""
import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
from nltk.stem import PorterStemmer
import re



def main():
	stemmer = PorterStemmer()
	row = 0
	with open("tsd_test.csv",  encoding="utf8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file
		line_count = 0          
		bad_words_file = open("badwords.txt", encoding="utf8") #loading a library of bad words to identify toxicity
		bad_words_lib = []
		f = open("system_output.txt", "w+")
		for line in bad_words_file.readlines(): #stemming the words in the library
			linetext = []
			for word in line.split():
				linetext.append(stemmer.stem(word.strip()))
			bad_words_lib.append(' '.join(linetext))
		bad_words_lib = set(bad_words_lib)

		for row in csv_reader:
			matches = [ word for word in word_tokenize(row[0]) if stemmer.stem(word.lower()) in bad_words_lib] #check for each word in the message if it is in our library.
			matches += [ gram[0] + ' ' + gram[1] for gram in ngrams(word_tokenize(row[0]), 2) if stemmer.stem(gram[0].lower()) + ' ' + stemmer.stem(gram[1].lower()) in bad_words_lib ] #check for each bigram in the message if it is in our library.
			span = []
			for match in matches:
				try:
					find_matches = re.finditer(match, row[0]) #identifying the location of the matches, to be able to compare them to the gold label.
				except:
					pass

				matches_positions = [found.start() for found in find_matches]   
				for i in range(len(match)):
					for pos in matches_positions:
						span.append(pos + i )

			f.write(str(span) + "\n")

		f.close()

if __name__ == '__main__':
	main()