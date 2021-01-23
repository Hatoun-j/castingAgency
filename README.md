# Casting Agncy

## Project Motivation 

Casting agncy final project for udacity aims to collect data of actors and movies and to de any modification on them. the project has three users: 1.Casting Assistant 2. Casting Director 3. Casting Director each of them has a specefic role and permissions. 

## Getting Started

### URLs
Locally: http://127.0.0.1:5000/
Heroku: https://casting-agency-reema-ah.herokuapp.com/

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment
Create Virtual Env by running:

```bash
virtualenv --python=python3.7 venv

```

#### PIP Dependencies

install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

#### Setup Authentication in Auth0: 

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
4. in API Settings:
    - Enable RBAC
    - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - get:actors
    - get:movies
    - delete:actors
    - delete:movies
    - post:actors
    - post:movies
    - patch:actors
    - patch:movies

6. Create new roles for:
    - Casting Assistant:
       Can view actors and movies
    - Casting Director:
      - All permissions a Casting Assistant has and…
      - Add or delete an actor
      - Modify actors or movies
    - Executive Producer:
       Can perform all actions



## Endpoints

### GET '/actors'
* Genreal
    * Fetches a dictionary of actors
    * Request Arguments: None
    * Returns: An object that contains actors array, and a success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors`

```
{
    "actors":[
        {"age":51,"gender":"Female","id":1,"name":"Jennifer aniston"},
        {"age":52,"gender":"Male","id":2,"name":"Will smith"},
        {"age":46,"gender":"Male","id":3,"name":"Leonardo dicaprio"},
        {"age":57,"gender":"Male","id":4,"name":"Brad pitt"},
        {"age":64,"gender":"Male","id":5,"name":"Tom hanks"}],
    "success":true
}
```

### GET '/movies'
* Genreal
    * Fetches a dictionary of movies
    * Request Arguments: None
    * Returns: movies array and success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies`

```
{
    "movies":[
        {"id":1,"release_date":"Wed, 01 Jan 2020 00:00:00 GMT","title":"Mulan"},
        {"id":2,"release_date":"Wed, 01 Jan 2020 00:00:00 GMT","title":"The Midnight Sky"},
        {"id":3,"release_date":"Fri, 01 Jan 2010 00:00:00 GMT","title":"Inception"},
        {"id":4,"release_date":"Wed, 01 Jan 2020 00:00:00 GMT","title":"Tenet"},
        {"id":5,"release_date":"Tue, 01 Jan 2019 00:00:00 GMT","title":"Joker"}],
    "success":true
}
```

### DELETE '/actors/1'
* Genreal
    * Removes the specified actor
    * Request Arguments: The actor's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted actor.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors/1`
```
{
  "deleted": 1,
  "success": true
}
```

### DELETE '/movies/1'
* Genreal
    * Removes the specified movie
    * Request Arguments: The movie's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted movie.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies/1`
```
{
  "deleted": 1,
  "success": true
}
```

### POST '/actors'
* General
    * Creates a new actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created actor.
* Sample: ` curl http://127.0.0.1:5000/actors -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Brad pitt\",\"age\":\"57\",\"gender\":\"Male\"}" `
```
{
    "created":4,
    "success":true
}
```

### POST '/movies'
* General
    * Creates a new movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created movie.
* Sample: ` curl http://127.0.0.1:5000/movies -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"Mulan\",\"release_date\":\"2020-01-01\"}" `

```
{ 
    "created":1,
    "success":true
}
```


### PATCH '/actors/1'
* General
    * Updates the specified actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated actor.
* Sample: ` curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Angelina jolie\"}" `
```
{
    "actor":{
        "age":45,
        "gender":
        "Female",
        "id":1,"
        name":"Angelina jolie"
    },
    "success":true}
```

### PATCH '/movies/1'
* General
    * Updates the specified movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated movie.
* Sample: ` curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"Home Alone\"}" `
```
{
    "movie":{
        "id":1,
        "release_date":"Thu, 01 Apr 1990 00:00:00 GMT",
        "title":"Home Alone"
    },
    "success":true
}
```
