PYTHONPATH=. pytest tests
black
flake8
mypy com_gui money Purchase tests *.py
