# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import sleep, perf_counter
from traceback import format_exc

from loguru import logger
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def clear_download():
    logger.debug("Clear download")
    for r_, d_, f_ in os.walk('download'):
        for file_ in f_:
            remove_file_name = os.path.join(r_, file_)
            os.remove(remove_file_name)
            logger.debug(f"Remove {remove_file_name}")
    logger.debug("Clear download... done")


def wait_file(file_name: str, pause=0.1, timeout=10):
    def check_file() -> bool:
        for r_, d_, f_ in os.walk('download'):
            for file_ in f_:
                if file_ == file_name:
                    return True

        return False

    start = perf_counter()
    while True:
        sleep(pause)
        if check_file():
            return
        if perf_counter() - start >= timeout:
            raise RuntimeError(f"Wait file '{file_name}' is timed out")


def get_check(check_photo_file_name: str):
    check_photo_file_name = os.path.normpath(os.path.abspath(check_photo_file_name))

    clear_download()

    driver = None
    try:
        options = ChromeOptions()
        current_directory = os.path.abspath(os.path.join(os.path.curdir, 'download'))

        options.add_experimental_option("prefs", {
            "download.default_directory": current_directory,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        })
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        s = Service(os.environ['CHROMEDRIVER_EXE_PATH'])

        driver = Chrome(service=s, chrome_options=options)
        wait = WebDriverWait(driver, 30)

        driver.get("https://proverkacheka.com/")

        photo = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div[2]/ul/li[3]/a")))
        assert (photo is not None)

        scroll_to_photo_action = ActionChains(driver)
        scroll_to_photo_action.move_to_element(photo).perform()

        photo.click()

        select_file = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             "/html/body/div/div[2]/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div/form/div[1]/div/span[1]/input")
        ))

        select_file.send_keys(check_photo_file_name)

        sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        save_file = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div[2]/div[3]/button")
        ))
        save_file.click()

        save_json = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div[2]/div[3]/ul/li[2]/a")
        ))
        save_json.click()

        wait_file('check.json')
    except Exception:
        file_name, _ = check_photo_file_name.split('.')
        with open(f"{file_name}.txt", 'w+') as error_file:
            error_file.write(format_exc())
        driver.save_screenshot(f"{file_name}_screenshot.png")

    finally:
        if driver is not None:
            driver.close()
