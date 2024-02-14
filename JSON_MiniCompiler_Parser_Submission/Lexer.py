from DFAMatcher import *


class Lexer:
    # Members
    tokens = []                                       # list of matched tokens to be returned. Final output of the lexer
    num_DFAs = 13                                     # num of DFAs written. Helps lists be created and reset to length
    DFA_still_matching = [True] * num_DFAs            # represents which DFAs are still matching
    matcher = DFAMatcher(num_DFAs)                    # DFAMatcher object, will call its methods
    chars_left_to_process = []                        # input. Cnstr puts input string into this list of chars

    # Methods
    def __init__(self, input):           # Constructor
        self.chars_left_to_process = list(input)      # convert string input to a list, so it's easier to work with
        self.chars_left_to_process.append(" ")        # appending this space ensures the final token will match. The way
                                                           # my DFAs work, they don't return a match until they all fail

    def resetDFAs(self):          # resets the lexer's record of which DFAs are matching. Resets all of matcher's DFAs
        self.DFA_still_matching = [True] * self.num_DFAs
        self.matcher.resetDFAs()

    def lex(self):                # main function of this class. It tokenizes input, and returns a list of tokens
        for char in self.chars_left_to_process:
            # Every DFA still matching attempts to match next char
            self.match(char)
        return self.tokens

    """match() is the main logic of this class. It takes a char as input. Then, for every DFA still matching, it 
    attempts to match that char. As long as at least one DFA is still matching, it will continue to pass chars to that
    DFA, ensuring a greedy longest match. Once all DFAs have failed a match, we know that the longest possile match was
    made. We get that from the matcher object and append it to tokens. Because the current char failed to match every
    DFA, we must reset all the DFAs, and attempt to match it again. Essentially, we don't want to consume that char
    without it ever having matched anything. """
    def match(self, char):
        # Call every DFA that is still matching
        for i in range(self.num_DFAs):
            if self.DFA_still_matching[i]:
                self.DFA_still_matching[i] = self.callAppropriateDFA(i, char)

        # Check if every element in DFAStillMatching == False
        still_matching = False
        for element in self.DFA_still_matching:
            if element:  # if True then that DFA is still matching
                still_matching = True

        if not still_matching:  # if still_matching == False
            # Check for unknown token. Longest match will be 0
            longest_match_length = 0
            for element in self.matcher.current_DFA_matches:
                if len(element) > longest_match_length:
                    longest_match_length = len(element)
            # unknown token case
            if longest_match_length == 0:           # if the char is unknown, every DFA will fail and len will be 0
                self.tokens.append((char, "UNKNOWN"))
                self.resetDFAs()  # reset DFAs
            # valid match case
            else:
                # Longest match found, since every DFA failed to match the current char
                self.tokens.append(self.matcher.returnLongestMatch())  # append the matched token to tokens
                self.resetDFAs()       # reset DFAs
                self.match(char)       # call match again so char isn't consumed since it didn't match

    def callAppropriateDFA(self, index, char):        # each DFA is associated with an index. This calls the right one
        match index:
            case 0:
                return self.matcher.true_DFA(char)
            case 1:
                return self.matcher.false_DFA(char)
            case 2:
                return self.matcher.null_DFA(char)
            case 3:
                return self.matcher.left_curly_DFA(char)
            case 4:
                return self.matcher.right_curly_DFA(char)
            case 5:
                return self.matcher.left_square_DFA(char)
            case 6:
                return self.matcher.right_square_DFA(char)
            case 7:
                return self.matcher.colon_DFA(char)
            case 8:
                return self.matcher.comma_DFA(char)
            case 9:
                return self.matcher.white_space_DFA(char)
            case 10:
                return self.matcher.number_DFA(char)
            case 11:
                return self.matcher.string_DFA(char)
            case 12:
                return self.matcher.long_string_DFA(char)
