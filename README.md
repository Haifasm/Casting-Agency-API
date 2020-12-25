# Casting Agency API

This is the last project of the [Full-Stack Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

It covers the following technical topics:
- Database modeling with PostgreSQL & SQLAlchemy.
- Perform CRUD(create, read, update and delete) operations on database with Flask.
- Automated testing using Unittest.
- Authorization and role based authentication.
- Deployment on Heroku.

The API is used for storing, updating, deleting and retrieving movies and actors in a PostgreSQL database.

There are 3 types of roles each of which having different permissions as specified below:
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
    
The API is deployed using Heroku in the following URL:
    https://haifa-casting-agency.herokuapp.com/

## Endpoints

### GET '/actors'

Returns a paginated list of actors of length 10 and the total number of actors.

<img width="1105" alt="Screen Shot 2020-12-25 at 6 50 19 PM" src="https://user-images.githubusercontent.com/51233872/103139310-cae20100-46eb-11eb-8baa-5d2ed951732e.png">

 ```
 curl -X GET https://haifa-casting-agency.herokuapp.com/actors\
 -H 'Authorization: Bearer <TOKEN>'
```

### GET '/movies'

Returns a paginated list of movies of length 10 and the total number of movies.

<img width="1105" alt="Screen Shot 2020-12-25 at 7 01 36 PM" src="https://user-images.githubusercontent.com/51233872/103139293-aab24200-46eb-11eb-9399-56858ed8bb1c.png">

 ```
 curl -X GET https://haifa-casting-agency.herokuapp.com/movies\
 -H 'Authorization: Bearer <TOKEN>'
```

### Get '/actors/<actor_id>'

Returns the actor with the given actor_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 8 31 55 PM" src="https://user-images.githubusercontent.com/51233872/103139750-7bea9a80-46f0-11eb-9b3a-c8bc228a8a10.png">

```
curl -X GET https://haifa-casting-agency.herokuapp.com/actors/3\
 -H 'Authorization: Bearer <TOKEN>'
```

### Get '/movies/<movie_id>'

Returns the movie with the given movie_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 8 33 12 PM" src="https://user-images.githubusercontent.com/51233872/103139754-80af4e80-46f0-11eb-9521-7793004f32cc.png">

```
curl -X GET https://haifa-casting-agency.herokuapp.com/movies/2\
 -H 'Authorization: Bearer <TOKEN>'
```

### Post '/actors'

Add actor to the database.

Attributes:
- name
- age
- gender
- description
- image_link

description and image_link are optional.

<img width="944" alt="Screen Shot 2020-12-25 at 6 49 29 PM" src="https://user-images.githubusercontent.com/51233872/103139298-bb62b800-46eb-11eb-966f-fa8290773ca6.png">

```
  curl -X POST https://haifa-casting-agency.herokuapp.com/actors \
   -H 'Authorization: Bearer <TOKEN>'\
  -H 'Content-Type: application/json' \
  -d '{"name": "Leonardo DiCaprio",
    "age": "46",
    "gender": "Male",
    "description": "American actor, film producer and environmentalist. He has often played unconventional roles, particularly in biopics and period films. As of 2019, his films have grossed US$7.2 billion worldwide, and he has placed eight times in annual rankings of the highest-paid actors in the world.",
    "image_link": "https://www.gstatic.com/tv/thumb/persons/435/435_v9_bc.jpg"}'
```
### Post '/movies'

Add movie to the database.

Attributes:
- title
- release
- description
- image_link

description and image_link are optional.

<img width="944" alt="Screen Shot 2020-12-25 at 6 47 24 PM" src="https://user-images.githubusercontent.com/51233872/103139245-514a1300-46eb-11eb-89d6-f56664cf29c4.png">

```
  curl -X POST https://haifa-casting-agency.herokuapp.com/movies \
   -H 'Authorization: Bearer <TOKEN>'\
  -H 'Content-Type: application/json' \
  -d '{"title": "The Imitation Game", "release": "2014-12-12", "description": "Alan Turing, a British mathematician, joins the cryptography team to decipher the German enigma code.", "image_link":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQ5vi9xgRkP0nk5aRn8tcGEGRnOQyM-aAS1ldqfQSi_69V1yfU"}'
```

### Patch '/actors/<actor_id>'

Update attributes of the actor with the given actor_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 6 54 11 PM" src="https://user-images.githubusercontent.com/51233872/103139284-9b32f900-46eb-11eb-99bf-4e4f0c12265e.png">

 ```
  curl -X PATCH https://haifa-casting-agency.herokuapp.com/actors/3 \
   -H 'Authorization: Bearer <TOKEN>' \
   -H 'Content-Type: application/json' \
   -d '{"description": "English actor. A graduate of the Victoria University of Manchester, he continued his training at the London Academy of Music and Dramatic Art, obtaining a Master of Arts in Classical Acting."}'
```

### Patch '/movies/<movie_id>'

Update attributes of the movie with the given movie_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 7 04 13 PM" src="https://user-images.githubusercontent.com/51233872/103139374-8dca3e80-46ec-11eb-8d49-e31fef8320d7.png">

 ```
  curl -X PATCH https://haifa-casting-agency.herokuapp.com/movies/3 \
   -H 'Authorization: Bearer <TOKEN>'\
   -H 'Content-Type: application/json' \
   -d '{"image_link":"https://iamyourtargetdemographic.files.wordpress.com/2013/12/wolf-of-wall-street.jpg"}'
```
### Delete '/actors/<actor_id>'

Delete the actor with the given actor_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 6 57 05 PM" src="https://user-images.githubusercontent.com/51233872/103139364-82771300-46ec-11eb-91af-1a06cd6d0c5a.png">

 ```
  curl -X DELETE https://haifa-casting-agency.herokuapp.com/actors/5 \
   -H 'Authorization: Bearer <TOKEN>'
```
### Delete '/movies/<movie_id>'

Delete the movie with the given movie_id.

<img width="1105" alt="Screen Shot 2020-12-25 at 7 05 52 PM" src="https://user-images.githubusercontent.com/51233872/103139377-94f14c80-46ec-11eb-8705-e1888bf801cd.png">

 ```
  curl -X DELETE https://haifa-casting-agency.herokuapp.com/movies/4 \
   -H 'Authorization: Bearer <TOKEN>'
```

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
    2. Create user in Auth0 and assign role.
    3. Use Auth0 URI in Step 1 and login withe the user created in previous step
    4. The token will be appended in the URL after login is completed.

### setup.sh

Replace the values of this file to reflect your setup.
Make sure to have no spaces before and after =.

```bash
export AUTH0_DOMAIN=
export API_AUDIENCE=
export AUTH0_APP_CLIENT_ID=

#databases
export HEROKU_DATABASE=
export LOCAL_DATABASE=
export TEST_DATABASE=

#tokens
export CASTING_ASSISTANT=
export EXECUTIVE_PRODUCER=
export CASTING_DIRECTOR=
```

To export the credentials as environment variable, after activating your environment run

```bash
source setup.sh
```

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

## Authors

- Haifa Almansour, Udacity Full Stack Web Developer Nanodegree Student.
- Udacity Team.
