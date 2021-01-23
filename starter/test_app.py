
  
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the CastingAgency test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

## Roles and auth headers 
        self.casting_assistant = {
            'Authorization': 'Bearer ' + os.environ.get('ASSISTANT_TOKEN')}
        self.casting_director = {
            'Authorization': 'Bearer ' + os.environ.get('DIRECTOR_TOKEN')}
        self.executive_producer = {
            'Authorization': 'Bearer ' + os.environ.get('PRODUCER_TOKEN')}

    def tearDown(self):
        """Executed after reach test"""
        pass

#  One test for error behavior of GET ACTORS end point 
    def test_get_actors_failure(self):
        """ Test get actors failure """
        # get response with no actors in the database 
        db.session.query(Actor).delete()
        db.session.commit()
        response = self.client().get('/actors', headers=self.casting_assistant)
        # 404 since no actors are stored in DB
        self.assertEqual(response.status_code, 404)

# ONE Success for GET movies end point
    def test_get_movies_success(self):
        """ Test get movies success """
#Add a new movie 
        movie = Movie( title='Modren family', release_date="Mon, 23 Jan 2013 12:00:00 GMT")
        movie.insert()

        # get response data + adding headers
        response = self.client().get('/movies', headers=self.casting_assistant)

        # check success value, status_code and if there is an actors list
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json.loads(response.data)['movies']))
# One test for error behavior of GET Movies
    def test_get_movies_failure(self):
        """ Test get actors failure """
        # get response with no movies in the database 
        db.session.query(Movie).delete()
        db.session.commit()
        response = self.client().get('/movies', headers=self.casting_assistant)
        # 404 since no actors are stored in DB
        self.assertEqual(response.status_code, 404) 

# ONE Success for GET actors end point
    def test_get_actors_success(self):
        """ Test get actors success """
#Add a new actor 
        actor= Actor( name='Hatounnnn', age=23, gender='female')
        actor.insert()

        # get response data + adding headers
        response = self.client().get('/actors', headers=self.casting_assistant)

        # check success value, status_code and if there is an actors list
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json.loads(response.data)['actors']))
# ONE Success for DELETE actors end point
    def test_delete_actor_success(self):
        """ Test delete actor success """
        #add an actor
        actor_test = Actor(
            name='hissah',
            age=50,
            gender='female')
        actor_test.insert()
        # get the number of actors before deleting the actor
        actors_total_before = len(Actor.query.all())
        # send request to delete the last created actor
        response = self.client().delete('/actors/' + format(actor_test.id),
                                        headers=self.casting_director)
        # get the number of actors after deleting the actor
        actors_total_after = len(Actor.query.all())

        # check success value, status_code
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual(response.status_code, 200)
        # compare actors_total_before and actors_total_after to check
        # if the actor is deleted
        self.assertFalse(actors_total_before == actors_total_after)
        self.assertTrue(actors_total_before > actors_total_after)
# One test for error behavior of DELETE Actor
    def test_delete_actor_unauthorized(self):
        """ Test delete actor failure """
        # get response data
        response = self.client().delete('/actors/' + format(100),
                                        headers=self.casting_assistant)

        # check success value, status_code
        self.assertEqual(response.status_code, 401)

# ONE Success for DELETE movie end point
    def test_delete_movie_success(self):
        """ Test delete movie success """

        # add a movie
        movie_test = Movie(
            title='insatnt family',
            release_date="mon, 23 Jan 2013 12:00:00 GMT")
        movie_test.insert()

        # get the number of movies before deleting 
        movies_total_before = len(Movie.query.all())
        # send request to delete the added movie
        response = self.client().delete('/movies/' + format(movie_test.id),
                                        headers=self.executive_producer)
        # get the number of movies after deleting 
        movies_total_after = len(Movie.query.all())

        # check success value, status_code
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual(response.status_code, 200)
        # compare actors_total_before and actors_total_after
        self.assertFalse(movies_total_before == movies_total_after)
        self.assertTrue(movies_total_before > movies_total_after)

# One test for error behavior of DELETE Movie
    def test_delete_movie_failure(self):
        """ Test delete movie failure """
        # get response data
        response = self.client().delete('/movies/' + format(100),
                                        headers=self.executive_producer)

        # 422 since the provided ID is wrong
        self.assertEqual(response.status_code, 422)

    def test_delete_movie_unauthorized(self):
        """ Test delete movie failure """
        # get response data
        response = self.client().delete('/movies/' + format(100),
                                        headers=self.casting_director)

        # Unauthorized since the casting_director
        # doesn't have permission to delete an actor
        self.assertEqual(response.status_code, 401)

