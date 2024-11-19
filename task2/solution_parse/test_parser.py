import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import os

# Импортируем функции из первого скрипта
from solution import get_animals_count, save_to_csv


class TestWikiParserScript(unittest.TestCase):
    def setUp(self):
        # Подготовка тестовых данных
        self.test_html = """
        <div class="mw-category-group">
            <a href="/wiki/Animal1">Абрикосовая рыба</a>
            <a href="/wiki/Animal2">Белка</a>
            <a href="/wiki/Animal3">Верблюд</a>
            <a href="/wiki/Service">Служебная:Test</a>
            <a href="/wiki/Category">Категория:Animals</a>
        </div>
        """
        self.test_data = {'А': 1, 'Б': 1, 'В': 1}

    @patch('requests.get')
    def test_get_animals_count(self, mock_get):
        # Настраиваем мок для requests.get
        mock_response = MagicMock()
        mock_response.text = self.test_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем тестируемую функцию
        result = get_animals_count()

        # Проверяем результаты
        self.assertIsInstance(result, dict)
        self.assertTrue(all(isinstance(k, str) for k in result.keys()))
        self.assertTrue(all(isinstance(v, int) for v in result.values()))

    def test_save_to_csv(self):
        # Тестируем сохранение в CSV
        test_filename = 'test_beasts.csv'

        # Вызываем функцию сохранения
        with patch('builtins.open') as mock_open:
            save_to_csv(self.test_data)
            mock_open.assert_called_once()

    def test_data_structure(self):
        # Проверяем структуру данных
        result = get_animals_count()
        self.assertIsInstance(result, dict)
        for key, value in result.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, int)
            self.assertEqual(len(key), 1)  # Ключ должен быть одной буквой


if __name__ == '__main__':
    unittest.main()
