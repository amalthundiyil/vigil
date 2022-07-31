#
#  Installation
#

.PHONY: install install-dev
.PHONY: clean rebuild chmod pip-compile docker-clean
install:
	@ ./scripts/install/install.sh prod

install-dev:
	@
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
	@ pip-compile -v requirements-dev.in
	@ pip-compile -v requirements.in

docker-clean:
	@docker rm -v $(sudo docker ps -a -q -f status=exited)
	@docker rmi -f  $(sudo docker images -f "dangling=true" -q)
	@docker volume ls -qf dangling=true | xargs -r docker volume rm

#
#  Development
#
.PHONY: dev-start dev-stop dev monitor-frontend monitor-backend monitor frontend-start backend-stop backend-start backend-restart backend clean rebuild test

backend-start:
	@ scripts/control/start_backend.sh

frontend-start:
	@ scripts/control/start_frontend.sh

dev-start:
	@ scripts/control/start_backend.sh

dev-stop:
	@ sauron backend stop
	@ scripts/control/kill_frontend.sh

dev: dev-stop dev-start

db:
	@sudo sysctl -w vm.max_map_count=262144
	@docker-compose up

test:
	@ python -m pytest
