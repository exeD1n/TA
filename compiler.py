import sys
from lexer import Lexer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            code = file.read()

        lexer = Lexer()
        result = lexer.analyze(code)
        print(result)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
