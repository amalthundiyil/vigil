#
#  Installation
#
.PHONY: install install-dev
.PHONY: clean rebuild
install:
	@ ./scripts/install/install.sh prod

install-dev:
	@ ./scripts/install/install.sh dev

clean:
	@ scripts/control/clean.sh

rebuild:
	@ scripts/control/rebuild.sh prod

rebuild-dev:
	@ scripts/control/rebuild-backend.sh dev

#
#  Development
#
.PHONY: dev-start dev-stop dev monitor-frontend monitor-backend monitor frontend backend-stop backend-start backend-restart backend clean rebuild

dev-start:
	@ scripts/control/start_sauron.sh
	@ scripts/control/start_frontend.sh

dev-stop:
	@ sauron backend stop
	@ scripts/control/kill_frontend.sh

dev: dev-stop dev-start

db:
	@ - docker stop sauron_database
	@ - docker rm sauron_database
	@ docker run -p 5434:5432 --name sauron_database sauronlabs/sauron:database
