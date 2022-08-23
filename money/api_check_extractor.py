import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

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
    description: str = ""


def get_check(token: str, input_qr_code_file_name: Path, output_json_file_name: Path) -> CheckResponce:
    response = requests.post(
        "https://proverkacheka.com/api/v1/check/get",
        data={
            "token": token,
        },
        files={
            "qrfile": open(input_qr_code_file_name, "rb"),
        },
    )

    if response.status_code == 200:
        json_data = json.loads(response.text)
        status = Status(json_data["code"])
        if status == Status.Success:
            with open(output_json_file_name, "w") as json_file:
                json_data = json.dumps(json_data["data"]["json"], indent=4, ensure_ascii=False)
                json_file.write(json_data)
            return CheckResponce(Status.Success, response.text, response.status_code)
        else:
            status2description = {
                Status.NotCorrect: "Чек некорректен",
                Status.NoData: "Данные чека пока не получены",
                Status.RequestsExceeded: "Превышено кол-во запросов",
                Status.WaitingBeforeRetrying: "Ожидание перед повторным запросом",
                Status.Other: "Прочее (данные не получены)",
            }
            return CheckResponce(status, response.text, response.status_code, status2description[status])
    else:
        return CheckResponce(Status.Error, response.text, response.status_code)
