import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import *
from auth import *

# number of actors or movies per page
RESULTS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginate(request, selection):
        # selection will be either actor or movie to be able to call .format()

        # use request to get the page number or 1 if no current page
        page = request.args.get('page', 1, type=int)

        # srart and end of the results
        start = (page - 1) * RESULTS_PER_PAGE
        end = start + RESULTS_PER_PAGE

        results = [obj.format() for obj in selection]
        current_results = results[start:end]

        return current_results

    @app.route('/')
    def home():
        return jsonify({
            'Welcome': 'Casting Agency API by Haifa Almansour'
        })

    # Actor

    # GET all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actor')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        results = paginate(request, actors)

        if len(results) == 0:
            abort(404, {'message': 'No actors found.'})

        return jsonify({
            'success': True,
            'actors': results,
            'number_of_actors': len(Actor.query.all())
        }), 200

    # GET specific actor
    @app.route('/actors/<actor_id>', methods=['GET'])
    @requires_auth('get:actor')
    def get_actor(payload, actor_id):

        if not actor_id:
            abort(400, {'message': 'No actor_id provided.'})

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404, {'message': 'Actor was not found.'})

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200

    # POST actor
    @app.route('/actors', methods=['POST'])
    # @requires_auth('post:actor')
    def create_actor():
        data = request.get_json()

        if not data:
            abort(400, {'message': 'Invalid JSON data.'})

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        description = data.get('description', None)
        image_link = data.get('image_link', None)

        # validate parameters, description and image_link are optional
        if not name:
            abort(422, {'message': 'Error: Missing name.'})
        if not age:
            abort(422, {'message': 'Error: Missing age.'})
        if not gender:
            abort(422, {'message': 'Error: Missing gender.'})

        actor = Actor(
            name=name,
            age=age,
            gender=gender,
            description=description,
            image_link=image_link)
        actor.create()

        return jsonify({
            'success': True,
            'created': actor.id
        }), 201

    # PATCH actor
    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, actor_id):
        data = request.get_json()
        selected_actor_id = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        # validate
        if not actor_id:
            abort(404, {'message': 'No actor_id provided.'})
        if not data:
            abort(400, {'message': 'Invalid JSON data.'})
        if not selected_actor_id:
            abort(
                404, {
                    'message': 'Actor with that id '
                    'was not found'.format(actor_id)})

        # get updated variables from data
        name = data.get('name', selected_actor_id.name)
        age = data.get('age', selected_actor_id.age)
        gender = data.get('gender', selected_actor_id.gender)
        description = data.get('description', selected_actor_id.description)
        image_link = data.get('image_link', selected_actor_id.image_link)

        # assign the variable to the selected actor
        selected_actor_id.name = name
        selected_actor_id.age = age
        selected_actor_id.gender = gender
        selected_actor_id.description = description
        selected_actor_id.image_link = image_link

        # UPDATE DATBASE
        selected_actor_id.update()

        # RETURN RESULTS
        return jsonify({
            'success': True,
            'updated': selected_actor_id.id,
            'actor': [selected_actor_id.format()]
        }), 200

    # DELETE actor
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor_id:
            abort(400, {'message': 'No actor_id provided.'})

        if not actor:
            abort(404, {'message': 'Actor was not found.'})

        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        }), 200

    #########################################
    # GET movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movie')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        results = paginate(request, movies)

        if len(results) == 0:
            abort(404, {'message': 'No movies found.'})

        return jsonify({
            'success': True,
            'movies': results,
            'number_of_movies': len(Movie.query.all())
        }), 200

    # GET specific movie
    @app.route('/movies/<movie_id>', methods=['GET'])
    @requires_auth('get:movie')
    def get_movie(payload, movie_id):

        if not movie_id:
            abort(400, {'message': 'No movie_id.'})

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404, {'message': 'Movie was not found.'})

        return jsonify({
            'success': True,
            'movie': [movie.format()]
        }), 200

    # POST movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        data = request.get_json()

        if not data:
            abort(400, {'message': 'Invalid JSON data.'})

        title = data.get('title', None)
        release = data.get('release', None)
        description = data.get('description', None)
        image_link = data.get('image_link', None)

        # validate parameters, description and image_link are optional
        if not title:
            abort(422, {'message': 'Error: Missing title.'})
        if not release:
            abort(422, {'message': 'Error: Missing release.'})

        movie = Movie(
            title=title,
            release=release,
            description=description,
            image_link=image_link)
        movie.create()

        return jsonify({
            'success': True,
            'created': movie.id
        }), 201

    # PATCH movie
    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        data = request.get_json()
        selected_movie_id = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        # validate
        if not movie_id:
            abort(404, {'message': 'No movie_id provided.'})
        if not data:
            abort(400, {'message': 'Invalid JSON data.'})
        if not selected_movie_id:
            abort(
                404, {
                    'message': 'Movie with that id'
                    ' was not found'.format(movie_id)})

        # get updated variables from data
        title = data.get('title', selected_movie_id.title)
        release = data.get('release', selected_movie_id.release)
        description = data.get('description', selected_movie_id.description)
        image_link = data.get('image_link', selected_movie_id.image_link)

        # assign the variable to the selected movie
        selected_movie_id.title = title
        selected_movie_id.release = release
        selected_movie_id.description = description
        selected_movie_id.image_link = image_link

        # UPDATE DATBASE
        selected_movie_id.update()

        # RETURN RESULTS
        return jsonify({
            'success': True,
            'updated': selected_movie_id.id,
            'movie': [selected_movie_id.format()]
        }), 200

    # DELETE movie
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie_id:
            abort(400, {'message': 'No movie_id provided.'})

        if not movie:
            abort(404, {'message': 'Movie was not found.'})

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        }), 200

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocesable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080, debug=True)
