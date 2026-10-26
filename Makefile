.PHONY: install run test lint dev-web
install:
	python -m pip install -r requirements-dev.txt
run:
	uvicorn app.main:app --reload
test:
	python -m pytest -q
lint:
	ruff check app tests
dev-web:
	cd web && npm run dev
