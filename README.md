# Casting Agency
This is a simple application API for managing movie and actor records in a PostgreSQL database.
The API is deployed using Heroku in the following URL:
https://haifa-casting-agency.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup
Run the following command:
```bash
createdb agency
```

### Auth0 Setup
1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
    - in applications settings:
        - Add "http://127.0.0.1:5000/" to Allowed Callback URLs 
4. Create a new API
    - in API settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actor`
    - `get:movie`
    - `post:actor`
    - `post:movie`
    - `patch:actor`
    - `patch:movie`
    - `delete:actor`
    - `delete:movie`
6. Create new roles and add the required permissions according to the table below:
    
    | Permission/Role  | Casting Assistant | Casting Director | Executive Producer |
    | ------------- | ------------- | ------------- | ------------- |
    | get:actor | ✔️ | ✔️ | ✔️ |
    | get:movie | ✔️ | ✔️ | ✔️ |
    | post:actor | | ✔️ | ✔️ |
    | post:movie | | | ✔️ |
    | patch:actor | | ✔️ | ✔️ |
    | patch:movie | | ✔️ | ✔️ |
    | delete:actor | | ✔️ | ✔️ |
    | delete:movie | | | ✔️ |

7. Get JWT tokens: 
    1. Enter the correct AUTH0 URI as follows:
    ```
     https://{YOUR_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={AUTHO_CLIENT_ID}&redirect_uri={CALLBACK_URL}
    ```
        In my case I will replace the following according to my setup as follows:
        - {YOUR_DOMAIN} = haifa-coffeeshop.us.auth0.com/
        - {API_AUDIENCE} = agency
        - {AUTHO_CLIENT_ID} = LaOEzzJTZtOfhsUt6JI2EZ7wWE8wv7bY
        - {CALLBACK_URL} = http://127.0.0.1:5000/

        Which will generate the following URL:
        ```
        https://haifa-coffeeshop.us.auth0.com/authorize?audience=agency&response_type=token&client_id=LaOEzzJTZtOfhsUt6JI2EZ7wWE8wv7bY&redirect_uri=http://127.0.0.1:5000/
        
        ```
    2. Create user in Auth0 and assign role
    3. Use Auth0 URI in Step 1 and login withe the user created in previous step
    4. The token will be appended in the URL after login is completed.


## Running the server

Ensure all environment variables are seet in .env file.
cd to the directory and ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Running tests
It is reccomended to have a seperate database for testing.
```bash
createdb agency_test
```
To run the tests execute 
```bash
python3 test_app.py
```

## Endpoints

### GET '/actors'

Returns a list of all actors.
 ```
 curl -X GET https://aw-casting-agency-api.herokuapp.com/all_actors \
 -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

### Get '/actors/<actor_id>'

Returns the actor with the given actor_id.
 ```
l
```
### Post '/actors'

Add actor to the database.
 ```
  curl -X POST https://aw-casting-agency-api.herokuapp.com/actor \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
   -d '{"id" : 1,
    "name" : 'Leonardo DiCaprio',
    "Age": 45,
    "gender" : 'Male',
    "movie_id": 1,
    "image_link": "https://d17zbv0kd7tyek.cloudfront.net/wp-content/uploads/2015/06/leonardo-dicaprio-fb.jpg"
    }'
```
### Patch '/actors/<actor_id>'

Update actor.
 ```
  curl -X PATCH https://aw-casting-agency-api.herokuapp.com/actor/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
   -H 'Content-Type: application/json' \
```
### Delete '/actors/<actor_id>'

Delete actor.
 ```
  curl -X DELETE https://aw-casting-agency-api.herokuapp.com/actor/<int:id> \
   -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```
;;;;;;;;

## Authors
- Haifa Almansour, Udacity Full Stack Web Developer Nanodegree Student.
- Udacity Team.