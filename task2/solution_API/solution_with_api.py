import requests

import csv
from collections import defaultdict
import logging
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


def get_animals_count():
    """
    Собирает статистику животных по первым буквам их названий
    из русскоязычной Википедии используя API
    """
    base_url = "https://ru.wikipedia.org/w/api.php"
    animals_by_letter = defaultdict(int)
    page_count = 0
    total_animals = 0

    # Параметры для API запроса
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': 'Категория:Животные_по_алфавиту',
        'cmlimit': 500,  # Максимальное количество результатов за запрос
        'cmcontinue': None
    }

    logging.info("Начинаем сбор данных с Википедии...")

    while True:
        try:
            # Получаем данные через API
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            page_count += 1
            logging.info(f"Обработка пакета данных {page_count}...")

            # Обрабатываем животных в текущем пакете данных
            current_batch_animals = 0
            for item in data['query']['categorymembers']:
                animal_name = item['title']
                if animal_name:
                    first_letter = animal_name[0].upper()
                    animals_by_letter[first_letter] += 1
                    current_batch_animals += 1

            total_animals += current_batch_animals
            logging.info(f"В пакете обработано {current_batch_animals} записей. "
                         f"Всего обработано: {total_animals}")

            # Проверяем, есть ли еще данные
            if 'continue' not in data:
                logging.info("Достигнут конец списка")
                break

            # Обновляем параметр для следующего запроса
            params['cmcontinue'] = data['continue']['cmcontinue']

            # Добавляем небольшую задержку между запросами
            time.sleep(0.1)

        except requests.RequestException as e:
            logging.error(f"Ошибка при получении данных: {e}")
            break
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}")
            break

    logging.info(f"Сбор данных завершен. Всего обработано {total_animals} записей "
                 f"в {page_count} пакетах")
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
        with open('api_beasts.csv', 'w', newline='', encoding='utf-8') as file:
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