# ONE Success for ADD Actor end point
    def test_create_new_actor_success(self):
        """ Test create a actor obj success """
        # get the number of actors before adding actor
        actors_total_before = len(Actor.query.all())

      
        actor_test = Actor(name='Lujain', age=25, gender='female')

        # load response data
        response = self.client().post('/actors', json=actor_test.format(),
                                      headers=self.casting_director)

        actors_total_after = len(Actor.query.all())

        # check success value, status_code
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual(response.status_code, 200)

        # compare actors_total_before and actors_total_after
        self.assertFalse(actors_total_before == actors_total_after)
        self.assertTrue(actors_total_before < actors_total_after)
# One test for error behavior of Add Actor
    def test_create_actor_failure(self):
        """ Test create actor obj failure """
        # get the number of actors after creating a new obj
        actors_total_before = len(Actor.query.all())

        # load response data
        response = self.client().post('/actors', json={},
                                      headers=self.casting_director)

        # get the number of actors after creating a new obj
        actors_total_after = len(Actor.query.all())

        # 422 since not data was provided in the request
        self.assertEqual(response.status_code, 422)
        # as no obj was created the actors_total_before
        # should be equal to actors_total_after
        self.assertTrue(actors_total_before == actors_total_after)
# ONE Success for ADD Movie end point
    def test_create_movie_success(self):
        """ Test create a movie obj success """
        # get the number of movies before creating a new obj
        movies_total_before = len(Movie.query.all())

        # create a new obj
        movie_test = Movie(
            title='Soul',
            release_date="mon, 23 Jan 2013 12:00:00 GMT")

        # load response data
        response = self.client().post('/movies', json=movie_test.format(),
                                      headers=self.executive_producer)

        # get the number of movies after creating a new obj
        movies_total_after = len(Movie.query.all())

        # status_code
        self.assertEqual(response.status_code, 201)

        # compare movies_total_before and movies_total_after
        self.assertFalse(movies_total_before == movies_total_after)
        self.assertTrue(movies_total_before < movies_total_after)

# One test for error behavior of Add Movie
    def test_create_movies_failure(self):
        """ Test create movie obj failure """
        # get the number of actors after creating a new obj
        movies_total_before = len(Movie.query.all())

        # load response data
        response = self.client().post('/movies', json={},
                                      headers=self.executive_producer)

        # get the number of movies after creating a new obj
        movies_total_after = len(Movie.query.all())

        self.assertEqual(response.status_code, 400)
        # as no obj was created the movies_total_before should
        # be equal to movies_total_after
        self.assertTrue(movies_total_before == movies_total_after)

# ONE Success for update actor end point
    def test_update_actor_success(self):
        """ Test update actor success """
        actor_test = Actor(
            name='Hatoun',
            age=23,
            gender='female')
        actor_test.insert()

        # load response data
        response = self.client().patch('/actors/' + format(actor_test.id),
                                       json={'name': "name1"},
                                       headers=self.casting_director)
        # Load the data using json.loads of the response

        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual('name1', json.loads(response.data)['actor']['name'])
        self.assertEqual(response.status_code, 200)
# One test for error behavior of update actor
    def test_update_actor_failure(self):
        """ Test update actor failure """
        # send request with wrong actor ID
        response = self.client().patch('/actors/' + format(100),
                                       json={'name': "name1"},
                                       headers=self.casting_director)
        # Load the data using json.loads of the response
        self.assertEqual(response.status_code, 404)


    def test_update_movie_success(self):
        """ Test update movie success """
        movie_test = Movie(
            title='Soul',
            release_date="mon, 23 Jan 2013 12:00:00 GMT")
        movie_test.insert()

        # load response data
        response = self.client().patch('/movies/' + format(movie_test.id),
                                       json={'title': "title1"},
                                       headers=self.executive_producer)
        # Load the data using json.loads of the response
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEqual('title1', json.loads(response.data)['movie']['title'])
        self.assertEqual(response.status_code, 200)

    def test_update_movie_failure(self):
        """ Test update movie failure """

        # load response data
        response = self.client().patch('/movies/' + format(100),
                                       json={'title': "title1"},
                                       headers=self.executive_producer)
        # Load the data using json.loads of the response
        self.assertEqual(response.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()



