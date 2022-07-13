# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass

from PySide6.QtCore import QByteArray


def from_bytearray(ba: QByteArray) -> str:
    return bytes(ba.toHex()).decode("ascii")  # type: ignore


def to_bytearray(data: str) -> QByteArray:
    return QByteArray.fromHex(bytes(data, "ascii"))


@dataclass()
class ByteArraySetting:
    data: str = ""

    def save(self, geometry: QByteArray):
        self.data = from_bytearray(geometry)

    def restore(self) -> QByteArray:
        return to_bytearray(self.data)

    def is_valid(self):
        return self.data != ""
