# Setup Django Rest API Application
# At first create virutal environment(env)
```
virtualenv env_name

and then 

cd env_name
```

### Install Requirements in the env

```
pip install -r requirements.txt
```

### Install Initial Migrations file creation

```
python manage.py makemigrations

```

### Migrate the Model Structure into the database table

```
python manage.py migrate

```

### To run Local Development Server

```
python manage.py runserver

```
