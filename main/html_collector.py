from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from functools import lru_cache
import os
import time



class HTMLCollector:
    """
    При помощи этого класса мы можем открывать необходимое количество страниц
    и сохранять их в файл HTML для последующей обработки парсером.
    В начале работы автоматически открывается первая страница и происходит
    подсчёт количества страниц в разделе.
    """

    def __init__(self, url, output_dir='html_pages', scroll_presses=9, scroll_delay=1, request_delay=2):
        self.url = url # Адрес страницы
        self.output_dir = output_dir # Название папки для сохранения HTML-страниц
        self.scroll_presses = scroll_presses # Количество нажатий на клавишу Page Down
        self.scroll_delay = scroll_delay # Задержка между нажатиями на клавишу Page Down
        self.request_delay = request_delay # Задержка между переходами к след. действию
        self.driver = None

    # Собирает количество страниц, которые можно забрать в выбранном разделе
    @property
    def num_pages(self):
        return self.page_count()


    # Кэширует результат работы функции page_count
    @lru_cache(maxsize=1)
    def page_count(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        try:
            driver.get(self.url)

            # Принимаем куки во всплывающем окне
            cookie_accept = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-button"]')))
            driver.execute_script("arguments[0].click();", cookie_accept)
            time.sleep(2)

            # Прокручиваем страницу вниз
            actions = ActionChains(driver)
            for _ in range(9):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)

            # Открываем список с общим количеством страниц
            pagination_list = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#container > div > div > div > div > div.catalog-content > '
                                            'div.catalog-wrapper > div > div > div.catalog-form__tabs > div > div > '
                                            'div > div > div.catalog-form__filter-part.catalog-form__filter-part_2 > '
                                            'div.catalog-pagination.catalog-pagination_visible > div > div')))
            driver.execute_script("arguments[0].click();", pagination_list)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Извлекаем количество страниц
            find_pages = [page.text.strip() for page in soup.find_all('li', class_='catalog-pagination__pages-item')]
            count_pages = len(find_pages)

            return count_pages

        except Exception as e:
            print(f'Произошла ошибка: {e}')
            return None

        finally:
            driver.quit()


    def __enter__(self):
        # Создаем объект ChromeOptions для настройки параметров запуска
        options = webdriver.ChromeOptions()
        # Создаем словарь с заголовками
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
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

    # Собирает необходимое кол-во страниц
    def collect_pages(self):
        # Открываем необходимое кол-во страниц
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



