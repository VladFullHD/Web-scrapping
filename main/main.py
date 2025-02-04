from html_collector import HTMLCollector
from html_parser import HTMLParser
import time

if __name__ == "__main__":
#     with HTMLCollector(
#         "https://catalog.onliner.by/videocard",
#         59,
#         'html_pages',
#         request_delay=1
#     ) as collector:
#
#         start_time = time.time()
#
#         collector.collect_pages()
#
#         end_time = time.time()
#
#         elapsed_time_seconds = end_time - start_time
#
#         minutes = int(elapsed_time_seconds // 60)
#         seconds = int(elapsed_time_seconds % 60)
#
#         print(f'Сбор страниц занял {minutes} минут, {seconds} секунд')


    start_time = time.time()

    parser = HTMLParser()
    parser.parse_all_files()

    end_time = time.time()

    elapsed_time_seconds = end_time - start_time

    minutes = int(elapsed_time_seconds // 60)
    seconds = int(elapsed_time_seconds % 60)

    print(f'Сбор информации из HTML-кода занял {minutes} минут, {seconds} секунд')
