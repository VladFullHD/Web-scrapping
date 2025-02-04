from html_collector import HTMLCollector
import time

if __name__ == "__main__":
    with HTMLCollector(
        "https://catalog.onliner.by/videocard",
        2,
        'html_pages'
    ) as collector:

        start_time = time.time()

        collector.collect_pages()

        end_time = time.time()

        elapsed_time_seconds = end_time - start_time

        minutes = int(elapsed_time_seconds // 60)
        seconds = int(elapsed_time_seconds % 60)

        print(f'Сбор страниц занял {minutes} минут, {seconds} секунд')