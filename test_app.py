import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

from dotenv import load_dotenv
load_dotenv()

#MY_ENV_VAR = os.getenv('MY_ENV_VAR')

#get tokens from .env file using dotnet
Casting_Assistant_Token = os.getenv('CASTING_ASSISTANT')
#Casting_Director_Token = os.environ.get('CASTING_DIRECTOR')
#Executive_Producer_Token = os.environ.get('EXECUTIVE_PRODUCER')

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        # set headers with tokens
        # self.headers_Casting_Assistant = {'Content-Type': 'application/json',
        #                                   'Authorization':
        #                                   Casting_Assistant_Token}

        # self.headers_Casting_Director = {'Content-Type':
        #                                  'application/json',
        #                                  'Authorization':
        #                                  Casting_Director_Token}

        # self.headers_Executive_Producer = {'Content-Type': 'application/json',
        #                                    'Authorization':
        #                                    Executive_Producer_Token}

        self.new_actor = {
            'name': 'Haifa',
            'age': '22',
            'gender': 'Female'
        }
        self.new_movie = {
            'title': 'The Imitation Game',
            'release': '2014-12-12',
            'description': 'Alan Turing, a British mathematician, joins the cryptography team to decipher the German enigma code.',
            'image_link': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQ5vi9xgRkP0nk5aRn8tcGEGRnOQyM-aAS1ldqfQSi_69V1yfU'
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

    '''
    Get Actors
    '''
    #200
    def test_get_actors(self):
        results = self.client().get('/actors', headers=Casting_Assistant_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['number_of_actors'])
    
    #404 page doesn't exist
    def test_404_get_actors_beyond_pages(self):
        results = self.client().get('/actors?page=2000')
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'No actors found.')
    
    '''
    Post Actor
    '''
    # def test_create_actor(self):
    #     results = self.client().post('/actors', json=self.new_actor)
    #     data = json.loads(results.data)

    #     self.assertEqual(results.status_code, 201) 
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    
    # def test_405_create_actor(self):
    #     results = self.client().post('/actors/1', json=self.new_question)
    #     data = json.loads(results.data)

    #     self.assertEqual(results.status_code, 405) 
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Method Not Allowed') 
    
    '''
    Delete Actor
    '''

    # def test_delete_question(self):
    #     results = self.client().delete('/actors/2')
    #     data = json.loads(results.data)

    #     deleted_question = Question.query.filter(Question.id == 2).one_or_none()

    #     self.assertEqual(results.status_code, 200) 
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['questions'])
    #     self.assertEqual(deleted_question, None)

    # def test_422_delete_question(self):
    #     results = self.client().delete('/actors/2000')
    #     data = json.loads(results.data)

    #     self.assertEqual(results.status_code, 422) 
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Unprocessable')

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

