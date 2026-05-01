PYTHON=python3.11
BACKEND_DIR=backend
FRONTEND_DIR=frontend

.PHONY: backend-install frontend-install backend-run frontend-run

backend-install:
	cd $(BACKEND_DIR) && $(PYTHON) -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

frontend-install:
	cd $(FRONTEND_DIR) && npm install

backend-run:
	cd $(BACKEND_DIR) && . .venv/bin/activate && uvicorn app.main:app --reload

frontend-run:
	cd $(FRONTEND_DIR) && npm run dev
