allure:
	pytest -s ./tests --alluredir=allureress || true
	allure serve ./allureress

coverage:
	coverage erase
	coverage run --source=./openapi_parser -m pytest
	coverage html
