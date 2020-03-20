prod:
	yum update -y
	yum install -y python3 python36-devel.x86_64 python3-pip postgresql-server postgresql-contrib sudo nginx gcc

	pip3 install pip --upgrade
	pip3 install pipenv uwsgi

	db_name="hasker"
	db_user="hasker_user"
	
	sudo -u postgres /usr/bin/initdb /var/lib/pgsql/data/
	sudo -u postgres /usr/bin/pg_ctl -D /var/lib/pgsql/data/ start
	sudo -u postgres createdb $db_name
	sudo -u postgres createuser $db_user
	db_pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32})
	sudo -u postgres psql -c "alter user hasker_user with encrypted password '$db_pass';"
	sudo -u postgres psql -c "grant all privileges on database hasker to hasker_user;"

	echo "SECRET_KEY = '$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-50 })'" > config/settings/secret.py
	echo "DB_NAME = '$db_name'" >> config/settings/secret.py
	echo "DB_USER = '$db_user'" >> config/settings/secret.py
	echo "DB_PASSWORD = '$db_pass'" >> config/settings/secret.py
	echo "EMAIL_HOST_PASSWORD = ''" >> config/settings/secret.py
	echo "EMAIL_HOST_USER = ''" >> config/settings/secret.py
	echo "EMAIL_FROM = 'ilya.zvezdin@gmail.com'" >> config/settings/secret.py

	pipenv install --deploy
	python3 -m manage.py collectstatic