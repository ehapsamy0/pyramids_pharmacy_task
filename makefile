env= local


upbuild: build up

up:
	docker-compose -f docker-compose.${env}.yml up

upd:
	docker-compose -f docker-compose.${env}.yml up -d

build:
	docker-compose -f docker-compose.${env}.yml build

run:
	docker-compose -f docker-compose.${env}.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f docker-compose.${env}.yml restart $(filter-out $@,$(MAKECMDGOALS))

shell:
	docker-compose -f docker-compose.${env}.yml exec django /entrypoint python manage.py shell_plus

bash:
	docker-compose -f docker-compose.${env}.yml exec django /entrypoint bash

makemigrations:
	docker-compose -f docker-compose.${env}.yml run --rm django python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f docker-compose.${env}.yml run --rm django python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

makemessages:
	docker-compose -f docker-compose.${env}.yml run --rm django python manage.py makemessages --no-location -l ar

compilemessages:
	docker-compose -f docker-compose.${env}.yml run --rm django python manage.py compilemessages

superuser:
	docker-compose -f docker-compose.${env}.yml run --rm django python manage.py createsuperuser

urls:
	docker-compose -f docker-compose.${env}.yml run django python manage.py show_urls

logs:
	docker-compose -f docker-compose.${env}.yml logs -f $(filter-out $@,$(MAKECMDGOALS))

test:
	docker-compose -f docker-compose.${env}.yml run --service-ports --rm -e DEBUGGER=True -e DJANGO_SETTINGS_MODULE=config.settings.test django python manage.py test $(filter-out $@,$(MAKECMDGOALS))

test_local:
	docker-compose -f docker-compose.${env}.yml exec -e DJANGO_SETTINGS_MODULE=config.settings.test django /entrypoint python manage.py test $(filter-out $@,$(MAKECMDGOALS))

pytest:
	docker-compose -f docker-compose.${env}.yml run --rm django pytest $(filter-out $@,$(MAKECMDGOALS))

mypy:
	docker-compose -f docker-compose.${env}.yml run --rm django mypy $(filter-out $@,$(MAKECMDGOALS))

debug:
	docker-compose -f docker-compose.${env}.yml run --service-ports --rm $(filter-out $@,$(MAKECMDGOALS))

down:
	docker-compose -f docker-compose.${env}.yml down $(filter-out $@,$(MAKECMDGOALS))

destroy:
	docker-compose -f docker-compose.${env}.yml down -v


rm_pyc:
	find . -name '__pycache__' -name '*.pyc' | xargs rm -rf
