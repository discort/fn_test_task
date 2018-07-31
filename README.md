# FN test task

There are Teachers  
There are Students  
Students are in classes that teachers teach  
Teachers can create multiple quizzes with many questions (each question is multiple choice)  
Teachers can assign quizzes to students  
Students solve/answer questions to complete the quiz, but they don't have to complete it at once. (Partial submissions can be made).  
Quizzes need to get graded  
For each teacher, they can calculate each student's total grade accumulated over a semester for their classes  

## Installation

1. clone this repo onto your machine
2. `cd` into the directory of the checkout
3. `virtualenv -p python3 env`
4. `source env/bin/activate`
5. `pip install -r requirements.txt`

## To run the tests

    py.test test_task.py