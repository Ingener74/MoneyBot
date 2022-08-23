from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt

from com_gui.mainwindow.main_window import MainWindow


class TestMainWindow:
    def test_open_file(self, qtbot, mocker, datadir):
        get_open_file_name_mock: MagicMock = mocker.patch("PySide6.QtWidgets.QFileDialog.getOpenFileName")
        get_open_file_name_mock.return_value = (str(datadir / "test_open_file/test_com.txt"), "txt")

        main_window = MainWindow()
        qtbot.addWidget(main_window)

        assert (datadir / "test_open_file/test_com.txt").is_file()

        assert main_window.ui.pushButtonSend.isEnabled() is False

        qtbot.mouseClick(main_window.ui.pushButtonOpen, Qt.LeftButton)

        def data(r, c):
            return main_window.ui.tableViewPurchases.model().index(r, c).data(Qt.DisplayRole)

        assert data(0, 0) == "МУП ПОВВ:ХВС ПОВЫШАЮЩИЙ КОЭФФИЦИЕНТ"
        assert data(0, 1) == "1,0"
        assert data(0, 2) == "120,82"
        assert data(0, 3) == 'МУП "ПОВВ"'
        assert data(0, 4) == "15.06.2022"

        assert data(1, 0) == "ТСН ГРИНПАРК 68: ЖИЛИЩНО-КОММУНАЛЬНЫЕ УСЛУГИ"
        assert data(1, 1) == "1,0"
        assert data(1, 2) == "2015,48"
        assert data(1, 3) == 'ТСН "ГРИНПАРК 68"'
        assert data(1, 4) == "15.06.2022"

        assert data(2, 0) == 'ЕРЦ УРАЛЭНЕРГОСБЫТ(ООО"НКР")ДЛЯ ООО УЭС,АО УСТЭК-ЧЕЛЯБ-СК: КОМ.'
        assert data(2, 1) == "1,0"
        assert data(2, 2) == "624,38"
        assert data(2, 3) == 'ОПЕРАТОР ООО "НКР" (ДЛЯ ООО "УРАЛЭНЕРГОСБЫТ" - Э/Э, ДЛЯ АО'
        assert data(2, 4) == "15.06.2022"

        assert data(3, 0) == "МУП ПОВВ:ВО"
        assert data(3, 1) == "1,0"
        assert data(3, 2) == "174,45"
        assert data(3, 3) == 'МУП "ПОВВ"'
        assert data(3, 4) == "15.06.2022"

        assert data(4, 0) == "МУП ПОВВ:ХВС"
        assert data(4, 1) == "1,0"
        assert data(4, 2) == "241,63"
        assert data(4, 3) == 'МУП "ПОВВ"'
        assert data(4, 4) == "15.06.2022"

        assert data(5, 0) == "УРАЛЖИЛСЕРВИС:ЗА ДОМОФОН"
        assert data(5, 1) == "1,0"
        assert data(5, 2) == "35,35"
        assert data(5, 3) == 'ООО "УРАЛЖИЛСЕРВИС"'
        assert data(5, 4) == "15.06.2022"

        assert data(6, 0) == "ООО ЦКС: УСЛУГИ ОБРАЩЕНИЯ С ТКО ЧЕЛЯБИНСКИЙ КЛАСТЕР"
        assert data(6, 1) == "1,0"
        assert data(6, 2) == "86,08"
        assert data(6, 3) == 'ООО "ЦКС"'
        assert data(6, 4) == "15.06.2022"

        assert data(7, 0) == "ТСН ГРИНПАРК 68: КАПИТАЛЬНЫЙ РЕМОНТ"
        assert data(7, 1) == "1,0"
        assert data(7, 2) == "661,02"
        assert data(7, 3) == 'ТСН "ГРИНПАРК 68"'
        assert data(7, 4) == "15.06.2022"

    # @pytest.mark.skip
    # def test_send(self, qtbot, mocker, datadir):
    #     get_open_file_name_mock: MagicMock = mocker.patch('PySide6.QtWidgets.QFileDialog.getOpenFileName')
    #     get_open_file_name_mock.return_value = (str(datadir / 'test_open_file/test_com.txt'), 'txt')
    #
    #     main_window = MainWindow()
    #     qtbot.addWidget(main_window)
    #
    #     assert (datadir / 'test_open_file/test_com.txt').is_file()
    #     assert main_window.ui.pushButtonSend.isEnabled() is False
    #
    #     qtbot.mouseClick(main_window.ui.pushButtonOpen, Qt.LeftButton)
    #
    #     assert main_window.ui.pushButtonSend.isEnabled() is True
    #
    #     qtbot.mouseClick(main_window.ui.pushButtonSend, Qt.LeftButton)
