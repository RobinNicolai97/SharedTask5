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
         
def main():
	trainx, trainy = create_binary("tsd_train.csv") #for classifying whole sentence toxic vs. part of sentence
	#unbalance: 7454, 485
	testx, testy = create_binary("tsd_trial.csv")
	vec = TfidfVectorizer(preprocessor = identity, tokenizer = identity)
	classifier = Pipeline([('vec', vec),('cls', svm.SVC(class_weight={0: 0.065, 1: 0.935}))])
	classifier.fit(trainx, trainy)
	Yguess = classifier.predict(testx)
	evaluate(testy, Yguess)
main() 
