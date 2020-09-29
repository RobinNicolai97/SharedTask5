import csv
from nltk.tokenize import word_tokenize 

with open("tsd_trial.csv",  encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0          
    bad_words_file = open("badwords.txt", encoding="utf8")
    bad_words_lib = [line.strip() for line in bad_words_file.readlines()] 
    for row in csv_reader:
            print("in the sentence: {0}, spans: {1} are toxic \n".format(row[1], row[0])) 
            matches = [ word for word in word_tokenize(row[1]) if word in bad_words_lib] 
            print('Found the bad words:', matches, '\n')
            print('Which are spans:')
            for match in matches:
                position = row[1].find(match)
                span = []
                for i in range(len(match)):
                    span.append(position + i )
                print(span, '\n')
                
            
            