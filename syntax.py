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
                if line.startswith('#') and line.endswith('#'):
                    # Корректный комментарий, игнорируем
                    continue
                elif '#' in line:
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

        return "Синтаксический анализ ОК"

    except FileNotFoundError:
        return f"[Error] Файл {file_path} не найден."
    except Exception as e:
        return f"[Error] Произошла ошибка: {e}"
