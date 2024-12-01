import re  # Для обработки чисел в экспоненциальной записи

# Таблица ключевых слов
KEYWORDS = [
    "program", "var", "begin", "end", "let", "if", "then", "else", "end_else",
    "for", "do", "while", "loop", "input", "output", "%", "!", "$"
]
# Таблица разделителей
DELIMITERS = [
    "<>", "<", "<=", ">", ">=", "or", "and", "not", "+", "-", "*", "/", ";", ",",
    "(", ")", "{", "}", "=", "#", ".", " "
]

def parse_program(file_path):
    try:
        # Открытие исходного файла
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Удаление комментариев и пустых строк
        cleaned_lines = []
        for line in lines:
            # Удаляем комментарий, если он есть
            line = line.split('#')[0].strip()
            # Добавляем строку в результат, если она не пустая
            if line:
                cleaned_lines.append(line)

        # Проверка наличия второй строки и извлечение переменных
        if len(cleaned_lines) > 1:
            variable_line = cleaned_lines[1]  # Вторая строка
            # Удаляем префикс (%, !, $) и делим переменные
            variables = [var.strip() for var in variable_line[1:].split(",") if var.strip()]
        else:
            variables = []

        # Список значений
        values = []

        # Регулярное выражение для вещественных чисел (включая экспоненциальную запись)
        float_regex = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$')

        # Замена ключевых слов, разделителей, переменных и значений
        processed_lines = []
        for line_index, line in enumerate(cleaned_lines):
            tokens = line.split()  # Разбиваем строку на токены
            new_line = []
            for token in tokens:
                if token in KEYWORDS:
                    index = KEYWORDS.index(token)  # Номер ключевого слова
                    new_line.append(f"(1,{index})")  # Заменяем ключевое слово
                elif token in DELIMITERS:
                    index = DELIMITERS.index(token)  # Номер разделителя
                    new_line.append(f"(2,{index})")  # Заменяем разделитель
                elif token in variables:
                    index = variables.index(token)  # Номер переменной
                    new_line.append(f"(3,{index})")  # Заменяем переменную
                elif token.isdigit() or float_regex.match(token):
                    # Обработка чисел (целые, вещественные, экспоненциальные)
                    value = float(token) if '.' in token or 'e' in token.lower() else int(token)
                    if value not in values:
                        values.append(value)  # Добавляем уникальное значение
                    index = values.index(value)  # Номер значения
                    new_line.append(f"(4,{index})")  # Заменяем значение
                elif token.lower() in ["true", "false"]:
                    # Обработка логических значений (boolean)
                    value = token.lower() == "true"
                    if value not in values:
                        values.append(value)  # Добавляем уникальное значение
                    index = values.index(value)  # Номер значения
                    new_line.append(f"(4,{index})")  # Заменяем значение
                else:
                    new_line.append(token)  # Оставляем неизменённым
            processed_lines.append(" ".join(new_line))

        # Запись результата в файл parse.txt
        with open("parse.txt", "w", encoding="utf-8") as output_file:
            # Записываем обработанную программу
            for line in processed_lines:
                output_file.write(line + "\n")

        print("Обработка завершена. Результаты сохранены в файл parse.txt.")

    except FileNotFoundError:
        print(f"[Error] Файл {file_path} не найден.")
    except Exception as e:
        print(f"[Error] Произошла ошибка: {e}")


def replace_spaces_in_parse_file():
    """
    Заменяет пробелы в файле `parse.txt` на токены из таблицы разделителей.
    """
    try:
        # Открываем файл parse.txt для чтения
        with open("parse.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Номер пробела в таблице разделителей
        space_index = DELIMITERS.index(" ")

        # Замена пробелов на (2, space_index)
        updated_lines = []
        for line in lines:
            updated_line = line.replace(" ", f" (2,{space_index}) ")
            updated_lines.append(updated_line.strip())

        # Запись обратно в файл parse.txt
        with open("parse.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(updated_lines))

    except FileNotFoundError:
        print("[Error] Файл parse.txt не найден.")
    except Exception as e:
        print(f"[Error] Произошла ошибка: {e}")
