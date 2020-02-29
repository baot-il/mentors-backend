# mentors-backend
Backend server code for Baot mentorship application.

## Deploy a Local Database

1. Install [Docker](https://docs.docker.com/install/) and verify installation.
2. Install [pgAdmin](https://www.pgadmin.org/download/) 
(or your favorite PostgreSQL GUI client)
3. In the command line, tun `docker run -p 5432:5432 --name baot-mentors -e 
POSTGRES_PASSWORD=somePassword -d postgres`.
_baot-mentors_ is the docker container's name and can be changed freely.
4. Connect to this DB using your PostgresSQL client with the following details:
* host: localhost
* port: 5432
* username: postgres
* password: somePassword
5. Clone this repository and install all dependencies using `pip install -r requirements.txt`.
6. Set the following environment variables (you can do so for your virtual
   environment):
    * `DATABASE_URL=postgresql://postgres:somePassword@localhost/postgres`
    * `SECRET_KEY=someSecretStringUsedByFlask`
    * `APP_SETTINGS=config.DevelopemtnConfig`
6. Run `reset_db.py` to initialize the DB tables.
   