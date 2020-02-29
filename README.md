# mentors-backend
Backend server code for Baot mentorship application.

## Deploy a Local Setup

### Local Database

1. Install [Docker](https://docs.docker.com/install/) and verify installation.
2. Install [pgAdmin](https://www.pgadmin.org/download/) 
(or your favorite PostgreSQL GUI client).
3. In the command line, tun `docker run -p 5432:5432 --name baot-mentors -e 
POSTGRES_PASSWORD=somePassword -d postgres`.
_baot-mentors_ is the docker container's name and can be changed freely.
4. Connect to this DB using your PostgresSQL client with the following details:
    * host: localhost
    * port: 5432
    * username: postgres
    * password: somePassword

### Local Server
1. Clone this repository and install all dependencies using `pip install -r requirements.txt`.
   Consider using Python's virtual environment (_venv_) to prevent 
   versions conflicts.
   
   > :mega: If you're experiencing installation problems with _psycopg2_, try installing it as a standalone
   using the command `pip install psycopg2-binary`

2. Set the following environment variables (you can set them in PyCharm's run configurations):
    * `DATABASE_URL=postgresql://postgres:somePassword@localhost/postgres`
    * `SECRET_KEY=someSecretStringUsedByFlask`
    * `APP_SETTINGS=config.DevelopementConfig`
3. Run `reset_db.py` to initialize the DB tables.
4. Run `python main_app.py` and verify (using the console output) that the server is running.
5. Browse to `http://localhost:5000` in your browser and verify you get a _Hello World_ page.


## Project Structure

* _main_app.py_: This file runs the application instance. Heroku knows to run this
file as it is pointed to by _Procfile_ (using _gunicorn_).
* _app.py_ - defines the application, its configuration and the DB.
* _config.py_: declares different configuration schemes for the application. The configuration
is set to an environment variable `APP_SETTINGS`.
* _models.py_: defines the DB model. Each class is a DB table. 
Refer to [Peewee](http://docs.peewee-orm.com/en/latest/) ORM for
more details and documentation.
* _views.py_: This file contains all application routing. Namely, it is
responsible for all exposed APIs.
### Heroku Files
* _Procfile_ tells Heroku which process to run on initialization.
* _runtime.txt_ tells Heroku which Python version it should use.


## DB Migrations
Use _migrate.py_ to perform migration operations on the DB. 
Once the script is final (and tested! :wink:), push it and run it remotely
with `heroku run python migrate.py` (this will only work if
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) is installed)
Make sure you edit _models.py_ according to your new schema.