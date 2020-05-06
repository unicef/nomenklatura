DOCKER_PASS?=
DOCKER_USER?=
VERSION?=1.0
ORGANIZATION=unicef
IMAGE_NAME=nomenklatura
DOCKER_IMAGE_NAME?=${ORGANIZATION}/${IMAGE_NAME}
DOCKER_IMAGE?=${DOCKER_IMAGE_NAME}:${VERSION}


release:
	docker build -t ${DOCKER_IMAGE} .


info:
	@echo 'docker images'
	@docker images | grep nomenklatura
	@echo '------------------'
	@echo 'docker containers'
	@docker ps -a | grep nomenklatura


ssh-backend:
	@docker exec -it nomenklatura /bin/sh
