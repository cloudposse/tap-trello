export DOCKER_IMAGE ?= cloudposse/$(APP)
export DOCKER_TAG ?= dev
export DOCKER_IMAGE_NAME ?= $(DOCKER_IMAGE):$(DOCKER_TAG)
export DOCKER_BUILD_FLAGS =

include $(shell curl --silent -O "https://raw.githubusercontent.com/cloudposse/build-harness/master/templates/Makefile.build-harness"; echo Makefile.build-harness)

run:
	docker run --name $(APP) --rm -it $(DOCKER_IMAGE_NAME)

shell:
	docker run --name $(APP) --rm -it $(DOCKER_IMAGE_NAME) bash

requirements.txt: tap_trello.py
	pip3 freeze > $@


fmt:
	yapf -i tap_trello.py
