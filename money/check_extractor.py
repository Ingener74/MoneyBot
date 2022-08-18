import json
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict

import requests


class Status(Enum):
    NotCorrect = 0
    Success = 1
    NoData = 2
    RequestsExceeded = 3
    WaitingBeforeRetrying = 4
    Other = 5
    Error = 6

@dataclass()
class CheckResponce:
    status: Status
    text: str
    status_code: int
    description: str = ''


def get_check(token: str, input_qr_code_file_name: Path, output_json_file_name: Path) -> CheckResponce:
    response = requests.post(
        'https://proverkacheka.com/api/v1/check/get',
        data={
            'token': token,
        },
        files={
            'qrfile': open(input_qr_code_file_name, 'rb'),
        }
    )

    if response.status_code == 200:
        json_data = json.loads(response.text)
        status = Status(json_data['code'])
        json.dump(json_data['data']["json"], open(output_json_file_name, 'w'), indent=4)
        if status == Status.Success:
            return CheckResponce(Status.Success, response.text, response.status_code)
        else:
            return CheckResponce(status, response.text, response.status_code,
                                 'Чек некорректен' if status == Status.NotCorrect else
                                 'Данные чека пока не получены' if status == Status.NoData else
                                 'Превышено кол-во запросов' if status == Status.RequestsExceeded else
                                 'Ожидание перед повторным запросом' if status == Status.WaitingBeforeRetrying else
                                 'Прочее (данные не получены)' if status == Status.Other else '')
    else:
        return CheckResponce(Status.Error, response.text, response.status_code)
