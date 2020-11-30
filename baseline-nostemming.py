import csv
from nltk.tokenize import word_tokenize 
from nltk import ngrams
import re

# Function for finding the matches between a word in the sentence and a word in our bad words library
def match_finder(row, bad_words_lib):
    matches = [ word for word in word_tokenize(row[1]) if word.lower() in bad_words_lib] #check for each word in the message if it is in our library.
    matches += [ gram[0] + ' ' + gram[1] for gram in ngrams(word_tokenize(row[1]), 2) if gram[0].lower() + ' ' + gram[1].lower() in bad_words_lib ] #check for each bigram in the message if it is in our library.
    span = []
    for match in matches:
        find_matches = re.finditer(match, row[1]) #identifying the location of the matches, to be able to compare them to the gold label.
        matches_positions = [found.start() for found in find_matches]   
        for i in range(len(match)):
            for pos in matches_positions:
                span.append(pos + i )

    return span, matches


# Function for finding the number of right answers
def find_right_answer(row, answer): 
    right_answers = row[0].strip('][').split(', ') 
    if len(right_answers) == 1: #all characters of messages belong to the toxic span if list is empty
        right_answers = []
        if answer.lower() == 'y':
            i = 0
            for char in row[1]:
                right_answers.append(i)
                i +=1  
    right_answers = [int(ans) for ans in right_answers] #make sure all answers are integers
    
    return right_answers

# Function for counting the amount of correct and incorrect answers
def add_scores(right_answers, span, total_scores):
    correct = 0
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

    return total_scores


# Function for printing the score measurements
def scoring(total_scores):
    precision =  total_scores[0] / ( total_scores[0] + total_scores[2])
    recall = total_scores[0] / ( total_scores[0] + total_scores[1]) 
    print('precision:', precision)
    print('recall:', recall)
    print('f1-score:', 2 * ((precision * recall) / (precision + recall)))


def main():
    answer = input('Do you want to use full toxic messages (empty brackets)? y/n: ')
    total_scores = [0,0,0] #correct finds, missed finds, incorrect finds
    row = 0
    with open("tsd_trial.csv",  encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',') # read csv-file          
        bad_words_file = open("badwords.txt", encoding="utf8") #loading a library of bad words to identify toxicity
        bad_words_lib = [line.strip() for line in bad_words_file.readlines()] # creating a list of bad words

        for row in csv_reader:
                span, matches = match_finder(row, bad_words_lib)
                right_answers = find_right_answer(row, answer)
                total_scores = add_scores(right_answers, span, total_scores)
                    
                    
        scoring(total_scores)         
        
if __name__ == "__main__":
    main()
                    