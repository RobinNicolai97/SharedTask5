# SharedTask5
## Background
For the final project, we chose the Task 5: Toxic Spans Detection. So in order to complete our final systems better, we made a system baseline and also provided an implementation of our system baseline for the task.
## Purporse
In our library, we work hard to make sure that bad words don't show up in places they shouldn't. So we make a system baseline meant for use in text generrators. And We found a text about bad words "badwords.txt" which can help us to fliter results from "tsd_train.csv".
## Install
This project uses python 3.8 and nltk library. Go check them out if you have them locally installed.
```
sudo pip install -U nltk
```
## Usage
Firstly, we quoted the method of word tokenizer to tokenize text into words. Then, we are going to calculate the score from the three aspects of correct finds, missed finds, and incorrect finds to evaluate the system. Next, we open and read the csv file prepared in advance. Now, we can load the library of bad words("badwords.txt") to detect toxicity and create a list of bad words. Then，we loop through the lines in the file.
Finally, we evaluated our system by calculating accuracy, precision, recall and f1-score.
## Run
Just type baseline.py, and make sure that "badwords.txt" and "tsd_train.csv" are in the same directory.
## Contributors
Nik van 't Slot, Yiming Han, Robin Nicolai, Jasper Bultman.
## License
