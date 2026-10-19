import functools


def log(filename=None):
    """Декоратор логирует автоматически начало и конец выполнения функции,
    а также её результаты или возникшие ошибки"""
    def my_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f'{function.__name__} ok\n')
                else:
                    print(f'{function.__name__} ok\n')

                return result

            except Exception as e:
                error_message = (f'{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}')

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f'{error_message}\n')
                else:
                    print(f'{error_message}\n')

                raise

        return wrapper
    return my_decorator


if __name__ == '__main__':
