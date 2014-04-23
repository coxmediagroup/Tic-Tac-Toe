
.PHONY: default

default:
	. env.sh
	. var/bin/activate && ttt/manage.py collectstatic --noinput
	. var/bin/activate && ttt/manage.py syncdb
	. var/bin/activate && ttt/manage.py migrate

.PHONY: test
test:
	. var/bin/activate && ttt/manage.py test tictac

.PHONY: shell
shell:
	. var/bin/activate && ttt/manage.py shell_plus

.PHONY: server
server:
	. var/bin/activate && ttt/manage.py runserver 127.0.0.1:9999

.PHONY: clean
clean:
	rm -Rf var
	rm ttt/db.sqlite3
	
