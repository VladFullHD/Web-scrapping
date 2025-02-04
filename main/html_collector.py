import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class HTMLCollector:
    """
    При помощи этого класса мы можем открывать необходимое количество страниц
    и сохранять их в файл HTML для последующей обработки парсером.
    """

    def __init__(self, url, num_pages, output_dir='html_pages', scroll_presses=9, scroll_delay=1, request_delay=2):
        self.url = url # Адрес страницы
        self.num_pages = num_pages # Количество страниц (пагинация)
        self.output_dir = output_dir # Название папки для сохранения HTML-страниц
        self.scroll_presses = scroll_presses # Количество нажатий на клавишу Page Down
        self.scroll_delay = scroll_delay # Задержка между нажатиями на клавишу Page Down
        self.request_delay = request_delay # Задержка между переходами к след. действию
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
        # Отключаем сообщение о принятии cookies
        options.add_argument("--disable-cookie-consent")
        # Запуск браузера с указанными опциями
        self.driver = webdriver.Chrome(options=options)
        # Открытие окна браузера в полный экран (сделал конкретно под onliner.by)
        self.driver.maximize_window()
        # Создаем директорию для сбора всех страниц
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return self


    def __exit__(self, *args):
        if self.driver:
            self.driver.quit()


    def collect_pages(self):
        # Открываем заданное кол-во страниц
        for page_num in range(1, self.num_pages + 1):
            our_url = self.url + f"?page={page_num}"
            self.driver.get(our_url)
            time.sleep(self.request_delay)

            # Прокрутка страницы вниз заданное кол-во раз
            actions = ActionChains(self.driver)
            for _ in range(self.scroll_presses):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(self.scroll_delay)

            # Сохранение кода страницы в указанную директорию
            filename = os.path.join(self.output_dir, f'page_{page_num}.html')
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.driver.page_source)
            print(f'Сохранена страница {page_num} из {self.num_pages}')
            time.sleep(self.request_delay)



