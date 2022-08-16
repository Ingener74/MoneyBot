from unittest.mock import MagicMock, call, ANY

import pytest

from Purchase.Purchase import Purchase
from Purchase.PurchaseConfig import PurchaseConfig


class TestPurchase:
    def test_save(self, mocker):
        fake_worksheet = MagicMock()
        fake_worksheet.col_values = MagicMock(return_value=["", "", "", "", "foo"])
        fake_worksheet.update = MagicMock()
        fake_worksheet.format = MagicMock()

        fake_spreadsheet = MagicMock()
        fake_spreadsheet.worksheet = MagicMock(return_value=fake_worksheet)

        fake_client = MagicMock()
        fake_client.open_by_key = MagicMock(return_value=fake_spreadsheet)
        gspread_service_account: MagicMock = mocker.patch("gspread.service_account", return_value=fake_client)

        manager = MagicMock()
        manager.client = fake_client
        manager.spreadsheet = fake_spreadsheet
        manager.worksheet = fake_worksheet

        purchases = [Purchase("Soap", "1,0", "1,0", "Seller", "01.01.2022")]
        Purchase.save(
            "01.2022",
            purchases,
            PurchaseConfig("A", "B", "C", "D", "E", "F", 0),
            "creds.json",
            "very-long-spreadsheet-id",
        )

        gspread_service_account.assert_has_calls([call(filename="creds.json")])
        assert manager.mock_calls == [
            call.client.open_by_key("very-long-spreadsheet-id"),
            call.spreadsheet.worksheet("01.2022"),
            call.worksheet.col_values(0),
            call.worksheet.update("A6:A7", [["Soap"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("A6:A6", ANY),
            call.worksheet.update("B6:B7", [["1,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("B6:B6", ANY),
            call.worksheet.update("C6:C7", [["1,0"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("C6:C6", ANY),
            call.worksheet.update("D6:D7", [["Seller"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("D6:D6", ANY),
            call.worksheet.update("E6:E7", [["01.01.2022"]], value_input_option="USER_ENTERED"),
            call.worksheet.format("E6:E6", ANY),
        ]

    def test_save_empty(self):
        with pytest.raises(ValueError) as ei:
            Purchase.save(
                "01.2022",
                [],
                PurchaseConfig("A", "B", "C", "D", "E", "F", 0),
                "creds.json",
                "very-long-spreadsheet-id",
            )
        assert str(ei.value) == "Empty purchases list"
