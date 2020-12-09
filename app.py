import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import *

'''
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/
'''

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

    #API ENDPOINTS
    @app.route('/')
    def home():
        return jsonify({
            'welcome': 'Welcome '
        })
    
    # GET actors
    @app.route('/actors', methods=['GET'])
    #@requires_auth('get:actor')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = {actor.id: actor.name for actor in actors}

        if len(formatted_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': formatted_actors,
            'number_of_actors': len(Actor.query.all())
        })

    #GET specific actor
    @app.route('/actors/<actor_id>', methods=['GET'])
    #@requires_auth('get:actor')
    def get_actor(actor_id):

        if not actor_id:
            abort(400, {'message': 'No actor_id'})

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404, {'message': 'Actor was not found'.format(actor_id)})

        return jsonify({'success': True, 'actor': [actor.format()]})

    # POST actor
    @app.route('/actors', methods=['POST'])
    #@requires_auth('post:actors')
    def create_actor():
        data = request.get_json()

        if not data:
            abort(400, {'message': 'invalid JSON data.'})

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

        actor = Actor(name=name, age=age, gender=gender, description=description, image_link=image_link)
        actor.create()

        return jsonify({'success': True, 'created': actor.id})
    
    # PATCH actor
    # DELETE actor



    return app




APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)


