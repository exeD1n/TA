def validate_constructions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    in_construction_block = False
    constructions = []
    construction = []

    for line in lines:
        line = line.strip()  # Убираем лишние пробелы

        if line == "begin":
            in_construction_block = True
            continue
        elif line == "end.":
            in_construction_block = False
            if construction:  # Если есть накопленный блок, добавляем его
                constructions.append(' '.join(construction))
            break

        if in_construction_block:
            if line == "":  # Если строка пустая, это конец текущей конструкции
                if construction:
                    constructions.append(' '.join(construction))
                    construction = []
            else:
                construction.append(line)  # Добавляем строку в текущую конструкцию

    # Выводим все конструкции
    print("Все конструкции:")
    for i, con in enumerate(constructions, 1):
        print(f"Конструкция {i}: {con}")

    # Проверка конструкций
    errors = []
    num_constructions = len(constructions)

    for i, con in enumerate(constructions):
        # Если конструкция одна или последняя, не должна заканчиваться на ';'
        if (num_constructions == 1 or i == num_constructions - 1) and con.endswith(';'):
            errors.append(f"Ошибка: Конструкция {i + 1} не должна заканчиваться на ';'.")
        # Если конструкция не последняя, должна заканчиваться на ';'
        elif num_constructions > 1 and i < num_constructions - 1 and not con.endswith(';'):
            errors.append(f"Ошибка: Конструкция {i + 1} должна заканчиваться на ';'.")

    # Если есть ошибки, выводим их
    if errors:
        for error in errors:
            print(error)
    else:
        print("Все конструкции корректны.")

# Пример вызова
validate_constructions('gg.m')
