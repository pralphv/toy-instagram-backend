# toy-instagram-backend
This repo is the backend of the project Toy-Instagram. The project is built using Flask and Postgresql and servers only as an API provider.

Frontend Repo: https://github.com/pralphv/toy-instagram-frondend

<a href="https://toy-instagram-frontend.herokuapp.com/">Live Demo</a>
## Getting Started
Install dependencies
```
pip install -r requirements.txt
```
Change the URL to your Postgresql connection in *config.py*. Feel free to change the salt and secret keys 
```
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # change
```
Create database in your Postgresql
```
(env)$ psql
# create database your_database_name
# create database your_database_name_test
```
Init, migrate and upgrade the database
```
(env)$ python manage.py db init
(env)$ python manage.py db migrate
(env)$ python manage.py db upgrade
```
Run the server
```
python run.py
```
You should see a link in the prompt. Copy it to your browser. If you see "Hello world", you are good to go.
## Api 
### api/igposts

GET response
```
{
    "status": str,
    "data": [
        {
            "id": int,
            "description": str,
            "img_path": str,
            "author": str,
            "update_date": str
        },
    ]
}
```
POST Request
```
{
    "body":{
        "description": str
        },
    "header": {
        "Authentication": "Bearer $(token)"
        },
}
```
### api/login
POST Request
```
{
    "username": str,
    "password": str
}
```
POST Response
```
{
  "status": str,
  "data": {
    "token": str
  }
}
```
### api/register
POST Request
```
{
    "username": str,
    "password": str,
    "retype_password": str
}
```
POST Response
```
{
    "status": str,
    "data": str
}
```

## Coverage
![alt text](https://github.com/pralphv/toy-instagram-backend/blob/master/coverage.jpg)
## What's left?
- More validations in the API
- Logging
- Compress images when uploaded
- Properly return errors
- Rate limiting

