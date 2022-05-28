restart: down up

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	docker-compose run web python manage.py migrate

user:
	docker-compose run web python manage.py createsuperuser

tests:
	docker-compose run web ./manage.py test main.tests
