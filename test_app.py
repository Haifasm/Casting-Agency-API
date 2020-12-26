import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

from dotenv import load_dotenv
load_dotenv()


class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        """ Define test variables and initialize app. """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE')
        setup_db(self.app, self.database_path)

        # get tokens from .env file using dotnet and create header
        self.Casting_Assistant_Token = {
            'Authorization': "Bearer " + os.getenv('CASTING_ASSISTANT') + ""}
        self.Casting_Director_Token = {
            'Authorization': "Bearer " + os.getenv('CASTING_DIRECTOR') + ""}
        self.Executive_Producer_Token = {
            'Authorization': "Bearer " + os.getenv('EXECUTIVE_PRODUCER') + ""}

        self.new_actor = {
            'name': 'Haifa',
            'age': '22',
            'gender': 'Female'
        }
        self.wrong_actor = {
            'age': '22',
            'gender': 'Female'
        }
        self.new_movie = {
            'title': 'The Imitation Game',
            'release': '2014-12-12',
            'description': 'Alan Turing, a British mathematician, joins the '
            'cryptography team to decipher the German enigma code.',
            'image_link': 'https://encrypted-tbn0.gstatic.com/images?'
            'q=tbn:ANd9GcQQ5vi9xgRkP0nk5aRn8tcGEGRnOQyM-aAS1ldqfQSi_69V1yfU'}
        self.wrong_movie = {
            'title': 'The Imitation Game',
            'description': 'Alan Turing, a British mathematician, joins the '
            'cryptography team to decipher the German enigma code.',
            'image_link': 'https://encrypted-tbn0.gstatic.com/images?'
            'q=tbn:ANd9GcQQ5vi9xgRkP0nk5aRn8tcGEGRnOQyM-aAS1ldqfQSi_69V1yfU'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Actor Test Cases

    '''
    Post Actor
    '''
    # 201 created

    def test1_create_actor(self):
        results = self.client().post('/actors', json=self.new_actor,
                                     headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # 422 create with missing mandotary attribute
    def test2_422_create_actor(self):
        results = self.client().post(
            '/actors',
            json=self.wrong_actor,
            headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    '''
    Get Actors
    '''
    # 200 ok

    def test3_get_actors(self):
        results = self.client().get('/actors?page=1',
                                    headers=self.Casting_Assistant_Token)

        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['number_of_actors'])

    # 404 page doesn't exist
    def test4_404_get_actors_beyond_pages(self):
        results = self.client().get(
            '/actors?page=2000',
            headers=self.Casting_Assistant_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'No actors found.')

    # Unauthorized
    def test5_401_get_all_actors(self):

        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    '''
    Patch Actor
    '''

    def test6_200_patch_actor(self):
        age_patch = {'age': '25'}
        results = self.client().patch('/actors/1', json=age_patch,
                                      headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)

    def test7_404_patch_actor(self):
        age_patch = {'age': '25'}
        results = self.client().patch(
            '/actors/100000',
            json=age_patch,
            headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    '''
    Delete Actor
    '''

    def test8_delete_actor(self):
        results = self.client().delete('/actors/1',
                                       headers=self.Casting_Director_Token)

        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '1')

    def test9_404_delete_actor(self):
        results = self.client().delete('/actors/2000',
                                       headers=self.Casting_Director_Token)

        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Movie Test Cases
    '''
    Post Movie
    '''
    # 201 created

    def test10_create_movie(self):
        results = self.client().post('/movies', json=self.new_movie,
                                     headers=self.Executive_Producer_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    # 422 create with missing mandotary attribute
    def test11_422_create_movie(self):
        results = self.client().post('/movies', json=self.wrong_movie,
                                     headers=self.Executive_Producer_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    '''
    Get Movies
    '''
    # 200 ok

    def test12_get_movies(self):
        results = self.client().get('/movies?page=1',
                                    headers=self.Executive_Producer_Token)

        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['number_of_movies'])

    # 404 page doesn't exist
    def test13_404_get_movies_beyond_pages(self):
        results = self.client().get(
            '/movies?page=2000',
            headers=self.Executive_Producer_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'No movies found.')

    # Unauthorized
    def test14_401_get_all_movies(self):

        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    '''
    Patch Movie
    '''

    def test15_200_patch_movie(self):
        date_patch = {'release_date': '2012-12-12'}
        results = self.client().patch('/movies/1', json=date_patch,
                                      headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)

    def test16_404_patch_movie(self):
        date_patch = {'release_date': '2012-12-12'}
        results = self.client().patch(
            '/movies/100000',
            json=date_patch,
            headers=self.Casting_Director_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    '''
    Delete Movie
    '''

    def test17_delete_movie(self):
        results = self.client().delete('/movies/1',
                                       headers=self.Executive_Producer_Token)

        data = json.loads(results.data)

        deleted_actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '1')

    def test18_404_delete_movie(self):
        results = self.client().delete(
            '/movies/2000', headers=self.Executive_Producer_Token)
        data = json.loads(results.data)

        self.assertEqual(results.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
