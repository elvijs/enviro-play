REQUIREMENTS="requirements.txt"
SOURCE_DIR="src"
TESTS_DIR="tests"


format: black isort

black:
	black $(SOURCE_DIR) $(TESTS_DIR)

isort:
	isort $(SOURCE_DIR) $(TESTS_DIR)


check_format: check_black check_isort

check_black:
	black --check $(SOURCE_DIR) $(TESTS_DIR)

check_isort:
	isort --diff $(SOURCE_DIR) $(TESTS_DIR)


static_checks: mypy flake8


mypy:
	mypy --ignore-missing-imports $(SOURCE_DIR) $(TESTS_DIR)

flake8:
	flake8 $(SOURCE_DIR) $(TESTS_DIR)


test: test_code

test_code:
	pytest $(TESTS_DIR)


freeze_requirements:
	pip freeze | grep -v enviro-play | grep -v \!\! > $(REQUIREMENTS)


install_deps:
	pip install -r $(REQUIREMENTS)

install: install_deps
	pip install -e .
