# Init sprint

## Environment
- CU_Project - directory for soft of CommU (Python, Django)
- Scrum - backlog of developing
- DJproject - Django project
  * CommU - application staff
  * DJproject - project settings 
  * file_store - File base
  * telegram - source for telegram bot

---

## Setup VScode project
- make virtual envirounment
> $ pipenv shell

- check or set variable in system PATH
> PATH = ....; PIPENV_VENV_IN_PROJECT=venv

- check interpreter is it choose right (CU_Project/.venv)
> $ type python

*ctrl + shift + p - to select python interpreter manually*

- lock used packets and its dependecies
> $ pipenv lock

*use < pipenv install > & < pipenv uninstall > to refrash pipfiles automatically*

- restart terminal and better VScode

---

## Setup Django

- install Django packet in virtual envirounment
  > $ pipenv install django

- check Django packet exists (or install it)
> $ django-admin --version 

- make Django project directory
> $ django-admin startproject DJproject

- in Django directory check up success
> $ python manage.py runserver

- make application space
> $ python manage.py startapp WebCommU

- setup & make first migration
> $ python manage.py makemigrations
> $ python manage.py migrate

- check up all is OK
> $ python manage.py check

- add source to project directory
  - DJproject/uproject - CommU base packet


## Setup CommU application

- in DJproject
  - make key.py - for save Django SECRET_KEY
  - add key.* to .gitignore file

- in settings.py:
  -  edit SECRET part:
    > from .key import DJANGO_KEY
    > SECRET_KEY = DJANGO_KEY
  
  - in INSTALLED_APPS = [ ... ]
    add CommU application
    > ...
    > 'django.contrib.staticfiles',
    > 'WebCommU',
    > ]
  
  - in TEMPLATES = [ ... ]
    add html-temlates directory
    > ...
    > 'DIRS': [BASE_DIR/'WebCommU'/'templates', ],
    >
  
  - add path to static files:
    > STATICFILES_DIRS = [ 
    >   BASE_DIR/'WebCommU'/'static'
    > ]

  - add redirect constants:
  > ...
  > ## URL redirect
  > LOGIN_REDIRECT_URL = '/' # Redirect to homepage after successful login
  > LOGOUT_REDIRECT_URL = '/' # Redirect to homepage after successful logout
  > LOGIN_URL = '/login/' # Where to redirect users if they try to access a login-required page


- to root project's urls add:
  > urlpatterns = [
  > ... 
  >  ## added paths
  >  path('accounts/', include('django.contrib.auth.urls')),
  >  path('', include('WebCommU.urls')),
  > ...
