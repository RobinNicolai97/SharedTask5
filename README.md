# SharedTask5
## Purporse
In our library, we work hard to make sure that bad words don't show up in places they shouldn't. So we make a system baseline meant for use in text generrators. And We found a text about bad words "badwords.txt" which can help us to fliter results from "tsd_train.csv".
## Get Started
Firstly, we quoted the method of word tokenizer to tokenize text into words. Then, we are going to calculate the score from the three aspects of correct finds, missed finds, and incorrect finds to evaluate the system. Next, we open and read the csv file prepared in advance. Now, we can load the library of bad words("badwords.txt") to detect toxicity and create a list of bad words. Then，we loop through the lines in the file.
