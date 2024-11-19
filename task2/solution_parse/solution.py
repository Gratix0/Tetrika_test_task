import requests
import csv
from collections import defaultdict
import logging
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


def get_animals_count():
    """
    Собирает статистику животных по первым буквам их названий
    из русскоязычной Википедии, парсируя HTML со всех подкатегорий
    """
    base_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    animals_by_letter = defaultdict(int)
    total_animals = 0

    logging.info("Начинаем сбор данных с Википедии...")

    try:
        # Получаем HTML-страницу с основной категорией
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все ссылки на животных
        animal_links = soup.find_all('a', href=True)

        for link in animal_links:
            # Пропускаем служебные ссылки
            if 'Категория:' in link.text:
                continue

            animal_name = link.text.strip()
            if animal_name and not animal_name.startswith('Служебная:'):
                first_letter = animal_name[0].upper()
                animals_by_letter[first_letter] += 1
                total_animals += 1
                logging.debug(f"Обработано животное: {animal_name}")

        # Проверяем наличие ссылки на следующую страницу
        next_link = soup.find('a', text='Следующая страница')
        while next_link and 'href' in next_link.attrs:
            next_url = urljoin(base_url, next_link['href'])
            logging.info(f"Переход на следующую страницу: {next_url}")

            response = requests.get(next_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            animal_links = soup.find_all('a', href=True)
            for link in animal_links:
                if 'Категория:' in link.text:
                    continue

                animal_name = link.text.strip()
                if animal_name and not animal_name.startswith('Служебная:'):
                    first_letter = animal_name[0].upper()
                    animals_by_letter[first_letter] += 1
                    total_animals += 1
                    logging.debug(f"Обработано животное: {animal_name}")

            next_link = soup.find('a', text='Следующая страница')

        logging.info(f"Сбор данных завершен. Всего обработано {total_animals} записей")

    except requests.RequestException as e:
        logging.error(f"Ошибка при получении данных: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

    return animals_by_letter


def save_to_csv(data):
    """
    Сохраняет собранную статистику в CSV файл
    Args:
        data: словарь с количеством животных по буквам
    """
    try:
        # Сортируем буквы по алфавиту
        sorted_data = sorted(data.items())

        # Записываем в CSV файл
        with open('beasts.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for letter, count in sorted_data:
                writer.writerow([letter, count])
                logging.debug(f"Записана буква {letter}: {count} животных")

        logging.info(f"Данные успешно сохранены в файл 'beasts.csv'")

        # Выводим краткую статистику
        total = sum(count for _, count in sorted_data)
        logging.info(f"Всего букв: {len(sorted_data)}")
        logging.info(f"Общее количество записей: {total}")

    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")
        raise


def main():
    """
    Основная функция программы
    """
    start_time = time.time()
    logging.info("Программа запущена")

    try:
        animals_count = get_animals_count()
        save_to_csv(animals_count)

        # Выводим время выполнения
        execution_time = time.time() - start_time
        logging.info(f"Программа завершена успешно. Время выполнения: {execution_time:.2f} секунд")

    except Exception as e:
        logging.error(f"Программа завершилась с ошибкой: {e}")


if __name__ == "__main__":
    main()
