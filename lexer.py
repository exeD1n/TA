import re
import difflib

# Таблица №1 ключевых слов языка M
keywords = {
    "program", "var", "begin", "end", "let", "if", "then", "else", "end_else", 
    "for", "do", "while", "loop", "input", "output", "%", "!", "$"
}

# Таблица №2 разделителей языка M
delimiters = {
    "<>", "<", "<=", ">", ">=", "or", "and", "not", "+", "-", "*", "/", ";", 
    ",", "}", "{", "(", ")", "пробел", ".", "=", "#"
}

# Регулярные выражения для чисел и булевых значений
number_regex = r"^[-+]?\d+\.\d+$|^[-+]?\d+$"  # Для чисел (целые и вещественные)
boolean_regex = r"^true$|^false$"  # Для булевых значений

# Регулярные выражения для переменных (строки начинаются с %, ! или $)
variable_regex = r"^[%!$]\s*(\w+(\s*,\s*\w+)*)\s*$"  # Ищем переменные, разделённые запятой

def parse_file(file_path):
    try:
        # Открытие файла для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            # Чтение содержимого файла
            content = file.read()

            # Удаление комментариев (между # и #)
            content = re.sub(r'#.*#', '', content)  # Удаляем комментарии

            # Разбиение на слова и символы
            tokens = re.findall(r'\w+|[^\w\s]', content)  # \w+ - слова, [^\w\s] - все остальные символы

            # Список для токенов, которых нет в таблицах
            unknown_tokens = []
            lex_error_tokens = []

            # Список переменных
            variables = set()
            variable_errors = []

            # Проход по строкам в файле для поиска переменных
            lines = content.splitlines()
            for line in lines:
                match = re.match(variable_regex, line.strip())  # Поиск строк с переменными
                if match:
                    # Извлекаем переменные из строки
                    var_list = match.group(1).split(',')
                    var_list = [var.strip() for var in var_list]  # Убираем лишние пробелы

                    # Проверка на переменные, начинающиеся с цифры
                    for var in var_list:
                        if var[0].isdigit():
                            variable_errors.append(f"[Error] Лексическая ошибка: переменная '{var}' не может начинаться с числа.")
                        else:
                            variables.add(var)

            # Проход по токенам и проверка их принадлежности к ключевым словам или разделителям
            for token in tokens:
                # Проверка на число или булевое значение
                if re.match(number_regex, token) or re.match(boolean_regex, token):
                    continue  # Пропускаем числа и булевы значения

                if token in variables:
                    continue  # Пропускаем переменные

                if token not in keywords and token not in delimiters:
                    unknown_tokens.append(token)

                    # Проверка на возможную лексическую ошибку (похоже на ключевое слово)
                    closest_keyword = difflib.get_close_matches(token, keywords, n=1, cutoff=0.8)
                    if closest_keyword:
                        lex_error_tokens.append(f"[Error] Лексическая ошибка: '{token}' возможно вы имели в виду '{closest_keyword[0]}'")
                    else:
                        # Если токен не является числом и не похоже на ключевое слово, это ошибка
                        lex_error_tokens.append(f"[Error] Лексическая ошибка: '{token}' не является допустимым токеном.")

            # Проверка на наличие ошибок
            if not lex_error_tokens and not variable_errors and not unknown_tokens:
                return "Лексический анализ ОК"

            return unknown_tokens, lex_error_tokens, variables, variable_errors

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
