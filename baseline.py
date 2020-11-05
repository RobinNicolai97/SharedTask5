import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

#Comments on our baseline:
#- coverage of the lexicon  with respect to the training data- it does not seem that you have checked this potential shortcomings;

# - problems in the way you compute the offsets. I see that some messages contains newlines. 
#   Please double check if in these cases, the counting of the offsets of the characters is correctly implemented 
#   Double checked - Works ( SEE TEXTFILE WITH PROOF)
#

total_scores = [0,0,0] #correct finds, missed finds, incorrect finds
row = 0
with open("tsd_train.csv",  encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file
    line_count = 0          
    bad_words_file = open("badwords.txt", encoding="utf8") #loading a library of bad words to identify toxicity
    bad_words_lib = [line.strip() for line in bad_words_file.readlines()] # creating a list of bad words
    #f = open("missedwords.txt", "w", encoding="utf8")
    for row in csv_reader:
            matches = [ word for word in word_tokenize(row[1]) if word.lower() in bad_words_lib] #check for each word in the message if it is in our library.
            matches += [ gram[0] + ' ' + gram[1] for gram in ngrams(word_tokenize(row[1]), 2) if gram[0].lower() + ' ' + gram[1].lower() in bad_words_lib ] #check for each bigram in the message if it is in our library.
            span = []
            for match in matches:
                find_matches = re.finditer(match, row[1]) #identifying the location of the matches, to be able to compare them to the gold label.
                matches_positions = [found.start() for found in find_matches]   
                for i in range(len(match)):
                    for pos in matches_positions:
                        span.append(pos + i )
                
            right_answers = row[0].strip('][').split(', ') 
            if len(right_answers) == 1: #all characters of messages belong to the toxic span if list is empty
                right_answers = []
                #i = 0
                #for char in row[1]:
                  #  right_answers.append(i)
                   # i +=1  
            right_answers = [int(ans) for ans in right_answers] #make sure all answers are integers
            #checking for true positives, false positives and false negatives. 
            correct = 0
            missed = 0
            incorrect = 0
            spanlist = span
            span = set(span) #filtering out double finds 
            if len(span) != 0:
                for loc in span:
                    if loc in right_answers:
                        correct += 1
                total_scores[0] += correct
                total_scores[1] += (len(right_answers) - correct)
                total_scores[2] += (len(span) - correct)
            else:
                total_scores[1] += len(right_answers) 
            #for loc in span:
                #if loc in right_answers:
                    #right_answers.remove(loc)
			
            #string = ''
            #for ans in right_answers: 
                #string += row[1][int(ans)] 
            #f.write(string)
            #f.write('\n')
			    
				
			
    #calculating precision, recall and f1-score                 
    precision =  total_scores[0] / ( total_scores[0] + total_scores[2])
    recall = total_scores[0] / ( total_scores[0] + total_scores[1]) 
    print('precision:', precision)
    print('recall:', recall)
    print('f1-score:', 2 * ((precision * recall) / (precision + recall)))
    #f.close()
                    
                
                
                
                

                
            
            