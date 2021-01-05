#!/usr/bin/env python
# coding: utf-8



import csv
from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from nltk import ngrams
import re

#I tried applying stemming to the messages. Recall for class 1 dropped 10%

def create_binary(file):
	with open(file,  encoding="utf8") as csv_file:
		messages = []
		labels = []
		csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file         
		for row in csv_reader:
			if row[0].strip() == 'spans':
				pass
			span = row[0].strip('][').split(', ') 
			if len(span) == 1: #all characters of messages belong to the toxic span if list is empty
				labels.append(1)
			else:
				labels.append(0)
			messages.append(row[1].strip())
	return messages[1:], labels[1:] #first line is gibberish 
	
def evaluate(Ytest, Yguess):
	print('\n accuracy score:', accuracy_score(Ytest, Yguess) )
	print('\n\n')
	print(classification_report(Ytest,Yguess))
	print('\n Confusion Matrix \n')
	print(confusion_matrix(Ytest,Yguess))

# a dummy function that just returns its input
def identity(x):
    return x	
         
# def main():
# 	trainx, trainy = create_binary("tsd_train.csv") #for classifying whole sentence toxic vs. part of sentence
# 	#unbalance: 7454, 485
# 	testx, testy = create_binary("tsd_trial.csv")
# 	vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity,ngram_range=(1, 2))
# 	classifier = Pipeline([('vec', vec),('cls', svm.SVC(class_weight={0: 0.065, 1: 0.935}))])
# 	classifier.fit(trainx, trainy)
# 	Yguess = classifier.predict(testx)
# 	evaluate(testy, Yguess)
# main() 


# remove stopwords

stopword=[j.strip() for j in open("stopwords.txt").readlines()]
    




trainx, trainy = create_binary("tsd_train.csv") #for classifying whole sentence toxic vs. part of sentence
#unbalance: 7454, 485
trainx=[" ".join([j for j in i.split(" ") if j not in stopword]) for i in trainx]
testx, testy = create_binary("tsd_trial.csv")
testx=[" ".join([j for j in i.split(" ") if j not in stopword]) for i in testx]



# use option for characters
def getcharfea(trainx):
    trainx=[" ".join(list("".join(i.split(" ")))) for i in trainx]
    vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity,ngram_range=(2, 2))
    res=vec.fit_transform(trainx).todense()
    return res,vec




train_char,vec=getcharfea(trainx)
test_char=vec.transform(testx).todense()
test_char.shape




vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity,ngram_range=(1, 2))
trainx_tf=vec.fit_transform(trainx)
testx_tf=vec.transform(testx)



trainx_tf=trainx_tf.todense()
testx_tf=testx_tf.todense()
trainx_tf.shape




# Add glove embedding
import gensim
from glove import Glove
from glove import Corpus
corpus_model = Corpus()
corpus_model.fit([i.split(" ") for i in trainx], window=5)
print('Collocations: %s' % corpus_model.matrix.nnz)
glove = Glove(no_components=10, learning_rate=0.05)
glove.fit(corpus_model.matrix, epochs=11, no_threads=1, verbose=True)

glove.add_dictionary(corpus_model.dictionary)




from tqdm import tqdm
import numpy as np
def seq_vector(seq):
        import numpy as np
        tmp=np.array([])
        for i in seq:
            if i in glove.dictionary:
                tmp=np.concatenate([tmp,glove.word_vectors[glove.dictionary[i]]])
        tmp=list(tmp)
        if len(tmp)<320:
            while len(tmp)<320:
                tmp.append(0)
        else:
            tmp=tmp[:320]
        return tmp
glove_train=[]
for i in tqdm(trainx):
    glove_train.append(seq_vector(i.split(" ")))
glove_test=[]
for i in tqdm(testx):
    glove_test.append(seq_vector(i.split(" ")))
glove_train=np.array(glove_train)
glove_test=np.array(glove_test)
glove_train.shape



trainx=np.concatenate([trainx_tf,glove_train,train_char],axis=1)
testx=np.concatenate([testx_tf,glove_test,test_char],axis=1)
trainx.shape,testx.shape




# classifier= svm.SVC(class_weight={0: 0.065, 1: 0.935})
classifier = Pipeline([('cls', svm.SVC(class_weight={0: 0.065, 1: 0.935}))])
classifier.fit(trainx, trainy)
Yguess = classifier.predict(testx)
evaluate(testy, Yguess)


