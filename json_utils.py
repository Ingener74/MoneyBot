# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path


def reformat_json(input_file_name: Path, output_file_name: Path):
    json_data = json.load(open(input_file_name, "r", encoding="utf-8"))
    json.dump(
        json_data,
        open(output_file_name, "w+", encoding="utf-8"),
        indent=4,
        ensure_ascii=False,
    )
