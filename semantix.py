import re

def check_semantics(file_path):
    try:
        # Открытие файла для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Удаление пустых строк
        lines = [line.strip() for line in lines if line.strip()]

        # Регулярное выражение для корректного комментария
        comment_regex = r"^#.*#$"

        # Удаляем строки с комментариями
        lines = [line for line in lines if not re.match(comment_regex, line)]

        # Проверка первой строки
        if not lines or lines[0].lower() != "program var":
            return "[Error] Семантическая ошибка: программа должна начинаться с 'program var'."

        # Проверка второй строки и типа переменных
        if len(lines) < 2 or not lines[1].startswith(('%', '!', '$')):
            return "[Error] Семантическая ошибка: во второй строке должны быть объявлены переменные с '%', '!' или '$'."

        # Определение типа данных из символа
        variable_prefix = lines[1][0]
        if variable_prefix == '%':
            expected_type = 'int'
        elif variable_prefix == '!':
            expected_type = 'float'
        elif variable_prefix == '$':
            expected_type = 'boolean'
        else:
            return "[Error] Семантическая ошибка: некорректный символ для объявления переменных."

        # Проверяем, что переменные объявлены
        variables = lines[1][1:].strip()
        if not variables:
            return "[Error] Семантическая ошибка: во второй строке должны быть объявлены хотя бы одна переменная."

        # Проверка наличия `begin` и `end.`
        if len(lines) < 3 or lines[2].lower() != "begin":
            return "[Error] Семантическая ошибка: третья строка должна быть 'begin'."
        if lines[-1].lower() != "end.":
            return "[Error] Семантическая ошибка: последняя строка должна быть 'end.'."

        # Проверяем наличие кода между `begin` и `end.`
        code_lines = lines[3:-1]
        if not code_lines:
            return "Семантический анализ: Ok (программа без кода между begin и end.)"

        # Словарь типов данных
        data_types = {
            'int': r"^[-+]?\d+$",  # Целые числа
            'float': r"^[-+]?\d*\.\d+$",  # Вещественные числа
            'boolean': r"^(true|false)$"  # Булевы значения
        }

        # Определяем, используется ли только один тип данных
        detected_types = set()
        for line in code_lines:
            tokens = re.findall(r'\w+', line)  # Извлекаем все слова/переменные
            for token in tokens:
                for dtype, regex in data_types.items():
                    if re.match(regex, token):
                        detected_types.add(dtype)

        # Проверяем, используется ли только один тип данных
        if len(detected_types) > 1:
            return "[Error] Семантическая ошибка: программа должна использовать только один тип данных."

        # Проверяем, соответствует ли тип данных символу во второй строке
        if expected_type not in detected_types and code_lines:
            return f"[Error] Семантическая ошибка: тип данных не соответствует символу '{variable_prefix}' во второй строке."

        return "Семантический анализ: Ok"

    except FileNotFoundError:
        return f"[Error] Файл {file_path} не найден."
    except Exception as e:
        return f"[Error] Произошла ошибка: {e}"
