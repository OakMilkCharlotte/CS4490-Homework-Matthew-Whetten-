from Lexer import *


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

        # Create the Lexer
        lexer = Lexer(self.file_input)

        # Lex the input and store it as a list in token_output
        self.token_output = lexer.lex()

        # Print the result
        for element in self.token_output:
            print(element)


def main():
    compiler = Compiler()
    compiler.compile()


if __name__ == '__main__':
    main()


# Test String:
# true false null {"this is a string"}[1, 553, 6.122, .55, 0.2^3, 4^32]:  """"long \tstring\n\"""" nullify tru fals nul