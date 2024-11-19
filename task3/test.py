import pytest
from solution import appearance  # Импорт функции appearance

@pytest.mark.parametrize("intervals, expected", [
    # Тест 1: Пересечения присутствуют
    (
        {
            "lesson": [10, 50],
            "pupil": [10, 15, 25, 40, 45, 50],
            "tutor": [15, 20, 30, 35, 40, 50]
        },
        10
    ),
    # Тест 2: Ученик и учитель полностью пересекаются
    (
        {
            "lesson": [10, 50],
            "pupil": [10, 50],
            "tutor": [10, 50]
        },
        40
    ),
    # Тест 3: Нет пересечений (учитель и ученик не встречались на уроке)
    (
        {
            "lesson": [10, 50],
            "pupil": [10, 20, 30, 40],
            "tutor": [21, 29, 41, 50]
        },
        0
    ),
    # Тест 4: Учитель отсутствует
    (
        {
            "lesson": [10, 50],
            "pupil": [10, 50],
            "tutor": []
        },
        0
    ),
    # Тест 5: Ученик отсутствует
    (
        {
            "lesson": [10, 50],
            "pupil": [],
            "tutor": [10, 50]
        },
        0
    ),
])
def test_appearance(intervals, expected):
    """
    Тестирование функции appearance с различными наборами данных.
    """
    assert appearance(intervals) == expected
