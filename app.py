import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import *


def create_app(test_config=None):
  # create and configure the app
 app = Flask(__name__)
 app.debug = True
 setup_db(app)
 CORS(app)
 
 @app.after_request
 def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

#####

##Main route## 
 @app.route('/')
 def index():
   return jsonify({
            'message': 'Main route home page'
        })
## Firt GET ##
##GET all movies##
 @app.route('/movies')
 @requires_auth('get:movies')
 def get_all_movies(jwt):
    try:
         movies = Movie.query.all()
         if len(movies) == 0:
            abort(404)
         else:
            movies = [movie.format() for movie in movies]
         return jsonify({
            'success': True,
            'movies': movies
            }), 200 
    except Exception as e:
            abort(404)

###SECOND GET### 
 @app.route('/actors')
 @requires_auth('get:actors')
 def get_actors(jwt):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        else:
            actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actors
                })

#ADD MOVIE
 @app.route('/movies', methods=['POST'])
 @requires_auth('post:movies')
 def add_movie(payload):
      title = request.get_json().get('title')
      release_date = request.get_json().get('release_date')
      try:
        data = title and release_date
        if not data:
            abort(400)
      except (TypeError, KeyError):
        abort(400)

      try:
        Movie(title=title, release_date=release_date).insert()
        return jsonify({
            'success': True,
            'movie': title
        }), 201
      except:
        abort(422)
### ADD ACTOR ### 

 @app.route("/actors", methods=['POST'])
 @requires_auth('post:actors')
 def create_actor(payload):
      # validation
      if 'name' in request.get_json() and 'age' in request.get_json() \
         and 'gender' in request.get_json():
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']

        new_actor = Actor(
            name=name,
            age=age,
            gender=gender)
        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
            })
      else:
          abort(422)



## DELETE ACTOR ### 

 @app.route("/actors/<int:actor_id>", methods=['DELETE'])
 @requires_auth('delete:actors')
    # This endpoint is to delete an actor
 def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id
                })
        except BaseException:
            abort(422)

## DELETE MOVIE ### 
 @app.route("/movies/<int:movie_id>", methods=['DELETE'])
 @requires_auth('delete:movies')
 def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id
                })
        except BaseException:
            abort(422)
### PATCH ACTOR ### 

 @app.route('/actors/<int:actor_id>', methods=['PATCH'])
 @requires_auth('patch:actors')
 def update_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            # check if title in post data
            if 'name' in request.get_json():
                name = request.get_json()['name']
                actor.name = name
            # check if name in post data
            if 'age' in request.get_json():
                age = request.get_json()['name']
                actor.age = age
            # check if gender in post data
            if 'gender' in request.get_json():
                gender = request.get_json()['gender']
                actor.gender = gender

            actor.update()
            return jsonify({'success': True, 'actor': actor.format()})

        except BaseException:
            # if the object is not exist a 404 error will be returned
            abort(404)


### PATCH MOVIE ###  
 @app.route('/movies/<int:movie_id>', methods=['PATCH'])
 @requires_auth('patch:movies')
 def update_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            # check if title in post data
            if 'title' in request.get_json():
                title = request.get_json()['title']
                movie.title = title
            # check if release_date in post data
            if 'release_date' in request.get_json():
                release_date = request.get_json()['release_date']
                movie.release_date = release_date

            movie.update()
            return jsonify({'success': True, 'movie': movie.format()})

        except BaseException:
            # if the object is not exist a 404 error will be returned
            abort(404)
####
   
####
######

 return app

app = create_app()

# Default port:
if __name__ == '__main__':
    app.run()
