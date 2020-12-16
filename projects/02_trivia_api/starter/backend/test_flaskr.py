import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '123456789', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Test question',
            'answer': 'Test',
            'difficulty': 1,
            'category': 1
        }

        self.quiz = {
            'quiz_category': {
                'id': '1',
                'type': 'Science'
            },
            'previous_questions': []
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']) , 6)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        self.assertEqual(res.status_code, 200)

    def test_get_questions_404_if_beyond_page(self):
        res = self.client().get('/questions?page=100000')
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']), 0)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)

    def test_add_question_fail(self):
        res = self.client().post('/questions', json={})
        self.assertEqual(res.status_code, 400)

    def test_delete_question(self):
        getQuestions = self.client().get('/questions?page=1')
        data = json.loads(getQuestions.data)
        idToDelete = data['questions'][0]['id']
        res = self.client().delete('/questions/' + str(idToDelete))
        data = json.loads(res.data)
        self.assertEqual(int(data['deleted']), idToDelete)
    
    def test_delete_question_fail(self):
        idToDelete = 10000000
        res = self.client().delete('/questions/' + str(idToDelete))
        self.assertEqual(res.status_code, 404)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions?page=1')
        self.assertEqual(res.status_code, 200)

    def test_get_question_by_category_fail(self):
        res = self.client().get('/categories/100/questions?page=1')
        self.assertEqual(res.status_code, 400)

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.quiz)
        self.assertEqual(res.status_code, 200)

    def test_quizzes_fail(self):
        res = self.client().post('/quizzes', json={})
        self.assertEqual(res.status_code, 400)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()