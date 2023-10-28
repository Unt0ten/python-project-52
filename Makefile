PORT ?= 8000
WEB_CONCURRENCY ?= 4

dev:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py migrate

migrations:
	python manage.py makemigrations

start:
	poetry run gunicorn -w $(WEB_CONCURRENCY) -b $0.0.0.0:$(PORT) task_manager.wsgi:application

lint:
	poetry run flake8 task_manager

build:
	./build.sh
