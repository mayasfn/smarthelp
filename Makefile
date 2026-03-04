.PHONY: venv run_agent setup_db app

venv:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

test_agent:
	PYTHONPATH=.:backend python3 scripts/chat_with_agent.py

setup_db:
	PYTHONPATH=.:backend python3 scripts/setup_database.py

app:
	streamlit run frontend/app.py
