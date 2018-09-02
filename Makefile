LOG_LINES = 100
FG = FALSE

ifeq ($(FG), TRUE)
	DOCKER_UP += -d
endif

DOCKER_UP := docker-compose up
DOCKER_LOGS := docker-compose logs --tail=$(LOG_LINES)
DOCKER_START := docker-compose start
DOCKER_STOP := docker-compose stop

ifdef FOLLOW
	DOCKER_LOGS += -f
endif

ifdef SERVICES
	DOCKER_UP += $(SERVICES)
	DOCKER_LOGS += $(SERVICES)
	DOCKER_STOP += $(SERVICES)
	DOCKER_START += $(SERVICES)
	DOCKER_RECREATE := docker-compose rm -s $(SERVICES); docker-compose up -d $(SERVICES)
endif

.DEFAULT_GOAL : help

help:
	@echo "    help - Print this help message"
	@echo "    "
	@echo "    run [FG=FALSE] [SERVICES=ALL]"
	@echo "        Run the project in Background mode by default."
	@echo "        FG: Define as TRUE to run in foreground."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    logs [LOG_LINES=100] [SERVICES=ALL] [FOLLOW=TRUE]"
	@echo "        See services logs."
	@echo "        LOG_LINES: The number of log lines for each service"
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "        FOLLOW: keep tracking the logs. E.g.: FOLLOW=TRUE"
	@echo "    "
	@echo "    stop [SERVICES=ALL]"
	@echo "        Stop one or more services."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    start [SERVICES=ALL]"
	@echo "        Start one or more stopped services."
	@echo "        SERVICES: servies that will be affected by the command. E.g.: SERVICES='service_a_name service_b_name'"
	@echo "    "
	@echo "    recreate SERVICES='<service_a> <service_b> ...'"
	@echo "        Remove and recreate the given services/containers, but not their volumes."
	@echo "    "
	@echo "    clean"
	@echo "        stop and remove all service containers and images."
	@echo "    "
	@echo "    clean-containers"
	@echo "        remove all containers, keeping images and volumes"
	@echo "    "
	@echo "    clean-volumes"
	@echo "        remove all volumes. It also remove containers"
	@echo "    "
	@echo "    clean-repo"
	@echo "        Clean the current repo by undoing all uncommited changes and"
	@echo "        remove untracked git files"
.PHONY: help

run:
	@$(DOCKER_UP)
.PHONY: run

logs:
	$(DOCKER_LOGS)
.PHONY: logs

stop:
	@$(DOCKER_STOP)
.PHONY: stop

start:
	@$(DOCKER_START)
.PHONY: start

recreate:
ifndef DOCKER_RECREATE
	@echo "You need to pass the services you want to recreate with SERVICE='service_a_name service_b_name'"
	@exit 1
else
	@$(DOCKER_RECREATE)
endif
.PHONY: recreate

clean:
	docker-compose down --rmi all
.PHONY: clean

clean-containers:
	docker-compose down
.PHONY: clean-containers

clean-volumes:
	docker-compose down --rmi -v
.PHONY: clean-containers

clean-repo:
	git reset --hard HEAD
	git clean -di -e '.env'
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
.PHONY: clean-pyc
