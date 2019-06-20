include $(shell curl --silent -O "https://raw.githubusercontent.com/cloudposse/build-harness/master/templates/Makefile.build-harness"; echo Makefile.build-harness)

run:
	./tap_trello.py

requirements.txt: tap_trello.py
	pip3 freeze > $@

fmt:
	yapf -i tap_trello.py
