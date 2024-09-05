import json
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from lxml import html
import re

# Установка ChromeDriver автоматически
# service = Service(executable_path=ChromeDriverManager().install())
#
# chrome_options = Options()
#
# driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://catalog.onliner.by/videocard"

# # Открытие страницы с помощью WebDriver
# driver.get(url)
#
# # Ждем несколько секунд для полной загрузки страницы
# time.sleep(5)
#
# # Получаем HTML-код страницы после полной загрузки
# src = driver.page_source
#
# #Закрываем WebDriver
# driver.quit()

# #Сохраняем HTML-код в файл
# with open('page.html', 'w', encoding='utf-8') as file:
#     file.write(src)
# print('HTML-код страницы успешно сохранен в файл "page.html"!')

#Читаем HTML-код из файла
with open('page.html', 'r', encoding='utf-8') as file:
    src = file.read()

# Парсим HTML с помощью BeautifulSoup
soup = BeautifulSoup(src, 'lxml')

all_elements_url = soup.find_all(class_='catalog-form__link catalog-form__link_primary-additional catalog-form__link_base-additional catalog-form__link_font-weight_semibold catalog-form__link_nodecor')

#Проходимся циклом по полученным данным о видеокартах и сохраняем в словарик значение в виде
#Видеокарта: Ссылка
all_items_dict = {}
for item in all_elements_url:
    item_text = item.text.strip()
    item_href = item.get('href')

    all_items_dict[item_text] = item_href
print(all_items_dict)

with open('all_items_dict.json', 'w') as file:
    json.dump(all_items_dict, file, indent=4, ensure_ascii=False)

