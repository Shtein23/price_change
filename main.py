from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import math
import configparser


def price_change(driver, admin_panel, email, password, coeff):

    # Переход на страницу авторизации
    driver.get(admin_panel)

    # Поиск input для ввода почты
    email_input = driver.find_element(by=By.XPATH, value='//input[@name="email"]')

    sleep(2)

    # Ввод почты
    email_input.click()
    email_input.send_keys(email)
    email_input.submit()

    sleep(1)

    # Поиск input для ввода пароля
    password_input = driver.find_element(by=By.XPATH, value='//input[@name="password"]')
    # Ввод пароля
    password_input.send_keys(password)
    password_input.submit()

    sleep(1)
    # Загрузка информации
    ex_data = pd.read_excel('Price.xlsx')

    # Создание массивов из необходимых столбцов
    links = ex_data['Links'].tolist()
    prices = ex_data['Price'].tolist()

    sleep(1)

    # len(links)
    for x in range(len(links)):
        # Проверка на пустую строку
        if not is_nan(links[x]):

            # Переход на страницу продукта
            driver.get(links[x])

            # Переход в настройки страницы
            driver.find_element(by=By.XPATH, value='//span[text()="Настройки страницы"]').click()

            # Поиск поля input для ввода цены
            elem = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div[2]/'
                                                          'div[5]/div[2]/div/div[2]/div/div/div[7]/input')

            sleep(1)

            # Очистка предыдущего значения
            elem.clear()
            elem.click()

            if not is_nan(prices[x]):
                # Вычисление новой цены
                cen = int((math.ceil((prices[x] * coeff) / 100)) * 100)

                # Проверка checkbox-а "Под заказ"
                if driver.find_element(by=By.XPATH, value='// *[ @ id = "isOrder"]').get_attribute('checked'):
                    driver.find_element(by=By.XPATH, value='// *[ @ id = "isOrder"]').click()
                else:
                    pass

                # Ввод цены
                elem.send_keys(cen)

            else:
                # Установить "Под заказ"
                if driver.find_element(by=By.XPATH, value='// *[ @ id = "isOrder"]').get_attribute('checked'):
                    pass
                else:
                    driver.find_element(by=By.XPATH, value='// *[ @ id = "isOrder"]').click()

            # Нажатие на кнопку "Сохранить"
            driver.find_element(by=By.XPATH, value='// *[ @ id = "__layout"] / div / div[2] / div[5] / div[2] / div '
                                                   '/ div[2] / div / div / div[10] / button ').click()

            sleep(1)

        else:
            pass


# Проверка на NaN
def is_nan(x):
    return x != x


if __name__ == '__main__':

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")           # считываем настройки

    # Initialize Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r"/chromedriver98.exe")

    price_change(driver=driver, admin_panel=config["site_1"]["admin_panel"], email=config["site_1"]["email"],
                 password=config["site_1"]["password"], coeff=config["site_1"]["coeff"])


