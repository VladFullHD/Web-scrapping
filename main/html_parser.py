import os
from bs4 import BeautifulSoup
import re
import csv

class HTMLParser:
    """
    Собирает информацию из HTML-страниц, сохраненных при помощи HTMLCollector.
    Собирает наименование товара, цену и ссылки на товары.
    Сохраняет данные в csv-файл для последующей работы с полученной информацией.
    """


    def __init__(self, input_dir='html_pages', output_file='card_data.csv'):
        self.input_dir = input_dir
        self.output_file = output_file
        self.card_data = {}


    # Основная функция, которая запускает процесс сбора данных.
    def parse_all_files(self):
        # Перебирает собранные HTML-страницы в указанной директории.
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.html'):
                self.parse_single_file(filename)
            self.save_to_csv()


    # Функция чтения HTML-страницы в заданной директории и запись в объект BeautifulSoup.
    def parse_single_file(self, filename):
        filepath = os.path.join(self.input_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        self.extract_card_data(soup, filename)


    # Сам процесс работы с HTML-кодом.
    def extract_card_data(self, soup, filename):
        data = soup.find_all('div', class_='catalog-form__offers-flex')
        name_tag = 'catalog-form__link catalog-form__link_primary-additional catalog-form__link_base-additional catalog-form__link_font-weight_semibold catalog-form__link_nodecor'
        special_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_error-alter catalog-form__link_huge-additional catalog-form__link_font-weight_bold'
        main_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_primary-additional catalog-form__link_huge-additional catalog-form__link_font-weight_bold'
        none_price_tag = 'catalog-form__description catalog-form__description_primary catalog-form__description_condensed-additional catalog-form__description_font-weight_bold catalog-form__description_middle'

        card_prices = []

        # Сбор цен на видеокарту.
        for card in data:
            # Ищет цену по определенному атрибуту класса.
            price = card.find('a', class_=main_price_tag)
            if price: # Проверка на None
                # Очистка найденной информации от лишних символов.
                price = price.text.strip()
                price = re.sub(r"[^\d,]", "", price).strip()
                # Добавление полученной цены в список card_prices.
                card_prices.append(price)

            # Если цена не была найдена в указанном атрибуте класса - ищем в другом.
            elif card.find('a', class_=special_price_tag):
                price = card.find('a', class_=special_price_tag).text.strip()
                # Очистка найденной информации от лишних символов.
                r_index = price.find('р')
                price = price[:r_index].strip()
                price = re.sub(r"[^\d,]", "", price).strip()
                # Добавление полученной цены в список card_prices.
                card_prices.append(price)

            # Если цена не была найдена в указанном атрибуте класса - ищем в другом.
            else:
                price = card.find('div', none_price_tag).text.strip()
                if price: # Проверка на None
                    card_prices.append(price)
                else: # Показывает, в каком файле цена не была найдена и выдает соответствующее сообщение.
                    print(f'Цена не найдена на странице: {filename}')
                    card_prices.append(None)


        # Собираем информацию по названиям видеокарт.
        card_names = []
        for card in data:
            name = card.find('a', name_tag).text.strip()
            card_names.append(name)

        # Собираем ссылки на видеокарты.
        card_urls = []
        for card in data:
            url = card.find('a', name_tag)['href']
            card_urls.append(url)

        for name, price, url in zip(card_names, card_prices, card_urls):
            self.card_data[name] = {'Price': price, 'URL': url}


    # Сохраняет полученные данные в csv-файл.
    def save_to_csv(self):
        with open(self.output_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'URL'])
            for name, data in self.card_data.items():
                writer.writerow([name, data['Price'], data['URL']])