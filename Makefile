.PHONY: venv run_agent

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run_agent:
	PYTHONPATH=.:backend python scripts/chat_with_agent.py

setup_db:
	PYTHONPATH=.:backend python scripts/setup_database.py
