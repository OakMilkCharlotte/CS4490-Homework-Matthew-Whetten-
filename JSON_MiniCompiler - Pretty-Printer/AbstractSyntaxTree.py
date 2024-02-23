from ArrayContainer import *
from Value import *
from ObjectContainer import *

class AbstractSyntaxTree:
    # Members
    tokens = []                         # raw token stream, has pairs of tag + value
    next_token = None                   # next token to look at recursively. Decisions based on this
    next_token_index = 0                # I want to know the index of next_token in the list
    root_container = []                 # this is the root list. All JSON values and other containers live inside here
    current_index = []                  # this list keeps track of depth. It knows the current container we're inserting into
    value_set = ["NUMBER", "STRING", "TRUE", "FALSE", "NULL"]           # easy way to check if a token is one of these values

    # Methods
    def __init__(self, tokens):           # constructor
        self.tokens = tokens
        self.next_token = tokens[0]

    def get_index(self):                  # this function returns a python list indexing, like [0][1][7] for example
        return_string = ""                    # ... this is how I get the location of the container to append to
        for element in self.current_index:      # building the string to return
            return_string += "[" + str(element) + "]"
        return return_string

    def addValue(self):                   # calls get_index() and builds a string with it, and uses execute() to append
        tmpValue = Value(self.next_token, len(self.current_index))     # ... the value to the right container
        self.advanceToken()
        exec("self.root_container" + self.get_index() + ".append(tmpValue)")    # appending the token to the right place

    def prettyPrint(self):                 # nicely prints the root_container and everything inside it
        print("\n" + '=' * 30 + "\n\nPretty printer printing:\n")
        for element in self.root_container:
            print(element, end="")

    def advanceToken(self):                # same as "consume". Advances next_token to the next so we can keep reading
        self.next_token_index += 1
        if self.next_token_index < len(self.tokens):
            self.next_token = self.tokens[self.next_token_index]

    def arrayDive(self):                  # dives 1 depth, creates an array and appends that container to the end of the
        tmpContainer = ArrayContainer(len(self.current_index) + 1)       # ... current container
        exec("self.root_container" + self.get_index() + ".append(tmpContainer)")   # appending array
        exec("self.current_index.append(len(self.root_container" + self.get_index() +") - 1)")   # updating current_index
                                                                          # ... so it points to the array we just added
    def objectDive(self):              # dives 1 depth, creates an object container and appends it to the end of the
        tmpContainer = ObjectContainer(len(self.current_index) + 1)                          # ... current container
        exec("self.root_container" + self.get_index() + ".append(tmpContainer)")
        exec("self.current_index.append(len(self.root_container" + self.get_index() + ") - 1)")  # updating current index

    def ascend(self):                 # closing the current container, and moving up 1 level in depth
        self.current_index.pop()

    def build_ast(self):              # main function, it reads tokens and builds them into a tree
        while self.next_token_index < len(self.tokens):
            self.Value()


    # Recursive Non-Terminal functions
        """I re-used these from the Parser. Instead of building the AST inline alongside parsing, I chose to do it 
        separately because the Parser code was getting cumbersome and confusing, with too many data members trying
        to keep track of what was going on. These recursively call each other with the same parse table rules, 
        and instead of checking off the token that's valid, it adds it to the AST"""

    def Value(self):
        if self.next_token[1] in self.value_set:
            self.addValue()
        elif self.next_token[1] == "LCURLY":
            self.Object()
        elif self.next_token[1] == "LSQUARE":
            self.Array()
        else:
            raise Exception()

    def Object(self):
        if self.next_token[1] == "LCURLY":
            self.objectDive()
            self.advanceToken()        #self.match("LCURLY")
            self.First_Pair()
            self.advanceToken()        #self.match("RCURLY")
            self.ascend()

    def First_Pair(self):
        if self.next_token[1] == "STRING":
            self.addValue()
            key_value_pair = self.next_token[0]
            self.advanceToken()       #self.match("COLON")
            self.Value()
            self.Second_Pair()
        elif self.next_token[1] == "RCURLY":
            pass
        else:
            raise Exception()

    def Second_Pair(self):
        if self.next_token[1] == "COMMA":
            self.advanceToken()               #self.match("COMMA")
            self.addValue()
            self.advanceToken()               #self.match("COLON")
            self.Value()
            self.Second_Pair()
        elif self.next_token[1] == "RCURLY":
            pass
        else:
            raise Exception()

    def Array(self):
        if self.next_token[1] == "LSQUARE":
            self.arrayDive()
            self.advanceToken()             #self.match("LSQUARE")
            self.First_Array_Value()
            self.advanceToken()             #self.match("RSQUARE")
            self.ascend()

    def First_Array_Value(self):
        if self.next_token[1] in self.value_set:
            self.Value()
            self.Second_Array_Value()
        elif self.next_token[1] == "LCURLY":
            self.advanceToken()
            self.Object()
            self.Second_Array_Value()
        elif self.next_token[1] == "LSQUARE":
            #self.advanceToken()
            self.Array()
            self.Second_Array_Value()
        elif self.next_token[1] == "RSQUARE":
            pass
        else:
            raise Exception()

    def Second_Array_Value(self):
        if self.next_token[1] == "COMMA":
            self.advanceToken()
            self.Value()
            self.Second_Array_Value()
        elif self.next_token[1] == "RSQUARE":
            pass
        else:
            raise Exception()