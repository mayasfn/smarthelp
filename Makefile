.PHONY: venv run_agent

venv:
	python3.11 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run_agent:
	PYTHONPATH=.:backend python3 scripts/chat_with_agent.py

setup_db:
	PYTHONPATH=.:backend python3 scripts/setup_database.py
