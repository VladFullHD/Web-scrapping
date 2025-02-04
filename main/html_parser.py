import os
from bs4 import BeautifulSoup
import re
import csv

class HTMLParser:

    def __init__(self, input_dir='html_pages', output_file='card_data.csv'):
        self.input_dir = input_dir
        self.output_file = output_file
        self.card_data = {}

    def parse_all_files(self):
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.html'):
                self.parse_single_file(filename)
            self.save_to_csv()

    def parse_single_file(self, filename):
        filepath = os.path.join(self.input_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        self.extract_card_data(soup)

    def extract_card_data(self, soup):
        data = soup.find_all('div', class_='catalog-form__offers-flex')
        name_tag = 'catalog-form__link catalog-form__link_primary-additional catalog-form__link_base-additional catalog-form__link_font-weight_semibold catalog-form__link_nodecor'
        special_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_error-alter catalog-form__link_huge-additional catalog-form__link_font-weight_bold'
        main_price_tag = 'catalog-form__link catalog-form__link_nodecor catalog-form__link_primary-additional catalog-form__link_huge-additional catalog-form__link_font-weight_bold'

        card_prices = []
        for card in data:
            price = card.find('a', class_=main_price_tag)
            if price:
                price = price.text.strip()
                price = re.sub(r"[^\d,]", "", price).strip()
                card_prices.append(price)
            else:
                price = card.find('a', class_=special_price_tag).text.strip()
                r_index = price.find('р')
                price = price[:r_index].strip()
                price = re.sub(r"[^\d,]", "", price).strip()
                card_prices.append(price)

        # Собираем информацию по названиям видеокарт
        card_names = []
        for card in data:
            name = card.find('a', name_tag).text.strip()
            card_names.append(name)

        # Собираем ссылки на видеокарты
        card_urls = []
        for card in data:
            url = card.find('a', name_tag)['href']
            card_urls.append(url)

        for name, price, url in zip(card_names, card_prices, card_urls):
            self.card_data[name] = {'Price': price, 'URL': url}

    def save_to_csv(self):
        with open(self.output_file, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'URL'])
            for name, data in self.card_data.items():
                writer.writerow([name, data['Price'], data['URL']])