import unittest
from unittest.mock import patch, MagicMock
import json

# Импортируем функции из второго скрипта
from solution_with_api import get_animals_count, save_to_csv


class TestWikiApiScript(unittest.TestCase):
    def setUp(self):
        # Подготовка тестовых данных
        self.test_api_response = {
            'query': {
                'categorymembers': [
                    {'title': 'Абрикосовая рыба'},
                    {'title': 'Белка'},
                    {'title': 'Верблюд'}
                ]
            }
        }
        self.test_data = {'А': 1, 'Б': 1, 'В': 1}

    @patch('requests.get')
    def test_get_animals_count(self, mock_get):
        # Настраиваем мок для requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = self.test_api_response
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
        test_filename = 'test_api_beasts.csv'

        # Вызываем функцию сохранения
        with patch('builtins.open') as mock_open:
            save_to_csv(self.test_data)
            mock_open.assert_called_once()

    def test_api_params(self):
        # Проверяем параметры API запроса
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.test_api_response
            mock_get.return_value = mock_response

            get_animals_count()

            # Проверяем, что запрос был сделан с правильными параметрами
            args, kwargs = mock_get.call_args
            self.assertIn('params', kwargs)
            params = kwargs['params']
            self.assertEqual(params['action'], 'query')
            self.assertEqual(params['format'], 'json')
            self.assertEqual(params['list'], 'categorymembers')

    def test_error_handling(self):
        # Проверяем обработку ошибок
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception('Test error')
            result = get_animals_count()
            self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
