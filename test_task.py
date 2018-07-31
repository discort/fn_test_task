import datetime
import unittest

from task import *


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.class_ = create_class()
        self.teacher = self.class_.teacher
        self.quiz_end_date = datetime.datetime(2018, 2, 1)

    def _create_questions(self, quiz, choices=None, answers=None):
        if not choices:
            choices = [
                {'q1': 'a1', 'q3': 'a3'},
                {'q2': 'a2', 'q4': 'a4'},
            ]
        if not answers:
            answers = [
                {'q3'},
                {'q2'},
            ]
        questions = []
        for ch, ans in zip(choices, answers):
            q = self.teacher.create_question(quiz=quiz, choices=ch, answers=ans)
            questions.append(q)
        return questions

    def test_create_class(self):
        """Testing if there are students and teacher in the class"""
        _class = self.class_
        assert isinstance(_class.teacher, Teacher)
        assert isinstance(_class.students[0], Student)

    def test_create_quiz(self):
        """
        Testing if teacher can create quizzes with questions
        """
        quiz = self.teacher.create_quiz()
        questions = self._create_questions(quiz=quiz)
        assert len(quiz.questions) == len(questions)

    def test_assign_quizzes(self):
        # Testing that student doesn't have quizzes
        quiz = self.teacher.create_quiz()
        student = self.class_.students[0]
        assert quiz not in student.quizzes

        # Testing that student have a quiz
        self.teacher.assign_quiz(quiz, student)
        assert quiz in student.quizzes

    def test_student_solve_quiz(self):
        # Assing quiz
        quiz = self.teacher.create_quiz()
        self._create_questions(quiz=quiz)
        student = self.class_.students[0]
        self.teacher.assign_quiz(quiz, student)

        # Test error case. Create a new quiz without assigning
        new_quiz = self.teacher.create_quiz()
        with self.assertRaises(Exception) as context:
            student.start_quiz(new_quiz)
        self.assertTrue('Quiz unavailable' in str(context.exception))

        quiz_result = student.start_quiz(quiz)

        # Success case, incorrect response
        question = quiz_result.read_question()
        result = quiz_result.answer_question(question, ['q1'])
        self.assertFalse(result)

        # Success case, correct response
        question = quiz_result.read_question()
        # Set is unordered, so result may change
        answer = 'q2' if 'q2' in question.choices else 'q3'
        result = quiz_result.answer_question(question, [answer])
        self.assertTrue(result)

    def test_teacher_calculate_total_grade_over_semester(self):
        quiz = self.teacher.create_quiz()
        self._create_questions(quiz=quiz)
        for student in self.class_.students:
            self.teacher.assign_quiz(quiz, student)

            quiz_result = student.start_quiz(quiz)
            question = quiz_result.read_question()
            answer = 'q2' if 'q2' in question.choices else 'q3'
            quiz_result.answer_question(question, [answer])
            student.finish_quiz(quiz_result, end_date=self.quiz_end_date)

        result = self.teacher.calculate_semester_total()
        self.assertEquals(len(result), len(self.class_.students))
        for item in result:
            self.assertEquals(item['total'], 1)
