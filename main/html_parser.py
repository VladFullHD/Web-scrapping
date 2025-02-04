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