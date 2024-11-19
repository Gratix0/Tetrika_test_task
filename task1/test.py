import pytest
from solution import strict

# Пример функций с декоратором @strict
@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def concat_strings(a: str, b: str) -> str:
    return a + b

@strict
def is_even(a: int) -> bool:
    return a % 2 == 0

@strict
def divide(a: float, b: float) -> float:
    return a / b

@strict
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Тесты
def test_sum_two_valid():
    assert sum_two(3, 4) == 7

def test_sum_two_invalid_type():
    with pytest.raises(TypeError, match="Argument 'b' must be of type int"):
        sum_two(3, "4")

def test_concat_strings_valid():
    assert concat_strings("Hello, ", "world!") == "Hello, world!"

def test_concat_strings_invalid_type():
    with pytest.raises(TypeError, match="Argument 'a' must be of type str"):
        concat_strings(5, "world!")

def test_is_even_valid():
    assert is_even(4) is True

def test_is_even_invalid_type():
    with pytest.raises(TypeError, match="Argument 'a' must be of type int"):
        is_even(3.5)

def test_divide_valid():
    assert divide(10.0, 2.0) == 5.0

def test_divide_invalid_type():
    with pytest.raises(TypeError, match="Argument 'a' must be of type float"):
        divide("10.0", 2.0)

def test_greet_valid():
    assert greet("Alice") == "Hello, Alice!"

def test_greet_invalid_type():
    with pytest.raises(TypeError, match="Argument 'name' must be of type str"):
        greet(12345)
