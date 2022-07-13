PYTHONPATH=. pytest tests
black com_gui money Purchase tests *.py --exclude com_gui/res --line-length 120
flake8
mypy com_gui money Purchase tests *.py
