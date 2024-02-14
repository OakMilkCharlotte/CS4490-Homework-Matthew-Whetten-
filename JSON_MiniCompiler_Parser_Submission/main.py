from Lexer import *
from Parser import *


class Compiler:
    # Members
    file_input = ""
    token_output = []

    # Methods
    def __init__(self):
        pass

    def compile(self):
        # Get JSON input from user so we can compile it
        self.file_input = input("Enter JSON file contents:\n")

        # Lex the input and store it as a list in token_output
        lexer = Lexer(self.file_input)
        self.token_output = lexer.lex()

        # Print the result of lexing
        for element in self.token_output:
            print(element)
        print()

        # Parse the JSON file
        parser = Parser(self.token_output)
        parser.parse()


def main():
    compiler = Compiler()
    compiler.compile()


if __name__ == '__main__':
    main()


# Test String:
# true false null {"key": "value"} {"key1": 12, "key2": [1, 2]} [11.3, -35, 0.002, 34e12, 3E21, -3.4E2] 44 23 "string"