import sys
from lexer import parse_file

def main():
    # Проверка на наличие аргумента
    if len(sys.argv) != 2:
        print("Использование: python main.py <имя_файла>")
        return

    file_path = sys.argv[1]  # Получаем имя файла из аргументов командной строки

    # Вызов функции парсинга
    result = parse_file(file_path)

    if isinstance(result, str):
        # Если результат - строка (успешный анализ)
        print(result)
    else:
        unknown_tokens, lex_error_tokens, variables, variable_errors = result

        # Вывод ошибок
        if lex_error_tokens:
            print("\nЛексические ошибки:")
            for error in lex_error_tokens:
                print(error)

        # Вывод ошибок в переменных
        if variable_errors:
            print("\nОшибки в переменных:")
            for error in variable_errors:
                print(error)

if __name__ == "__main__":
    main()
