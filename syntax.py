import re

def check_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        
        # Фильтрация комментариев
        comment_regex = r"^#.*#$"
        cleaned_lines = []
        for line in lines:
            if '#' in line and not re.match(comment_regex, line):
                return f"[Error] Некорректный комментарий: {line}"
            if not re.match(comment_regex, line):
                cleaned_lines.append(line)
        
        check_document(cleaned_lines)
        return "Синтаксический анализ ОК"
    except FileNotFoundError:
        return f"[Error] Файл {file_path} не найден."
    except Exception as e:
        return f"[Error] {e}"

def check_document(lines):
    """Проверяет структуру всего документа."""
    # Проверка первой строки
    if not lines or lines[0].lower() != "program var":
        raise SyntaxError("Первая строка должна быть 'program var'.")
    
    # Проверка второй строки
    if len(lines) < 2 or not lines[1].startswith(('%', '!', '$')):
        raise SyntaxError("Вторая строка должна быть '%', '!' или '$' и содержать переменные.")
    if len(lines[1].split(',')) < 2:
        raise SyntaxError("На второй строке должны быть объявлены хотя бы одна переменная.")
    
    # Проверка третьей строки
    if len(lines) < 3 or lines[2].lower() != "begin":
        raise SyntaxError("Третья строка должна быть 'begin'.")
    
    # Проверка последней строки
    if lines[-1].lower() != "end.":
        raise SyntaxError("Последняя строка должна быть 'end.'.")
    
    # Проверка содержимого между begin и end
    body_lines = lines[3:-1]
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        if line.lower() == "do while":
            i = check_do_while(body_lines, i)  # Возвращаем новый индекс после проверки do while
        elif line.lower() == "if":
            i = check_if_else(body_lines, i)  # Возвращаем новый индекс после проверки if-else
        elif line.lower() == "for":
            i = check_for_loop(body_lines, i)
        else:
            check_operator(line)
            i += 1

def check_operator(line):
    """Проверяет оператор: присваивание, input, output, do while или if-else."""
    assignment_regex = r'^(let\s+)?[a-zA-Z_]\w*\s*=\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false)(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false))*\s*;?$'
    input_regex = r'^input\s*\(\s*[a-zA-Z_]\w*(\s+[a-zA-Z_]\w*)*\s*\)\s*;?$'
    output_regex = r'^output\s*\(\s*([a-zA-Z_]\w*(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*[a-zA-Z_]\w*)*(\s+[a-zA-Z_]\w*)*)\s*\)\s*;?$'

    
    if re.match(assignment_regex, line):
        return  # Присваивание корректно
    elif re.match(input_regex, line):
        return  # Ввод корректен
    elif re.match(output_regex, line):
        return  # Вывод корректен
    else:
        raise SyntaxError(f"Некорректный оператор: {line}")

def check_do_while(lines, i):
    """Проверяет синтаксис блока `do while` с вложенными операторами."""
    do_while_start_regex = r'^do\s+while$'
    expression_regex = r'^([a-zA-Z_]\w*|\d+(\.\d+)?|true|false)(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false))*$'
    loop_regex = r"^loop\s*;?$"

    # Проверка начала блока `do while`
    if not re.match(do_while_start_regex, lines[i].strip(), re.IGNORECASE):
        raise SyntaxError(f"Ожидается 'do while', но найдено: {lines[i]}")

    if i + 1 >= len(lines):
        raise SyntaxError("Неполный блок 'do while': отсутствует выражение.")

    # Проверка выражения после `do while`
    expression_line = lines[i + 1].strip()
    if not re.match(expression_regex, expression_line, re.IGNORECASE):
        raise SyntaxError(f"Некорректное выражение в 'do while': {expression_line}")

    # Проверка вложенных операторов
    i += 2  # Переход к первому оператору внутри `do while`
    while i < len(lines) and not re.match(loop_regex, lines[i].strip(), re.IGNORECASE):
        line = lines[i].strip().lower()
        if line.startswith("if"):
            i = check_if_else(lines, i)
        elif line.startswith("do while"):
            i = check_do_while(lines, i)
        else:
            check_operator(lines[i])
            i += 1

    # Проверка наличия `loop`
    if i >= len(lines) or not re.match(loop_regex, lines[i].strip(), re.IGNORECASE):
        raise SyntaxError(f"Отсутствует корректный 'loop' в блоке 'do while' на строке {i}.")

    return i + 1  # Возвращаем индекс после завершения блока 'do while'


def process_nested_blocks(lines, i):
    """Обрабатывает тело блока do while, построчно проверяя вложенные конструкции и операторы."""
    while i < len(lines):
        line = lines[i].strip().lower()

        if line == "do while":
            # Встречаем вложенный блок do while
            i = check_do_while(lines, i)
        elif line == "if":
            # Встречаем вложенный блок if-else
            i = check_if_else(lines, i)
        elif line == "for":
            # Встречаем вложенный блок for
            i = check_for_loop(lines, i)
        elif line == 'do while':
            i = check_do_while(lines, i)
        elif line == "loop":
            # Завершаем цикл
            break
        else:
            # Проверка оператора
            try:
                check_operator(line)
                i += 1
            except SyntaxError as e:
                raise SyntaxError(f"Некорректный оператор: {line}")

    return i  # Возвращаем индекс после завершения обработки тела

