PORT ?= 8000
WEB_CONCURRENCY ?= 4

dev:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

start:
	poetry run gunicorn -w $(WEB_CONCURRENCY) -b 0.0.0.0:$(PORT) task_manager.wsgi:application

lint:
	poetry run flake8 task_manager

build:
	./build.sh

compile:
	cd task_manager && poetry run django-admin makemessages -l ru && poetry run django-admin compilemessages --ignore=venv

tests:
	poetry run python3 manage.py test task_manager.tests

coverage:
	poetry run coverage run --source='.' manage.py test task_manager.tests

report:
	poetry run coverage xml