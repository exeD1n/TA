import re

class Lexer:
    def __init__(self):
        # Ключевые слова, разделители и допустимые символы
        self.keywords = {
            "program", "var", "begin", "end", "let", "if", "then", "else", "end_else",
            "for", "do", "while", "loop", "input", "output", "%", "!", "$"
        }
        self.delimiters = {
            "<>", "<", "<=", ">", ">=", "or", "and", "not", "+", "-", "*", "/",
            ";", ",", "}", "{", "(", ")", " ", ".", "=",
        }
        self.comment_start = "#"
        self.comment_end = "#|"

        # Регулярные выражения для лексем
        self.patterns = {
            "identifier": r"^[A-Za-z][A-Za-z0-9]*$",  # Идентификаторы
            "integer": r"^[+-]?\d+$",  # Целые числа (допускаются знаки + и -)
            "real": r"^[+-]?\d+\.\d+([eE][+-]?\d+)?$",  # Действительные числа
            "logical_constant": r"^(true|false)$",  # Логические константы
        }

    def tokenize(self, code):
        """
        Лексический анализ: проверка программы на лексические ошибки.
        """
        errors = []
        tokens = []

        # Удаление комментариев
        code = self.remove_comments(code)

        # Разбиение кода на токены с учётом пробелов и разделителей
        words = re.split(r"(\s+|[<>=;,+*/{}().-])", code)
        words = [word.strip() for word in words if word.strip()]

        for word in words:
            if word in self.keywords:  # Ключевое слово
                tokens.append(f"KEYWORD({word})")
            elif word in self.delimiters:  # Разделитель
                tokens.append(f"DELIMITER({word})")
            elif re.fullmatch(self.patterns["identifier"], word):  # Идентификатор
                tokens.append(f"IDENTIFIER({word})")
            elif re.fullmatch(self.patterns["integer"], word):  # Целое число
                tokens.append(f"INTEGER({word})")
            elif re.fullmatch(self.patterns["real"], word):  # Действительное число
                tokens.append(f"REAL({word})")
            elif re.fullmatch(self.patterns["logical_constant"], word):  # Логическая константа
                tokens.append(f"BOOLEAN({word})")
            else:  # Неизвестная лексема
                errors.append(f"Неизвестная лексема: '{word}'")

        return tokens, errors

    def remove_comments(self, code):
        """
        Удаляет комментарии из кода.
        """
        return re.sub(rf"{self.comment_start}.*?{self.comment_end}", "", code, flags=re.DOTALL)

    def analyze(self, code):
        tokens, errors = self.tokenize(code)

        if errors:
            return "Лексическая проверка: NON"
        return "Лексическая проверка: OK"
