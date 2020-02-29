# mentors-backend
Backend server code for Baot mentorship application.

## Deploy a Local Database

1. Install Docker.
2. Install pgAdmin (or your favorite PostgreSQL GUI client)
3. Run `docker run -p 5432:5432 --name baot-mentors -e 
POSTGRES_PASSWORD=somePassword -d postgres`
4. Connect to this DB with the following details:
   `host=localhost`, `port=5432`, `username=postgres`, 
   `password=somePassword`.
5. Set the following environment variables:
 `DATABASE_URL=postgresql://postgres@somePassword@localhost/postgres` 
 `SECRET_KEY=someSecretStringUsedByFlask`
 `APP_SETTINGS=config.DevelopemtnConfig`
6. Run `reset_db.py` to initialize the DB tables.
   