#
#  Installation
#

.PHONY: install install-dev
.PHONY: clean rebuild chmod pip-compile
install:
	@ ./scripts/install/install.sh prod

install-dev:
	@ ./scripts/install/install.sh dev

clean:
	@ scripts/control/clean.sh

rebuild:
	@ scripts/control/rebuild.sh prod

rebuild-dev:
	@ scripts/control/rebuild.sh dev

chmod:
	@ chmod +x scripts/*/*

pip-compile:
	pip-compile requirements-dev.in
	pip-compile requirements.in

#
#  Development
#
.PHONY: dev-start dev-stop dev monitor-frontend monitor-backend monitor frontend backend-stop backend-start backend-restart backend clean rebuild

dev-start:
	@ scripts/control/start_backend.sh

frontend-start:
	@ scripts/control/start_frontend.sh

dev-stop:
	@ sauron backend stop
	@ scripts/control/kill_frontend.sh

dev: dev-stop dev-start

db:
	@ - docker stop sauron_database
	@ - docker rm sauron_database
	@ docker run -p 5434:5432 --name sauron_database sauronlabs/sauron:database
