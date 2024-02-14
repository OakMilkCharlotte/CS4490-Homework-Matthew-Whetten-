class DFAMatcher:
    # Members
    num_DFAs = 0
    current_DFA_matches = []
    current_DFA_states = []
    matched_DFAs = []

    # Methods
    def __init__(self, n):      # Constructor
        self.num_DFAs = n
        self.resetDFAs()

    def resetDFAs(self):       # Resets all DFA states and matches so they're ready to match anew
        self.current_DFA_states = ["EMPTY"] * self.num_DFAs
        self.current_DFA_matches = [""] * self.num_DFAs
        self.matched_DFAs = [False] * self.num_DFAs

    def returnLongestMatch(self):      # Returns the longest, valid, highest priority match
        longest_match = []
        longest_match_size = -1
        longest_match_index = -1
        for i in range(len(self.current_DFA_matches)):
            if len(self.current_DFA_matches[i]) > longest_match_size:
                longest_match_size = len(self.current_DFA_matches[i])
                longest_match = self.current_DFA_matches[i]
                longest_match_index = i

        if self.matched_DFAs[longest_match_index]:
            return_tags = ["TRUE", "FALSE", "NULL", "LCURLY", "RCURLY", "LSQUARE", "RSQUARE", "COLON", "COMMA",
                       "WHITESPACE", "NUMBER", "STRING", "STRING"]
            return (longest_match, return_tags[longest_match_index])
        else:
            return (longest_match, "UNKNOWN")


    def stillMatching(self, index):        # DFA helper func, tells the lexer if this DFA is still matching or not
        if self.current_DFA_states[index] == "TRAP":
            return False
        else:
            return True

    # DFAs
    def true_DFA(self, char):      # index 0
        match self.current_DFA_states[0]:
            case "EMPTY":
                if char == 't':
                    self.current_DFA_matches[0] = "t"
                    self.current_DFA_states[0] = "t"
                else:
                    self.current_DFA_states[0] = "TRAP"
            case "t":
                if char == 'r':
                    self.current_DFA_matches[0] = "tr"
                    self.current_DFA_states[0] = "tr"
                else:
                    self.current_DFA_states[0] = "TRAP"
            case "tr":
                if char == 'u':
                    self.current_DFA_matches[0] = "tru"
                    self.current_DFA_states[0] = "tru"
                else:
                    self.current_DFA_states[0] = "TRAP"
            case "tru":
                if char == 'e':
                    self.current_DFA_matches[0] = "true"
                    self.current_DFA_states[0] = "ACCEPT"
                else:
                    self.current_DFA_states[0] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[0] = "TRAP"
                self.matched_DFAs[0] = True
            case "TRAP":
                pass
        return self.stillMatching(0)

    def false_DFA(self, char):      # index 1
        match self.current_DFA_states[1]:
            case "EMPTY":
                if char == 'f':
                    self.current_DFA_matches[1] = "f"
                    self.current_DFA_states[1] = "f"
                else:
                    self.current_DFA_states[1] = "TRAP"
            case "f":
                if char == 'a':
                    self.current_DFA_matches[1] = "fa"
                    self.current_DFA_states[1] = "fa"
                else:
                    self.current_DFA_states[1] = "TRAP"
            case "fa":
                if char == 'l':
                    self.current_DFA_matches[1] = "fal"
                    self.current_DFA_states[1] = "fal"
                else:
                    self.current_DFA_states[1] = "TRAP"
            case "fal":
                if char == 's':
                    self.current_DFA_matches[1] = "fals"
                    self.current_DFA_states[1] = "fals"
                else:
                    self.current_DFA_states[1] = "TRAP"
            case "fals":
                if char == 'e':
                    self.current_DFA_matches[1] = "false"
                    self.current_DFA_states[1] = "ACCEPT"
                else:
                    self.current_DFA_states[1] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[1] = "TRAP"
                self.matched_DFAs[1] = True
            case "TRAP":
                pass
        return self.stillMatching(1)

    def null_DFA(self, char):      # index 2
        match self.current_DFA_states[2]:
            case "EMPTY":
                if char == 'n':
                    self.current_DFA_matches[2] = "n"
                    self.current_DFA_states[2] = "n"
                else:
                    self.current_DFA_states[2] = "TRAP"
            case "n":
                if char == 'u':
                    self.current_DFA_matches[2] = "nu"
                    self.current_DFA_states[2] = "nu"
                else:
                    self.current_DFA_states[2] = "TRAP"
            case "nu":
                if char == 'l':
                    self.current_DFA_matches[2] = "nul"
                    self.current_DFA_states[2] = "nul"
                else:
                    self.current_DFA_states[2] = "TRAP"
            case "nul":
                if char == 'l':
                    self.current_DFA_matches[2] = "null"
                    self.current_DFA_states[2] = "ACCEPT"
                else:
                    self.current_DFA_states[2] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[2] = "TRAP"
                self.matched_DFAs[2] = True
            case "TRAP":
                pass
        return self.stillMatching(2)

    def left_curly_DFA(self, char):      # index 3
        match self.current_DFA_states[3]:
            case "EMPTY":
                if char == '{':
                    self.current_DFA_matches[3] = "{"
                    self.current_DFA_states[3] = "ACCEPT"
                else:
                    self.current_DFA_states[3] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[3] = "TRAP"
                self.matched_DFAs[3] = True
            case "TRAP":
                pass
        return self.stillMatching(3)

    def right_curly_DFA(self, char):      # index 4
        match self.current_DFA_states[4]:
            case "EMPTY":
                if char == '}':
                    self.current_DFA_matches[4] = "}"
                    self.current_DFA_states[4] = "ACCEPT"
                else:
                    self.current_DFA_states[4] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[4] = "TRAP"
                self.matched_DFAs[4] = True
            case "TRAP":
                pass
        return self.stillMatching(4)

    def left_square_DFA(self, char):      # index 5
        match self.current_DFA_states[5]:
            case "EMPTY":
                if char == '[':
                    self.current_DFA_matches[5] = "["
                    self.current_DFA_states[5] = "ACCEPT"
                else:
                    self.current_DFA_states[5] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[5] = "TRAP"
                self.matched_DFAs[5] = True
            case "TRAP":
                pass
        return self.stillMatching(5)

    def right_square_DFA(self, char):      # index 6
        match self.current_DFA_states[6]:
            case "EMPTY":
                if char == ']':
                    self.current_DFA_matches[6] = "]"
                    self.current_DFA_states[6] = "ACCEPT"
                else:
                    self.current_DFA_states[6] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[6] = "TRAP"
                self.matched_DFAs[6] = True
            case "TRAP":
                pass
        return self.stillMatching(6)

    def colon_DFA(self, char):      # index 7
        match self.current_DFA_states[7]:
            case "EMPTY":
                if char == ':':
                    self.current_DFA_matches[7] = ":"
                    self.current_DFA_states[7] = "ACCEPT"
                else:
                    self.current_DFA_states[7] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[7] = "TRAP"
                self.matched_DFAs[7] = True
            case "TRAP":
                pass
        return self.stillMatching(7)

    def comma_DFA(self, char):      # index 8
        match self.current_DFA_states[8]:
            case "EMPTY":
                if char == ',':
                    self.current_DFA_matches[8] = ","
                    self.current_DFA_states[8] = "ACCEPT"
                else:
                    self.current_DFA_states[8] = "TRAP"
            case "ACCEPT":
                self.current_DFA_states[8] = "TRAP"
                self.matched_DFAs[8] = True
            case "TRAP":
                pass
        return self.stillMatching(8)

    def white_space_DFA(self, char):      # index 9
        match self.current_DFA_states[9]:
            case "EMPTY":
                if char == ' ' or ord(char) == 9 or ord(char) == 13 or ord(char) == 10:
                    self.current_DFA_matches[9] += char
                    self.current_DFA_states[9] = "ACCEPT"
                elif ord(char) == 92:
                    self.current_DFA_states[9] = "expecting_escaped_char"
                else:
                    self.current_DFA_states[9] = "TRAP"
            case "expecting_escaped_char":
                if char in ['n', 'r', 't']:
                    self.current_DFA_states[9] = "ACCEPT"
                    match char:
                        case 'n':
                            self.current_DFA_matches[9] += '\n'
                        case 'r':
                            self.current_DFA_matches[9] += '\r'
                        case 't':
                            self.current_DFA_matches[9] += '\t'
                else:
                    self.current_DFA_states[9] = "TRAP"
            case "ACCEPT":
                self.matched_DFAs[9] = True
                if char == ' ' or ord(char) == 9 or ord(char) == 13 or ord(char) == 10:
                    self.current_DFA_matches[9] += char
                elif ord(char) == 92:
                    self.current_DFA_states[9] = "expecting_escaped_char"
                else:
                    self.current_DFA_states[9] = "TRAP"
            case "TRAP":
                pass
        return self.stillMatching(9)

    def number_DFA(self, char):      # index 10
        match self.current_DFA_states[10]:
            case "EMPTY":
                if char == '0':
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "zero"
                    self.matched_DFAs[10] = True
                elif char == '-':
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "negative_expecting_digit"
                elif char.isdigit():
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "digit"
                    self.matched_DFAs[10] = True
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "negative_expecting_digit":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "digit"
                    self.matched_DFAs[10] = True
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "zero":
                if char == '.':
                    self.current_DFA_matches[10] += '.'
                    self.current_DFA_states[10] = "fraction_expecting_digit"
                    self.matched_DFAs[10] = False
                elif char.lower() == 'e':
                    self.current_DFA_matches[10] += 'E'
                    self.current_DFA_states[10] = "expecting_exponent"
                    self.matched_DFAs[10] = False
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "digit":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                elif char.lower() == 'e':
                    self.current_DFA_matches[10] += 'E'
                    self.current_DFA_states[10] = "expecting_exponent"
                    self.matched_DFAs[10] = False
                elif char == '.':
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "fraction_expecting_digit"
                    self.matched_DFAs[10] = False
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "fraction_expecting_digit":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "fraction"
                    self.matched_DFAs[10] = True
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "fraction":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                elif char.lower() == 'e':
                    self.current_DFA_matches[10] += 'E'
                    self.current_DFA_states[10] = "expecting_exponent"
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "expecting_exponent":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                    self.current_DFA_states[10] = "exponent"
                    self.matched_DFAs[10] = True
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "exponent":
                if char.isdigit():
                    self.current_DFA_matches[10] += char
                else:
                    self.current_DFA_states[10] = "TRAP"
            case "TRAP":
                pass
        return self.stillMatching(10)

    def string_DFA(self, char):      # index 11
        match self.current_DFA_states[11]:
            case "EMPTY":
                if char == '"':
                    self.current_DFA_states[11] = "matching_string"
                else:
                    self.current_DFA_states[11] = "TRAP"
            case "matching_string":
                if ord(char) == 92:               # 92 is backslash. escapes aren't allowed in a normal string
                    self.current_DFA_states[11] = "expecting_escaped_char"
                elif ord(char) == 34:
                    self.current_DFA_states[11] = "ACCEPT"
                elif 32 <= ord(char) <= 126:
                    self.current_DFA_matches[11] += char
                else:
                    self.current_DFA_states[11] = "TRAP"
            case "expecting_escaped_char":
                if char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't']:
                    self.current_DFA_states[11] = "matching_string"
                    match char:
                        case '"':
                            self.current_DFA_matches[11] += '"'
                        case '\\':
                            self.current_DFA_matches[11] += '\\'
                        case '/':
                            self.current_DFA_matches[11] += '/'
                        case 'b':
                            self.current_DFA_matches[11] += '\b'
                        case 'n':
                            self.current_DFA_matches[11] += '\n'
                        case 'r':
                            self.current_DFA_matches[11] += '\r'
                        case 't':
                            self.current_DFA_matches[11] += '\t'
            case "ACCEPT":
                self.matched_DFAs[11] = True
                self.current_DFA_states[11] = "TRAP"
            case "TRAP":
                pass
        return self.stillMatching(11)

    def long_string_DFA(self, char):        # index 12
        match self.current_DFA_states[12]:
            case "EMPTY":
                if char == '"':
                    self.current_DFA_states[12] = "single_quote"
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "single_quote":
                if char == '"':
                    self.current_DFA_states[12] = "double_quote"
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "double_quote":
                if char == '"':
                    self.current_DFA_states[12] = "matching_long_string"
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "matching_long_string":
                if char == '"':
                    self.current_DFA_states[12] = "exit_quote1"
                elif ord(char) == 92:
                    self.current_DFA_states[12] = "expecting_escaped_char"
                elif 32 <= ord(char) <= 126:
                    self.current_DFA_matches[12] += char
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "expecting_escaped_char":
                if char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't']:
                    self.current_DFA_states[12] = "matching_long_string"
                    match char:
                        case '"':
                            self.current_DFA_matches[12] += '"'
                        case '\\':
                            self.current_DFA_matches[12] += '\\'
                        case '/':
                            self.current_DFA_matches[12] += '/'
                        case 'b':
                            self.current_DFA_matches[12] += '\b'
                        case 'n':
                            self.current_DFA_matches[12] += '\n'
                        case 'r':
                            self.current_DFA_matches[12] += '\r'
                        case 't':
                            self.current_DFA_matches[12] += '\t'
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "exit_quote1":
                if char == '"':
                    self.current_DFA_states[12] = "exit_quote2"
                elif ord(char) == 92:
                    self.current_DFA_matches[12] += '"'
                    self.current_DFA_states[12] = "expecting_escaped_char"
                elif 32 <= ord(char) <= 126:
                    self.current_DFA_matches[12] += "\"" + char
                    self.current_DFA_states[12] = "matching_long_string"
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "exit_quote2":
                if char == '"':
                    self.current_DFA_states[12] = "ACCEPT"
                elif ord(char) == 92:
                    self.current_DFA_matches[12] += "\"\""
                    self.current_DFA_states[12] = "expecting_escaped_char"
                elif 32 <= ord(char) <= 126:
                    self.current_DFA_matches[12] += "\"\"" + char
                    self.current_DFA_states[12] = "matching_long_string"
                else:
                    self.current_DFA_states[12] = "TRAP"
            case "ACCEPT":
                self.matched_DFAs[12] = True
                self.current_DFA_states[12] = "TRAP"
            case "TRAP":
                pass
        return self.stillMatching(12)
