# mentors-backend

Backend server code for Baot mentorship application.

## Deploy a Local Setup

### Local Database

1. Install [Docker](https://docs.docker.com/install/) and verify installation.
2. Install [pgAdmin](https://www.pgadmin.org/download/)
   (or your favorite PostgreSQL GUI client).
3. In the command line, tun `docker run -p 5432:5432 --name baot-mentors -e POSTGRES_PASSWORD=somePassword -d postgres`.
   _baot-mentors_ is the docker container's name and can be changed freely.
4. Connect to this DB using your PostgresSQL client with the following details:
   - host: localhost
   - port: 5432
   - username: postgres
   - password: somePassword

### Local Server

1. Clone this repository and install all dependencies using `pip install -r requirements.txt`.
   Consider using Python's virtual environment (_venv_) to prevent
   versioning conflicts.

   > :mega: If you're experiencing installation problems with _psycopg2_,
   > try installing it separately using the command `pip install psycopg2-binary`. (in such case don't forget to comment it on the requirements.txt file and re-run `pip install -r requirements.txt`)

2. Set the following environment variables (you can do so in PyCharm's run configurations):
   - `DATABASE_URL=postgresql://postgres:somePassword@localhost/postgres`
   - `SECRET_KEY=someSecretStringUsedByFlask`
   - `APP_SETTINGS=config.DevelopmentConfig`
   - `GOOGLE_APPLICATION_CREDENTIALS=secretKey` - for prod use FIREBASE_CONFIG instead
3. Run `python reset_db.py` to initialize the DB tables.
4. Run `python main_app.py` and verify (using the console output) that the server is running.

**NOTE:** you can skip clause 2-4 and just run `start_env.sh` script which executes them for you

5. Browse to `http://localhost:5000` in your browser and verify you get a _Hello World_ page.

## Project Structure

- _main_app.py_: This file runs the application instance. Heroku knows to run this
  file as it is pointed to by _Procfile_ (using _gunicorn_).
- _app.py_ - defines the application, its configuration and the DB.
- _config.py_: declares different configuration schemes for the application. The configuration
  is set to an environment variable `APP_SETTINGS`.
- _models.py_: defines the DB model. Each class is a DB table.
  Refer to [Peewee](http://docs.peewee-orm.com/en/latest/) ORM for
  more details and documentation.
- _views.py_: This file contains all application routing. Namely, it is
  responsible for all exposed APIs.

### Heroku Files

- _Procfile_ tells Heroku which process to run on initialization.
- _runtime.txt_ tells Heroku which Python version it should use.

## DB Migrations

To perform changes on the DB, follow these guidelines:

1. Backup the database's current state (you can do this
   [manually](https://data.heroku.com/datastores/35002e65-a561-4a72-a47c-c81b3cec2aa3#durability)
   from the database's resource page on Heroku).
2. Edit _migrate.py_ to perform the desired operations on the DB.
   Use [Peewee's Schema Migrations](http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#migrate)
   documentation and examples.
3. Make sure you edit _models.py_ to reflect your new schema.
4. Once the script is final (and tested locally! :wink:), push it to the remote
   repository.
5. Run it on the staging app with `heroku run python migrate.py --app baot-mentors-stage` (you'll need
   [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)).
6. Do the same with production: `heroku run python migrate.py --app baot-mentors-prod`

To apply migrations to the local DB (and if you don't mind losing all local data) -
simply run _reset_db.py_ which will re-create the DB according to the schema in _models.py_.

## Tips & Tricks :smile:

- `heroku logs --app <app_name>` to show recent logs (use after crash...).
- Both staging and production applications deploy automatically from `master`.

## Project Architecture

![Project Architecture](/resources/arch.png)
