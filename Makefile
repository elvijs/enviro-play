REQUIREMENTS="requirements.txt"
SOURCE_DIR="src"
SCRIPTS_DIR="scripts"
TESTS_DIR="tests"
ALL_CODE_DIRS=$(SOURCE_DIR) $(SCRIPTS_DIR) $(TESTS_DIR)


format: black isort

black:
	black $(ALL_CODE_DIRS)

isort:
	isort $(ALL_CODE_DIRS)


check_format: check_black check_isort

check_black:
	black --check $(ALL_CODE_DIRS)

check_isort:
	isort --diff $(ALL_CODE_DIRS)


static_checks: mypy flake8


mypy:
	mypy --ignore-missing-imports $(ALL_CODE_DIRS)

flake8:
	flake8 $(ALL_CODE_DIRS)


test: test_code

test_code:
	pytest $(TESTS_DIR)


freeze_requirements:
	pip freeze | grep -v enviro-play | grep -v \!\! > $(REQUIREMENTS)


install_deps:
	pip install -r $(REQUIREMENTS)

install: install_deps
	pip install -e .


# RaspberryPi stuff

initial_raspi_setup:
	curl -sSL https://get.pimoroni.com/enviroplus | bash
