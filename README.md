## 1	Background

For the final project, we chose the Task 5: Toxic Spans Detection. In order to complete our final systems better, we made a system baseline and also provided an implementation of our system baseline for the task. In our library, we work hard to make sure that bad words don't show up in places they shouldn't. We make a system baseline meant for use in text generators. We found a list of banned words that Google used for their Android system . We call it "badwords.txt". It can help us filter results from "tsd_train.csv".

## 2	Install

This project uses python 3.8 and nltk library. Go check them out if you have them locally installed.

sudo pip install -U nltk

## 3	Usage

We are going to calculate the score from the three aspects of correct finds, missed finds, and incorrect finds to evaluate the system. We open and read the csv file provided by the task organizers, "tsd_train.csv", which they prepared in advance.

Now, we can load the library of bad words("badwords.txt") to detect toxicity and create a list of bad words. For every line in the csv-file, we tokenize it and make sure it is lowercased to guarantee that matching words will always be found. We check for each individual word if it exists in our library of bad words. We do the same for all bigrams that we make out of the separate lines. The bigrams are being made using nltk's ngrams function.

Next we retrieve all position of bad words found in the line with the regular expression 
finditer function. It returns all positions or indices in the line of the matches found. This 
function also makes sure that the correct position of the match is found, when it occurs multiple times in one line. Since this function only returns the starting position of the matches, we created a small function to also retrieve positions for every single character in the found matches. We need this to be able to review our system on the gold standard, which contains the complete spans for all toxic expressions.

Then, we check for true positives, false positives and false negatives. We do this by comparing our model's found character span locations to those of the gold standard. Matching character locations will be concerned correct. Locations that are in the gold standard but not found by our model will be considered missed. Finally, character locations found by our model that are not in the gold standard will be classified as incorrect. Finally, using this information, we evaluated our system by calculating precision, recall and f1-score.

The baseline results in a precision of 0.67, a recall of 0.1 and an f-score of 0.17. The extremely low f-score largely stems from the fact that dictionary lookup only accounts for explicit toxicity and not implicit toxicity. In the gold label, implicitly toxic tweets are considered to be entirely toxic, so the recall decreases considerably.

## 4	Run

python3 baseline.py

Run the above line in the terminal. Make sure that "badwords.txt" and "tsd_train.csv" are in the same directory as the baseline program.
