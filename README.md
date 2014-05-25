# Lazy Journal 

# v 0.1 created by jdegen (thegricean) on 01/01/2014

################
# What it does #
################

Allows "lazy" journalers to keep a regular journal by choosing answers from a dropdown menu.


###########
# Updates #
###########

05/25/2014 added default response adding functionality


##########
# Usage #
##########

python lazyjournal.py

This will open a window (likely kind of ugly because I have yet to improve the layout of the thing) with various questions that you can answer either by choosing an option from the drop-down menu or entering one manually. A complete set of answers to these questions constitutes a journal entry. Clicking "OK" will save the journal entry to a csv file, so you can use the data to at some point analyze your mood/behavior in R or other stats program if you are so inclined. 

The questions/answers are entirely determined by the user. The only piece of data the program saves by default is the system time. There are no pre-loaded questions, so the first time you run the program you'll have to add questions. If you need inspiration, have a look at the questions in examplequestions.txt.


############
# Features #
############

Add a new question by clicking on the "Add question" button.

Add a default response to a question by clicking on the "Add default" button.

Click the "OK" button to save your journal entry to the file result.csv. Note: the current version does _not_ check if you answered every question. It just saves whatever it finds for each question. If there are no questions, it saves only the system time.

Click the "Cancel" button to end the program without saving.


##################
# Idiosyncrasies #
##################

If you want to remove a journal entry, delete the appropriate line in result.csv.

If you want to remove a question, delete the appropriate line in questions.txt. Also delete the appropriate file in the library folder. You can find the file by checking the question's ID in questions.txt. The file to delete in the library folder is QUESTION-ID.txt

This thing is likely to be buggy - if sth weird happens, let me know! For safety, backups of both questions.txt and result.csv are saved as .questions.backup and .result.backup.


########
# TODO #
########

- include automatic deletion of questions
- allow for questions to have different kinds of answer inputs (eg sliders for ratings or checkboxes for multiple options)
- improve adding of default answers, eg by showing all the questions and their defaults and allowing user to select a question and add a default
- make prettier (eg, automatically calculate optimal row/column numbers)

