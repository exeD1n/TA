def parse_program(file_path):
    # Таблица ключевых слов
    KEYWORDS = [
        "program", "var", "begin", "end", "let", "if", "then", "else", "end_else",
        "for", "do", "while", "loop", "input", "output", "%", "!", "$"
    ]

    # Таблица разделителей
    DELIMITERS = {
        "<>", "<", "<=", ">", ">=", "or", "and", "not", "+", "-", "*", "/", ";", ",",
        "(", ")", "{", "}", "=", "#", ".", " "
    }
    
    try:
        # Открытие файла
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

        # Замена ключевых слов на их индексы
        processed_lines = []
        for line in cleaned_lines:
            tokens = line.split()  # Разбиваем строку на токены
            new_line = []
            for token in tokens:
                if token in KEYWORDS:
                    index = KEYWORDS.index(token) + 1  # Номер ключевого слова
                    new_line.append(f"(1,{index})")  # Заменяем ключевое слово
                else:
                    new_line.append(token)  # Оставляем неизменённым
            processed_lines.append(" ".join(new_line))

        # Вывод обработанных строк
        print("--- Обработанная программа ---")
        for line in processed_lines:
            print(line)

    except FileNotFoundError:
        print(f"[Error] Файл {file_path} не найден.")
    except Exception as e:
        print(f"[Error] Произошла ошибка: {e}")


# Пример использования
if __name__ == "__main__":
    file_path = 'gg.m'
    parse_program(file_path)
