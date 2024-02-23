from AbstractSyntaxTree import *

class Parser:
    # Members
    original_token_stream = []
    token_stream = []
    next_token = ""
    next_token_index = 0
    ast = None

    # Constructor
    def __init__(self, tokens):
        # Shave off whitespace, and create a list with just the token labels in it
        for token in tokens:
            if token[1] != "WHITESPACE":
                self.token_stream.append(token[1])
                self.original_token_stream.append((token[0], token[1]))
        self.token_stream.append("$")
        self.next_token = self.token_stream[self.next_token_index]
        self.next_token_pair = self.original_token_stream[0]
        self.ast = AbstractSyntaxTree(self.original_token_stream)

    # Main function, parses input and reports outcome
    def parse(self):
        try:
            self.Start()
            if self.next_token == "$":
                print("Valid JSON value")
                self.ast.build_ast()
                self.ast.prettyPrint()
            else:
                raise Exception()
        except:
            print(f"Invalid JSON value. Token number: {self.next_token_index} Token: {self.token_stream[self.next_token_index]} Token value: {self.original_token_stream[self.next_token_index][0]}")

    def get_next_token(self):
        if self.next_token_index + 1 == len(self.token_stream):
            raise Exception("Attempted to parse out of bounds")
        else:
            self.next_token_index += 1
            return self.token_stream[self.next_token_index]

    def match(self, token_to_match):
        if self.next_token == token_to_match:
            self.next_token = self.get_next_token()
            if self.next_token != "$":
                self.next_token_pair = self.original_token_stream[self.next_token_index]
        else:
            raise Exception()

    # Parse table functions. Each of these functions represents a non-terminal in the grammar
    def Start(self):
        while self.next_token != "$":
            self.Value()

    def Value(self):
        if self.next_token == "STRING":
            self.match("STRING")
        elif self.next_token == "NUMBER":
            self.match("NUMBER")
        elif self.next_token == "TRUE":
            self.match("TRUE")
        elif self.next_token == "FALSE":
            self.match("FALSE")
        elif self.next_token == "NULL":
            self.match("NULL")
        elif self.next_token == "LCURLY":
            self.Object()
        elif self.next_token == "LSQUARE":
            self.Array()
        elif self.next_token == "$":
            pass
        else:
            raise Exception()

    def Object(self):
        if self.next_token == "LCURLY":
            self.match("LCURLY")
            self.First_Pair()
            self.match("RCURLY")

    def First_Pair(self):
        if self.next_token == "STRING":
            self.match("STRING")
            self.match("COLON")
            self.Value()
            self.Second_Pair()
        elif self.next_token == "RCURLY":
            pass
        else:
            raise Exception()

    def Second_Pair(self):
        if self.next_token == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            self.match("COLON")
            self.Value()
            self.Second_Pair()
        elif self.next_token == "RCURLY":
            pass
        else:
            raise Exception()

    def Array(self):
        if self.next_token == "LSQUARE":
            self.match("LSQUARE")
            self.First_Array_Value()
            self.match("RSQUARE")

    def First_Array_Value(self):
        if self.next_token == "STRING":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "NUMBER":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "TRUE":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "FALSE":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "NULL":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "LCURLY":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "LSQUARE":
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "RSQUARE":
            pass
        elif self.next_token == "$":
            pass
        else:
            raise Exception()

    def Second_Array_Value(self):
        if self.next_token == "COMMA":
            self.match("COMMA")
            self.Value()
            self.Second_Array_Value()
        elif self.next_token == "RSQUARE":
            pass
        else:
            raise Exception()
