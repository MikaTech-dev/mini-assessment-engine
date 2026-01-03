# mini-assessment-engine
ACAD AI Assesment

Clone repository

    git clone https://github.com/MikaTech-dev/mini-assessment-engine.git
Cd into repository

    cd ./mini-assessment-engine

Initialize virtual environment with

    python -m venv .venv

Get CMD prompt to use virtual environment

    .venv\Scripts\activate
    ./.venv/Scripts/activate

Install Django

    pip install django

Start the project

    python -m django startproject assessment-engine

Run server

    python manage.py runserver

Migrate database models

    python manage.py makemigrations

Run pylint, load the django plugin, point to your django settings and specify what directory to lint
    pylint --load-plugins pylint_django --django-settings-module=assessment_engine.settings ./api/