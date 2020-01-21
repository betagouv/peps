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
PEPS_MJ_APIKEY_PUBLIC=xxxxxxxx
PEPS_MJ_APIKEY_PRIVATE=xxxxxxxx
PEPS_ASANA_PERSONAL_TOKEN=xxxxxxxx
PEPS_ASANA_PROJECT=xxxxxxxx
PEPS_STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
PEPS_DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
PEPS_CELLAR_HOST=''
PEPS_CELLAR_KEY=''
PEPS_CELLAR_SECRET=''
PEPS_CELLAR_BUCKET_NAME=''
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

### Updating test mock data

API tests rely on mock data available under ```api/tests/testdata```. To update these files with the latest Airtable data, you can run the following command:

```
python manage.py generatetestdata
```

## Web applications and frontend

There are two different client-side code locations in this repository:

### 1- ```/web```

These are templates and client-side elements that adhere to Django's standard way of doing things. These are currently used for utility views - such as the one showing the weight of the practices in real time.

The views here are not meant to be shown to the final user.

### 2- ```/frontend```

Under frontend we have a VueJS single page application meant to be the main client side web app.

#### Developing for ```/frontend```

In order to develop and debug this web app we need to launch two development servers: Django's and Vue's.

To launch Django's server:
```
python manage.py runserver
```

To launch Vue's server:
```
cd frontend
npm run serve
```

This will allow you to have instant reload on both the backend and the frontend.
