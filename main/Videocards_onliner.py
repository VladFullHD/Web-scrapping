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

class HTMLCollector:
    # Инициализация
    def __init__(self, url, num_pages, output_dir='html_pages', scroll_presses=9, scroll_delay=1, request_delay=2):
        self.url = url
        self.num_pages = num_pages
        self.output_dir = output_dir
        self.scroll_presses = scroll_presses
        self.scroll.delay = scroll_delay
        self.request_delay = request_delay
        self.driver = None

    def __enter__(self):
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
        self.driver = webdriver.Chrome(options=options)
        # Открытие окна в полный экран (тем самым убираем окно MiniPay)
        self.driver.maximize_window()
        # Создаем директорию для сбора всех страниц
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return self

    def __exit__(self, *args):
        if self.driver:
            self.driver.quit()

    def collect_pages(self):
        # Открытие заданного количества страниц, прокрутка вниз и сохранение страницы
        for page_num in range(1, self.num_pages + 1):
            our_url = self.url + f"?page={page_num}"
            self.driver.get(our_url)
            time.sleep(self.request_delay)

            # Прокрутка страницы вниз N раз
            actions = ActionChains(self.driver)
            for _ in range(self.scroll_presses):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(self.request_delay)
            # Сохраняем страницу в папку
            filename = os.path.join(self.output_dir, f'page_{page_num}.html')
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.driver.page_source)
            print(f'Сохранена страница {page_num} из {self.num_pages}')

            time.sleep(self.request_delay)




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
