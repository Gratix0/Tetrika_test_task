def strict(func):
    """
    Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов,
    объявленным в прототипе функции.
    """
    def wrapper(*args, **kwargs):
        # Получаем аннотации аргументов функции
        annotations = func.__annotations__

        # Проверяем типы всех аргументов
        for arg_value, (arg_name, expected_type) in zip(args, annotations.items()):
            # Пропускаем аннотацию возвращаемого значения
            if arg_name == 'return':
                continue
            # Если тип аргумента не соответствует ожидаемому, выбрасываем исключение
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Argument '{arg_name}' must be of type {expected_type.__name__}, "
                    f"but got {type(arg_value).__name__}"
                )

        # Вызываем оригинальную функцию
        return func(*args, **kwargs)

    return wrapper