def check_if_else(lines, i):
    """Проверка синтаксиса блока if-else с вложенными конструкциями и множественными else."""
    if_regex = r'^if$'
    expression_regex = r'^([a-zA-Z_]\w*|\d+(\.\d+)?|true|false)(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false))*$'
    then_regex = r'^then$'
    else_regex = r'^else$'
    end_else_regex = r'^end_else\s*;?$'

    # Проверка начала блока if
    if not re.match(if_regex, lines[i].strip(), re.IGNORECASE):
        raise SyntaxError(f"Ожидается 'if', но найдено: {lines[i]}")

    # Проверка выражения после if
    if i + 1 >= len(lines):
        raise SyntaxError("Отсутствует выражение после 'if'.")
    expression_line = lines[i + 1].strip()
    if not re.match(expression_regex, expression_line, re.IGNORECASE):
        raise SyntaxError(f"Некорректное выражение в 'if': {expression_line}")

    # Проверка 'then'
    if i + 2 >= len(lines):
        raise SyntaxError("Отсутствует 'then' после выражения.")
    then_line = lines[i + 2].strip()
    if not re.match(then_regex, then_line, re.IGNORECASE):
        raise SyntaxError(f"Ожидается 'then', но найдено: {then_line}")

    # Переход к оператору после 'then'
    i += 3
    if i >= len(lines):
        raise SyntaxError("Отсутствует оператор после 'then'.")

    # Проверка оператора после 'then'
    if lines[i].strip().lower() == "if":
        i = check_if_else(lines, i)
    elif lines[i].strip().lower() == "do while":
        i = check_do_while(lines, i)
    elif lines[i].strip().lower() == "for":
        i = check_for_loop(lines, i)
    else:
        check_operator(lines[i].strip())
        i += 1

    # Проверка блоков 'else' (если они есть)
    while i < len(lines) and re.match(else_regex, lines[i].strip(), re.IGNORECASE):
        i += 1  # Переход к оператору после 'else'
        if i >= len(lines):
            raise SyntaxError("Отсутствует оператор после 'else'.")

        if lines[i].strip().lower() == "if":
            i = check_if_else(lines, i)
        elif lines[i].strip().lower() == "do while":
            i = check_do_while(lines, i)
        elif lines[i].strip().lower() == "for":
            i = check_for_loop(lines, i)
        else:
            check_operator(lines[i].strip())
            i += 1

    # Проверка 'end_else' только в конце блока if
    if i >= len(lines) or not re.match(end_else_regex, lines[i].strip(), re.IGNORECASE):
        raise SyntaxError(f"Отсутствует 'end_else' или оно некорректно в блоке 'if'.")

    return i + 1  # Возвращаем индекс после завершения блока 'if-else'


def check_for_loop(lines, i):
    """
    Проверяет синтаксис фиксированного цикла 'for' с поддержкой вложенных конструкций и пустых выражений.
    
    <фиксированного_цикла>::= for «(» [<выражение>] ; [<выражение>] ; [<выражение>] «)» <оператор>
    """
    # Проверка на наличие ключевого слова 'for'
    if not lines[i].strip().lower().startswith("for"):
        raise SyntaxError(f"Ожидается 'for', но найдено: {lines[i]}")

    # Проверка строки с выражениями внутри круглых скобок
    expression_line = lines[i + 1].strip()
    if not expression_line.startswith("(") or not expression_line.endswith(")"):
        raise SyntaxError(f"Ожидаются круглые скобки с выражениями после 'for': {expression_line}")

    # Убираем скобки и разделяем выражения по ';'
    expression_content = expression_line[1:-1].strip()
    expressions = expression_content.split(";")
    if len(expressions) != 3:
        raise SyntaxError(f"Ожидается три выражения, разделенных ';' в цикле 'for': {expression_line}")

    # Проверка каждого выражения (они могут быть пустыми)
    for idx, expr in enumerate(expressions):
        expr = expr.strip()
        if expr:  # Проверяем только непустые выражения
            # Используем регулярное выражение для проверки корректности выражений
            # Это выражение поддерживает арифметические операции, операторы сравнения и присваивания
            if not re.match(r'^\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false)(\s*(\+|-|\*|\/|or|and|not|<>|=|<|<=|>|>=)\s*([a-zA-Z_]\w*|\d+(\.\d+)?|true|false))*$', expr):
                raise SyntaxError(f"Некорректное выражение {idx + 1} в 'for': {expr}")

    # Проверка тела цикла (следующая строка после `for (...)`)
    body_line = lines[i + 2].strip()
    if body_line.lower() == "do while":
        i = check_do_while(lines, i + 2)
    elif body_line.lower() == "for":
        i = check_for_loop(lines, i + 2)
    elif body_line.lower() == "if":
        i = check_if_else(lines, i + 2) - 1
    else:
        try:
            check_operator(body_line)  # Проверка простого оператора
        except SyntaxError:
            raise SyntaxError(f"Некорректный оператор в теле 'for': {body_line}")

    # Проверка на необязательный символ ; в конце тела цикла
    if body_line.endswith(";"):
        body_line = body_line[:-1].strip()  # Убираем ; для последующей проверки на пустую строку

    # Возвращаем индекс после завершения обработки цикла
    return i + 1  # Возвращаем индекс после завершения блока 'for'
