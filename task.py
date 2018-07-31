import datetime
import itertools


SEMESTER_START_DATE = datetime.date(2018, 1, 1)
SEMESTER_END_DATE = datetime.date(2018, 7, 1)


def create_teacher():
    return Teacher()


def create_student():
    return Student()


def create_class(teacher=None, students=None, default_students_number=10):
    if not teacher:
        teacher = create_teacher()

    if not students:
        students = []
        for _ in range(default_students_number):
            student = create_student()
            students.append(student)

    class_ = Class(teacher=teacher, students=students)
    teacher.classes.append(class_)
    return class_


class Teacher:
    def __init__(self):
        self.classes = []

    def create_quiz(self):
        return Quiz(teacher=self)

    def create_question(self, quiz, choices, answers, grade=1):
        question = Question(quiz=quiz, choices=choices, answers=answers, grade=grade)
        quiz.questions.add(question)
        return question

    def assign_quiz(self, quiz, student):
        student.quizzes.add(quiz)

    def calculate_total(self, start_date, end_date):
        result = []
        for class_ in self.classes:
            data = self.calculate_total_by_class(class_, start_date, end_date)
            result.extend(data)

        return result

    def calculate_total_by_class(self, class_, start_date, end_date):
        result = []
        for student in class_.students:
            student_total = self._get_student_total(student, start_date, end_date)
            data = {'student': student, 'total': student_total}
            result.append(data)
        return result

    def _get_student_total(self, student, start_date, end_date):
        student_total = []
        student_results = student.get_results()
        for k, v in student_results.items():
            if start_date <= k <= end_date:
                student_total.append(v)
        return sum(student_total)

    def calculate_semester_total(self):
        return self.calculate_total(SEMESTER_START_DATE, SEMESTER_END_DATE)


class Student:
    def __init__(self):
        self.quizzes = set()
        self.quizzes_result = []

    def start_quiz(self, quiz):
        if quiz not in self.quizzes:
            raise Exception("Quiz unavailable!")

        self.quizzes.remove(quiz)
        return QuizResult(quiz=quiz, student=self)

    def finish_quiz(self, quiz_result, end_date=None):
        if not end_date:
            end_date = datetime.datetime.now()

        quiz_result.end_date = end_date
        self.quizzes_result.append(quiz_result)

    def get_results(self):
        if not self.quizzes_result:
            return

        result = {}
        data = sorted(self.quizzes_result, key=lambda x: x.end_date)
        for k, group in itertools.groupby(data, key=lambda x: x.end_date.date()):
            result[k] = sum([item.result for item in group])

        return result


class QuizResult:
    def __init__(self, quiz, student):
        """
        quiz: Quiz obj
        student: Student obj
        """
        self.quiz = quiz
        self.student = student
        self.questions = (q for q in self.quiz.questions)

        self.result = 0
        self.end_date = None

    def read_question(self):
        """Returns Question obj"""
        try:
            return next(self.questions)
        except StopIteration:
            return

    def answer_question(self, question, answer=None):
        if not question or not answer:
            return

        if set(answer) == question.answers:
            self.result += question.grade
            return True
        return False


class Class:
    def __init__(self, teacher, students):
        """
        teacher: Teacher obj
        students: list of Student objs
        """
        self.teacher = teacher
        self.students = students


class Quiz:
    def __init__(self, teacher, questions=None):
        """
        teacher: Teacher obj
        questions: set of Question objs
        """
        self.teacher = teacher
        self.questions = questions
        if not questions:
            self.questions = set()


class Question:
    def __init__(self, quiz, choices=None, answers=None, grade=None):
        """
        quiz: Quiz obj
        choices: dict of str
        answers: set of str
        grade: int or float
        """
        self.quiz = quiz
        self.choices = choices
        self.answers = answers
        self.grade = grade
