restart: down up

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	docker-compose run backend python manage.py migrate

makemigrations:
	docker-compose run backend ./manage.py makemigrations

user:
	docker-compose run backend python manage.py createsuperuser

tests:
	docker-compose run backend ./manage.py test main.tests
