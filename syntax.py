import re

def check_syntax(file_path):
    try:
        # Открытие файла для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Удаление пустых строк
        lines = [line.strip() for line in lines if line.strip()]

        # Регулярное выражение для проверки корректного комментария
        comment_regex = r"^#.*#$"

        # Фильтр для проверки строк с комментариями
        cleaned_lines = []
        for line in lines:
            if '#' in line:
                # Проверяем строки с символами `#`
                if re.match(comment_regex, line):
                    # Корректный комментарий, игнорируем
                    continue
                else:
                    return f"[Error] Синтаксическая ошибка: некорректный комментарий: {line}"
            # Добавляем только строки, которые не являются комментариями
            cleaned_lines.append(line)

        # Проверка первой строки
        if not cleaned_lines or cleaned_lines[0].lower() != "program var":
            return "[Error] Синтаксическая ошибка: первая строка должна быть 'program var'."

        # Проверка второй строки
        if len(cleaned_lines) < 2 or not cleaned_lines[1].startswith(('%', '!', '$')):
            return "[Error] Синтаксическая ошибка: вторая строка должна начинаться с '%', '!' или '$' и содержать объявление переменных."
        if len(cleaned_lines[1].split(',')) < 2:  # Проверяем, что хотя бы одна переменная объявлена
            return "[Error] Синтаксическая ошибка: на второй строке должны быть объявлены хотя бы одна переменная."

        # Проверка третьей строки
        if len(cleaned_lines) < 3 or cleaned_lines[2].lower() != "begin":
            return "[Error] Синтаксическая ошибка: третья строка должна быть ключевым словом 'begin'."

        # Проверка последней строки
        if cleaned_lines[-1].lower() != "end.":
            return "[Error] Синтаксическая ошибка: последняя строка должна быть 'end.'."

        # Извлекаем строки между `begin` и `end.`
        body_lines = cleaned_lines[3:-1]

        # Регулярные выражения для проверки строк
        assignment_regex = r'^(let\s+)?(?!let\b|input\b|output\b)[a-zA-Z_]\w*\s*=\s*(([a-zA-Z_]\w*|\d+(\.\d+)?|true|false)(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false))*)$'
        input_regex = r'^input\s*\(\s*[a-zA-Z_]\w*(\s+[a-zA-Z_]\w*)*\s*\)$'
        output_regex = r'^output\s*\(\s*([a-zA-Z_]\w*(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*[a-zA-Z_]\w*)*)\s*\)$'
        
        # Проверка строк между `begin` и `end.`
        for line in body_lines:
            if not (re.match(assignment_regex, line) or
                    re.match(input_regex, line) or
                    re.match(output_regex, line)):
                return f"[Error] Синтаксическая ошибка: строка не соответствует допустимым конструкциям: {line}"

        return "Синтаксический анализ ОК"

    except FileNotFoundError:
        return f"[Error] Файл {file_path} не найден."
    except Exception as e:
        return f"[Error] Произошла ошибка: {e}"