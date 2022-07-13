# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def reformat_json(input_file_name: str, output_file_name: str):
    json_data = json.load(open(input_file_name, "r", encoding="utf-8"))
    json.dump(
        json_data,
        open(output_file_name, "w+", encoding="utf-8"),
        indent=4,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    reformat_json(
        "C:\\prj\\vps\\photos\\file_302.jpg.json",
        "C:\\prj\\vps\\photos\\file_302.output.json",
    )
