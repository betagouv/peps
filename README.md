# Peps

Peps helps find personalized agricultural practices to reduce pesticide use.

📱 The repository for Peps' mobile application [can be found here](https://github.com/betagouv/peps-app).

## Setup the development environment

### Python 3 virtualenv

Start a virtualenv with Python3:

```
virtualenv -p python3 venv
source ./venv/bin/activate
```

### Install requirements

The requirements are found in ```requirements.txt```. To install them:

```
pip install -r requirements.txt
```

### Postgresql database

You will need a Postgresql database to run the application. You can create one as follows:

```
psql
CREATE DATABASE peps;
```

### Environment variables

Create an ```.env``` file at the same level as the ```manage.py``` file. This file should have the following environment values:

```
PEPS_SECRET='some-secret-value'
PEPS_DEBUG='True'
PEPS_DB_USER='your-pgsql-user'
PEPS_DB_PASSWORD='your-pgsql-password'
PEPS_DB_HOST='127.0.0.1'
PEPS_DB_PORT='5432'
PEPS_DB_NAME='your-db-name'
PEPS_AIRTABLE_KEY='your-airtable-api-key'
PEPS_ALLOWED_HOSTS=127.0.0.1,0.0.0.0
```

### Make initial migration and create super user

Before you start, ensure the database is properly migrated:

```
python manage.py migrate
```

And create a super user:

```
python manage.py createsuperuser
```

## Test

You should be ready to go. Run the following command to ensure everything is OK:

```
python manage.py test
```
