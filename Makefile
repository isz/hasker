DB_HOST = localhost
DB_NAME = hasker
DB_USER = hasker_user
DB_PASS = $(shell < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c$${1:-32})
SECRET_KEY = $(shell < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c$${1:-50})


SOCK_DIR = /var/local/hasker
UWSGI_LOG_DIR = /var/log/uwsgi
MEDIA_ROOT = /var/local/hasker/media
STATIC_ROOT = /var/local/hasker/static

.PHONY: all prod ngnix postgres hasker uwsgi dependences test

all:

dependences:
	@echo "Install dependences"
	@yum update -y
	@yum install -y python3 python36-devel python3-pip postgresql-server postgresql-contrib sudo nginx gcc
	@pip3 install pip --upgrade
	@pip3 install uwsgi

	@pip3 install -r requirements.txt

postgres:
	@echo "Database configurating"
	@sudo -u postgres /usr/bin/initdb /var/lib/pgsql/data/
	@sudo -u postgres /usr/bin/pg_ctl -D /var/lib/pgsql/data/ start
	@sudo -u postgres createdb $(DB_NAME)
	@sudo -u postgres createuser $(DB_USER)
	@sudo -u postgres psql -c "alter user hasker_user with password '$(DB_PASS)';"
	@sudo -u postgres psql -c "grant all privileges on database hasker to hasker_user;"

hasker:
	@echo "Create secrets"
	@echo "SECRET_KEY = '$(SECRET_KEY)'" > config/settings/secret.py
	@echo "DB_NAME = '$(DB_NAME)'" >> config/settings/secret.py
	@echo "DB_USER = '$(DB_USER)'" >> config/settings/secret.py
	@echo "DB_PASSWORD = '$(DB_PASS)'" >> config/settings/secret.py
	@echo "DB_HOST = '$(DB_HOST)'" >> config/settings/secret.py

	@echo "E-mail notifications config"
	@read -p "Enter e-mail host: " EMAIL_HOST; \
	echo "EMAIL_HOST = '$$EMAIL_HOST'" >> config/settings/secret.py

	@read -p "Enter e-mail  user: " EMAIL_USER; \
	echo "EMAIL_HOST_USER = '$$EMAIL_USER'" >> config/settings/secret.py

	@read -p "Enter password: " EMAIL_PASSWORD; \
	echo "EMAIL_HOST_PASSWORD = '$$EMAIL_PASSWORD'" >> config/settings/secret.py

	@read -p "Enter e-mail from: " EMAIL_FROM; \
	echo "EMAIL_FROM = '$$EMAIL_FROM'" >> config/settings/secret.py

	@echo "Collect static and migrate"
	@export DJANGO_SETTINGS_MODULE="config.settings.production"; \
	export MEDIA_ROOT=$(MEDIA_ROOT); \
	export STATIC_ROOT=$(STATIC_ROOT); \
	python3 manage.py collectstatic; \
	python3 manage.py migrate

	mkdir -p $(MEDIA_ROOT)

uwsgi:
	@echo "UWSGI configurating"
	@mkdir -p $(SOCK_DIR)
	@mkdir -p $(UWSGI_LOG_DIR)

nginx:
	@echo "NGINX configurating"
	@cp deploy/nginx.conf /etc/nginx/conf.d/hasker.conf
	@echo "Start NGINX"
	@nginx

prod: dependences postgres hasker nginx uwsgi
	@echo "Start application"
	@export DJANGO_SETTINGS_MODULE="config.settings.production"; \
	export MEDIA_ROOT=$(MEDIA_ROOT); \
	uwsgi --ini deploy/uwsgi.ini
