#!/usr/bin/env python
# coding: utf-8



import csv
from nltk.tokenize import sent_tokenize, word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from nltk import ngrams
import re
import gensim
from tqdm import tqdm
import numpy as np

#I tried applying stemming to the messages. Recall for class 1 dropped 10%

def create_binary(file):
	with open(file,  encoding="utf8") as csv_file:
		messages = []
		labels = []
		tokens = []
		csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file
		counter = 0        
		for row in csv_reader:
			# Sherlock, here is the counter for how many messages the program takes into account
			# This is just for the development, so the program runs faster, and to prevent the memoryerror
			if counter >= 50:
				break
			else:
				if row[0].strip() == 'spans':
					pass
				else:
					word_cnt = 0
					sentences = sent_tokenize(row[1])
					new_message = []
					for sent in sentences:
						words = word_tokenize(sent)
						for word in words:
							new_message.append(word)
							tokens.append(word)
							word_cnt += 1

					span = row[0].strip('][').split(', ')

					# All characters of messages belong to the toxic span if list is empty
					# In these cases, we annotate every word as toxic
					if len(span) == 1:
						for i in range(word_cnt):
							labels.append(1)

					else:
						bad_words = ""
						for position in span:
							bad_words += row[1][int(position)]
							if str(int(position) + 1) not in span:
								bad_words += " "
						cuss_list = word_tokenize(bad_words)
						for word in new_message:
							if word in cuss_list:
								labels.append(1)
							else:
								labels.append(0)
					counter += 1

	return tokens, labels #first line is gibberish
	
def evaluate(Ytest, Yguess):
	print('\n accuracy score:', accuracy_score(Ytest, Yguess) )
	print('\n\n')
	print(classification_report(Ytest,Yguess))
	print('\n Confusion Matrix \n')
	print(confusion_matrix(Ytest,Yguess))



# a dummy function that just returns its input
def identity(x):
	return x	



# use option for characters
def getcharfea(trainx):
	trainx=[" ".join(list("".join(i.split(" ")))) for i in trainx]

# use bigram only
	vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity,ngram_range=(2, 2))
	res=vec.fit_transform(trainx).todense()
	return res,vec


def seq_vector(seq, embeddings_dict):
	tmp=np.array([])
	for i in seq:
		if i in embeddings_dict:
			tmp=np.concatenate([tmp,embeddings_dict[i]])
	tmp=list(tmp)
	if len(tmp)<320:
		while len(tmp)<320:
			tmp.append(0)
	else:
		tmp=tmp[:320]
	return tmp


def main():
	# remove stopwords

	stopword=[j.strip() for j in open("stopwords.txt").readlines()]

	#for classifying whole sentence toxic vs. part of sentence
	trainx, trainy = create_binary("tsd_train.csv")

	# Limit size of trainx for development speed purposes

	#unbalance: 7454, 485
	trainx=[" ".join([j for j in i.split(" ") if j not in stopword]) for i in trainx]
	testx, testy = create_binary("tsd_trial.csv")
	testx=[" ".join([j for j in i.split(" ") if j not in stopword]) for i in testx]

	train_char,vec=getcharfea(trainx)
	test_char=vec.transform(testx).todense()
	test_char.shape

	# use only unigram

	vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity,ngram_range=(1, 1))
	trainx_tf=vec.fit_transform(trainx)
	testx_tf=vec.transform(testx)

	trainx_tf=trainx_tf.todense()
	testx_tf=testx_tf.todense()
	trainx_tf.shape

	# The following lines create a dictionary containing the glove embeddings
	embeddings_dict = {}
	with open("glove.6B/glove.6B.50d.txt", 'r') as f:
	    for line in f:
	        values = line.split()
	        word = values[0]
	        vector = np.asarray(values[1:], "float32")
	        embeddings_dict[word] = vector


	glove_train=[]

	for i in tqdm(trainx):
		glove_train.append(seq_vector(i.split(" "), embeddings_dict))

	glove_test=[]
	for i in tqdm(testx):
		glove_test.append(seq_vector(i.split(" "), embeddings_dict))

	glove_train=np.array(glove_train)
	glove_test=np.array(glove_test)
	glove_train.shape


	# Because of MemoryError, I have excluded glove_train and train_char for now
	trainx=np.concatenate([trainx_tf,glove_train,train_char],axis=1)
	#trainx=np.concatenate([trainx_tf],axis=1)


	testx=np.concatenate([testx_tf,glove_test,test_char],axis=1)
	#testx=np.concatenate([testx_tf],axis=1)
	trainx.shape,testx.shape

	# classifier= svm.SVC(class_weight={0: 0.065, 1: 0.935})
	classifier = Pipeline([('cls', svm.SVC(class_weight={0: 0.065, 1: 0.935}))])
	print("Pipeline created")
	classifier.fit(trainx, trainy)
	print("Training done")
	Yguess = classifier.predict(testx)
	print("Predicting done")
	evaluate(testy, Yguess)
	# With the addition of the above features, the results all fit into category “0”

if __name__ == '__main__':
	main()
