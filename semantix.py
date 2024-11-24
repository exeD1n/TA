import re

# Регулярные выражения для типов данных
int_regex = r"^-?\d+$"  # Целое число
float_regex = r"^-?\d+\.\d+$"  # Вещественное число
boolean_regex = r"^(true|false)$"  # Булевое значение

def check_semantics(file_path):
    try:
        # Открытие файла для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Удаление пустых строк и комментариев
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

        if not lines:
            return "[Error] Файл пустой или содержит только комментарии."

        # Проверка на наличие строки "program var" в начале
        if lines[0] != "program var":
            return "[Error] Программа должна начинаться с 'program var'."

        # Тип данных, указанный во второй строке
        if len(lines) < 2:
            return "[Error] Отсутствует вторая строка с типом переменных."
        
        variable_declaration = lines[1]
        declared_type = None
        if variable_declaration.startswith('%'):
            declared_type = "int"
        elif variable_declaration.startswith('!'):
            declared_type = "float"
        elif variable_declaration.startswith('$'):
            declared_type = "boolean"
        else:
            return "[Error] Вторая строка должна начинаться с %, ! или $."

        # Типы данных, найденные в файле
        used_types = set()

        # Проверяем содержимое программы
        for line in lines[2:]:
            # Игнорируем строки с комментариями (они уже удалены)
            # Извлекаем все возможные токены (числа, значения true/false)
            tokens = re.findall(r'\b(true|false|-?\d+\.\d+|-?\d+)\b', line, re.IGNORECASE)
            for token in tokens:
                if re.match(int_regex, token):
                    used_types.add("int")
                elif re.match(float_regex, token):
                    used_types.add("float")
                elif re.match(boolean_regex, token, re.IGNORECASE):
                    used_types.add("boolean")

        # Проверка на использование одного типа данных
        if len(used_types) > 1:
            return f"[Error] В программе используются разные типы данных: {', '.join(used_types)}."
        
        # Проверка соответствия использованного типа данных объявленному
        if declared_type not in used_types:
            return f"[Error] Заявленный тип данных '{declared_type}' не соответствует используемому: {', '.join(used_types)}."

        return "Семантический анализ: OK"

    except FileNotFoundError:
        return f"[Error] Файл {file_path} не найден."
    except Exception as e:
        return f"[Error] Произошла ошибка: {e}"
