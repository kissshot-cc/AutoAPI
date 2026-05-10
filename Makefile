.PHONY: install test test-smoke allure mock lint fmt clean

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest

test-smoke:
	pytest -m smoke

test-regression:
	pytest -m regression

allure:
	pytest --alluredir=report
	allure serve report

mock:
	python3 mock_server.py

lint:
	ruff check .
	black --check .

fmt:
	ruff check --fix .
	black .

clean:
	rm -rf report/ allure-report/ allure-results/
	rm -rf logs/
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -f .coverage coverage.xml
	rm -f test.db

docker-test:
	docker compose up --build api-test
