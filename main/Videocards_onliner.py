import re
import os
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import json
import csv


url = 'https://catalog.onliner.by/videocard'

# Создаем объект ChromeOptions для настройки параметров запуска
options = webdriver.ChromeOptions()

# Создаем словарь с заголовками
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Перебираем все заголовки в словаре и добавляем каждый заголовок в ChromeOptions
for header, value in headers.items():
    options.add_argument(f'--header={header}:{value}')

# Запуск браузера с указанными опциями
driver = webdriver.Chrome(options=options)
# Открытие окна в полный экран (тем самым убираем окно MiniPay)
driver.maximize_window()

# Создаем директорию для сбора всех страниц
if not os.path.exists('html_pages'):
    os.makedirs('html_pages')

# Указываем количество страниц
num_pages = 59

# Открытие заданного количества страниц, прокрутка вниз и сохранение страницы
for page_num in range(1, num_pages + 1):
    our_url = url + f"?page={page_num}" # Формируем URL текущей страницы

    driver.get(our_url)
    time.sleep(3)

    # Создаем объект ActionChains
    actions = ActionChains(driver)
    # Прокрутка страницы вниз 5 раз
    num_presses = 9
    for press in range(num_presses):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)

    # Сохраняем страницу в папку
    filename = f'html_pages/page_{page_num}.html'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    print(f'Сохранена страница {page_num} из {num_pages}')

    time.sleep(2)

# Выходим из браузера
driver.quit()

# with open('onliner_videocards.html', encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# # Необходимые блоки, по которым ищем нужную информацию
# data = soup.find_all('div', class_= 'catalog-form__offers-flex')
# name_tag = 'catalog-form__link catalog-form__link_primary-additional catalog-form__link_base-additional catalog-form__link_font-weight_semibold catalog-form__link_nodecor'
# special_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_error-alter catalog-form__link_huge-additional catalog-form__link_font-weight_bold'
# main_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_primary-additional catalog-form__link_huge-additional catalog-form__link_font-weight_bold'
#
# # Собираем информацию по ценам, цены делятся на спец. предложение и стандартные цены
# card_prices = []
# for card in data:
#     price = card.find('a', class_= main_price_tag)
#     if price:
#         price = price.text.strip()
#         price = re.sub(r"[^\d,]", "", price).strip()
#         card_prices.append(price)
#     else:
#         price = card.find('a', class_=special_price_tag).text.strip()
#         r_index = price.find('р')
#         price = price[:r_index].strip()
#         price = re.sub(r"[^\d,]", "", price).strip()
#         card_prices.append(price)
#
# # Собираем информацию по названиям видеокарт
# card_names = []
# for card in data:
#     name = card.find('a', name_tag).text.strip()
#     card_names.append(name)
#
# # Собираем ссылки на видеокарты
# card_urls = []
# for card in data:
#     url = card.find('a', name_tag)['href']
#     card_urls.append(url)
#
# # Создаем вложенный словарь, где ключ - имя видеокарты, а значение - Price и URL
# card_data = {}
# for name, price, url in zip(card_names, card_prices, card_urls):
#     card_data[name] = {'Price': price, 'URL': url}
#
# # Запись полученных данных в csv-файл для последующей выгрузки в Excel-таблицу
# with open('card_data_csv.csv', 'w', encoding='utf-8', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Name', 'Price', 'URL'])
#     for name, data in card_data.items():
#         writer.writerow([name, data['Price'], data['URL']])
