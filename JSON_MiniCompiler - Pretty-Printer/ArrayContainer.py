class ArrayContainer:
    # Members
    myList = []
    depth = 0

    # Methods
    def __init__(self, depth):
        self.depth = depth
        self.myList = []

    def __str__(self):
        return_string = "\t" * (self.depth - 1) + "[ArrayContainer]\n"
        for element in self.myList:
            return_string += str(element)
        return return_string

    def __getitem__(self, key):
        return self.myList[key]

    def __len__(self):
        return len(self.myList)

    def append(self, value):
        self.myList.append(value)

    def getPair(self, key_or_value):        # used if this array is the value inside an object pair
        return self.getPairStr() + "}\n"

    def getPairStr(self):          # helper function for getPair()
        return_string = "\t" * (self.depth - 1) + "[ArrayContainer]\n"
        for element in self.myList:
            return_string += str(element)
        return return_string[:-1]
