# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from subprocess import run
from loguru import logger

if __name__ == '__main__':
    res_dir = Path(__file__).parent / "res"
    ui_file = res_dir / "main_window.ui"
    py_file = res_dir / "ui_main_window.py"
    run(f'pyside6-uic {ui_file} -o {py_file}', shell=True)
    logger.info('Done.')
