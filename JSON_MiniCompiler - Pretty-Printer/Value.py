class Value:
    # Members
    value = None
    type = ""            # type of value. true, false, null, number, string
    depth = 0            # need to know how deep we are to add appropriate tabs for pretty printing

    # Methods
    def __init__(self, v, d):
        self.value = v[0]
        self.type = v[1]
        self.depth = d

    def __str__(self):
        return "\t" * self.depth + "[" + str(self.value) + ", " + str(self.type) + "]\n"

    def getPair(self, key_or_value):           # this is used if we are the key or value inside an object
        if key_or_value == 0:    # key
            return "\t" * self.depth + "{" + str(self.value) + ": "
        else:
            return str(self.value) + "}\n"

