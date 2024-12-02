import re

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

# Функция перевода токена в бинарный код
def translate_token(token):
    # Сопоставление ключевых слов
    if token in keywords:
        return f"KW_{format(hash(token) % 256, '08b')}"  # Пример: KW_01010101
    # Сопоставление разделителей
    elif token in delimiters:
        return f"DL_{format(hash(token) % 256, '08b')}"  # Пример: DL_01101100
    # Числа
    elif re.match(r"^\d+(?:\.\d+)?(?:e[+-]?\d+)?$", token):
        return f"NUM_{format(int(float(token)), '016b')}"  # Пример: NUM_0000000010000001
    # Переменные
    elif re.match(r"^[a-zA-Z_][a-zA-Z_0-9]*$", token):
        return f"ID_{format(hash(token) % 256, '08b')}"  # Пример: ID_01111010
    # Неизвестный токен
    else:
        return "UNKNOWN"

# Функция обработки текста и записи результата
def parse_to_binary(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        binary_output = []
        for line in lines:
            # Удаление комментариев (всё после # считается комментарием)
            line = re.sub(r"#.*", "", line).strip()
            # Пропуск пустых строк
            if not line:
                continue
            # Разделение строки на токены
            tokens = re.findall(r"[a-zA-Z_][a-zA-Z_0-9]*|\d+(?:\.\d+)?(?:e[+-]?\d+)?|<>|<=|>=|[><=;,+*/\-\{\}\(\).]|[^\s]+", line)
            # Перевод токенов в бинарный формат
            binary_line = " ".join(translate_token(token) for token in tokens)
            binary_output.append(binary_line)

        with open(output_file, 'w', encoding='utf-8') as binary_file:
            binary_file.write("\n".join(binary_output))

        print(f"Файл '{input_file}' успешно обработан. Результат сохранён в '{output_file}'.")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
input_path = 'gg.m'  # Файл с кодом
output_path = 'program_binary.txt'  # Файл с результатом
parse_to_binary(input_path, output_path)
