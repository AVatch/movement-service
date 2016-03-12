# Movement Service

### Overview
A Django backend service to support movement

### Requirements
Reference the ```requirements.txt``` file

### Configuration
#### 1 Install dependencies
Create a ```virtualenv``` and install the dependencies using ```pip```
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

#### 2 Setup [python-dotenv](https://github.com/theskumar/python-dotenv) to handle credentials.
1. Create a file called ```.env``` in ```movement/movement``` directory. It should be at the same level as ```settings.py```
2. In the .env file you need to supply a few credentials. ```SECRET_KEY``` and ```GEO_SERVICE_API_KEY``` (which for now is a Google API key that has google maps api enabled). You're file should look something like this

```
SECRET_KEY="SOME SUPER SECRET KEY HERE FOR DJANGO TO USE"
GEO_SERVICE_API_KEY="SOME COOL KEY FROM A PROVIDER"
```

#### 3 Perform initial migrations and create a superuser
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ <follow prompts>
```

### Running the server locally
Provided everything is installed and you are sourced into your ```virtualenv``` just run the normal Django command
```
$ python manage.py runserver <port number, default to 8000> 
```

### Availible Endpoints
##### Cohorts Module
```
GET  /api/v1/cohorts
POST /api/v1/cohorts
```
##### Locations Module
```
GET  /api/v1/locations
POST /api/v1/locations
PUT  /api/v1/locations
GET  /api/v1/locations/<pk>/reveal
POST /api/v1/locations/<pk>/reveal
```
