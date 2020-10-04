import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

total_scores = [0,0,0] #correct finds, missed finds, incorrect finds

with open("tsd_train.csv",  encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file
    line_count = 0          
    bad_words_file = open("badwords.txt", encoding="utf8") #loading a library of bad words to identify toxicity
    bad_words_lib = [line.strip() for line in bad_words_file.readlines()] # creating a list of bad words
    for row in csv_reader:
            matches = [ word for word in word_tokenize(row[1].lower()) if word in bad_words_lib] #check for each word in the message if it is in our library.
            matches += [ gram[0] + ' ' + gram[1] for gram in ngrams(word_tokenize(row[1].lower()), 2) if gram[0] + ' ' + gram[1] in bad_words_lib ] #check for each bigram in the message if it is in our library.
            span = []
            for match in matches:
                find_matches = re.finditer(match, row[1]) #identifying the location of the matches, to be able to compare them to the gold label.
                matches_positions = [found.start() for found in find_matches]   
                for i in range(len(match)):
                    for pos in matches_positions:
                        span.append(pos + i )
                
            right_answers = row[0].strip('][').split(', ') 
            #checking for true positives, false positives and false negatives. 
            correct = 0
            missed = 0
            incorrect = 0
            span = set(span) #filtering out double finds   
            if len(span) != 0:
                for loc in span:
                    if str(loc) in right_answers:
                        correct += 1
                total_scores[0] += correct
                total_scores[1] += (len(right_answers) - correct)
                total_scores[2] += (len(span) - correct)
            else:
                total_scores[1] += len(right_answers) 
    #calculating precision, recall and f1-score                 
    precision =  total_scores[0] / ( total_scores[0] + total_scores[2])
    recall = total_scores[0] / ( total_scores[0] + total_scores[1]) 
    print('precision:', precision)
    print('recall:', recall)
    print('f1-score:', 2 * ((precision * recall) / (precision + recall)))
                    
                
                
                
                

                
            
            