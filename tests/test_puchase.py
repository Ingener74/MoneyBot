from unittest.mock import MagicMock, call, ANY

import pytest

from Purchase.Purchase import Purchase
from Purchase.PurchaseConfig import PurchaseConfig


class TestPurchase:
    def test_save(self, mocker):
        fake_worksheet = MagicMock()
        fake_worksheet.col_values = MagicMock(return_value=[
            '',
            '',
            '',
            '',
            'foo'
        ])
        fake_worksheet.update = MagicMock()
        fake_worksheet.format = MagicMock()

        fake_spreadsheet = MagicMock()
        fake_spreadsheet.worksheet = MagicMock(return_value=fake_worksheet)

        fake_client = MagicMock()
        fake_client.open_by_key = MagicMock(return_value=fake_spreadsheet)
        gspread_service_account: MagicMock = mocker.patch('gspread.service_account', return_value=fake_client)

        purchases = [
            Purchase('Soap', '1,0', '1,0', 'Seller', '01.01.2022')
        ]
        Purchase.save('01.2022', purchases, PurchaseConfig(
            'A', 'B', 'C', 'D', 'E', 0
        ), 'creds.json', 'very-long-spreadsheet-id')

        gspread_service_account.assert_has_calls([
            call(filename='creds.json')
        ])
        fake_client.open_by_key.assert_has_calls([
            call('very-long-spreadsheet-id')
        ])
        fake_spreadsheet.worksheet.assert_has_calls([
            call('01.2022')
        ])
        fake_worksheet.update.assert_has_calls([
            call('A6:A7', [['Soap']], value_input_option='USER_ENTERED')
        ])
        fake_worksheet.update.assert_has_calls([
            call('B6:B7', [['1,0']], value_input_option='USER_ENTERED')
        ])
        fake_worksheet.update.assert_has_calls([
            call('C6:C7', [['1,0']], value_input_option='USER_ENTERED')
        ])
        fake_worksheet.update.assert_has_calls([
            call('D6:D7', [['Seller']], value_input_option='USER_ENTERED')
        ])
        fake_worksheet.update.assert_has_calls([
            call('E6:E7', [['01.01.2022']], value_input_option='USER_ENTERED')
        ])
        fake_worksheet.format.assert_has_calls([
            call('A6:A6', ANY)
        ])

    def test_save_empty(self):
        with pytest.raises(ValueError) as ei:
            Purchase.save('01.2022', [], PurchaseConfig(
                'A', 'B', 'C', 'D', 'E', 0
            ), 'creds.json', 'very-long-spreadsheet-id')
        assert str(ei.value) == "Empty purchases list"
