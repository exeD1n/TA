import sys
from lexer import parse_file
# from syntax import check_syntax
from semantix import check_semantics
from test import check_syntax

def main():
    # Проверка наличия аргумента (имени файла)
    if len(sys.argv) != 2:
        print("Использование: python main.py <имя_файла>")
        return

    file_path = sys.argv[1]  # Получаем имя файла из аргументов командной строки

    # Выполнение лексического анализа
    print("\n--- Лексический анализ ---")
    lex_result = parse_file(file_path)

    if isinstance(lex_result, str):
        # Если результат - строка, то лексический анализ прошел успешно
        print(lex_result)
    else:
        # Если есть ошибки, выводим их и завершаем выполнение
        unknown_tokens, lex_error_tokens, variables, variable_errors = lex_result

        if lex_error_tokens:
            print("Лексические ошибки:")
            for error in lex_error_tokens:
                print(f"  {error}")

        if variable_errors:
            print("\nОшибки в переменных:")
            for error in variable_errors:
                print(f"  {error}")

        print("\nЛексический анализ завершился с ошибками. Исправьте их и повторите попытку.")
        return

    # Выполнение синтаксического анализа
    print("\n--- Синтаксический анализ ---")
    syntax_result = check_syntax(file_path)
    if syntax_result != "Синтаксический анализ ОК":
        print(syntax_result)
        print("\nСинтаксический анализ завершился с ошибками. Исправьте их и повторите попытку.")
        return

    print(syntax_result)

    # Выполнение семантического анализа
    print("\n--- Семантический анализ ---")
    semantic_result = check_semantics(file_path)
    print(semantic_result)

if __name__ == "__main__":
    main()
