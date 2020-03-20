prod:
	yum update -y
	yum install -y python3 python36-devel.x86_64 python3-pip postgresql-server postgresql-contrib sudo nginx gcc

	pip3 install pip --upgrade
	pip3 install pipenv uwsgi

	sudo -u postgres /usr/bin/initdb /var/lib/pgsql/data/
	sudo -u postgres /usr/bin/pg_ctl -D /var/lib/pgsql/data/ start
	sudo -u postgres createdb hasker
	sudo -u postgres createuser hasker_user
	psql_pass=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32})
	sudo -u postgres psql -c "alter user hasker_user with encrypted password '$psql_pass';"
	sudo -u postgres psql -c "grant all privileges on database hasker to hasker_user;"


	pipenv install --deploy --system