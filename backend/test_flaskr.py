import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app
from flaskr.models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = f"postgresql://root:toor@172.22.192.1:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

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
        res = self.client.get('/categories')
        self.assertEqual(res.status_code, 200)

    def test_get_unexist_categories(self):
        res = self.client.get('/categories/99')
        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client.get('/questions')
        self.assertEqual(res.status_code, 200)
        
    def test_get_unexist_questions_page(self):
        res = self.client.get('/questions?page=1000')
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client.delete('/questions/2')
        self.assertEqual(res.status_code, 200)

    def test_delete_unexist_question(self):
        res = self.client.delete('/questions/1')
        self.assertEqual(res.status_code, 404)
        
    def test_create_new_question(self):
        data = {
            'question': 'test',
            'answer': 'test',
            'difficulty': '1',
            'category': 4
        }
        json_data = json.dumps(data)
        res = self.client.post('/questions', data=json_data)
        self.assertEqual(res.status_code, 201)

    def test_create_an_exist_question(self):
        data = {
            'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
            'answer': 'Apollo 13',
            'difficulty': '4',
            'category': 4
        }
        json_data = json.dumps(data)
        res = self.client.post('/questions', data=json_data)
        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_catigory(self):
        res = self.client.get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)
    
    def test_get_questions_by_unexist_catigory(self):
        res = self.client.get('/categories/10/questions')
        self.assertEqual(res.status_code, 404)

    def test_search_questions(self):
        data = json.dumps({'searchTerm': 'who'})
        res = self.client.post('/questions/search', data=data)
        self.assertEqual(res.status_code, 200)
    
    def test_search_questions_for_unexist_term(self):
        data = json.dumps({'searchTerm': 'hazem'})
        res = self.client.post('/questions/search', data=data)
        self.assertEqual(res.status_code, 404)

    def test_play_quiz(self):
        json_data = json.dumps({
            'previous_questions': [],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 5
            }
        })
        res = self.client.post('/quizzes', data=json_data)
        self.assertEqual(res.status_code, 200)

    def test_play_quiz_with_unesist_catigory(self):
        json_data = json.dumps({
            'previous_questions': [],
            'quiz_category': {
                'type': 'test',
                'id': 1000
            }
        })
        res = self.client.post('/quizzes', data=json_data)
        data = json.loads(res.data)
        self.assertEqual(data['question'], None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()