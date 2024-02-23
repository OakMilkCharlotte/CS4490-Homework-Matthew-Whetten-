class ObjectContainer:
    # Members
    myList = []
    depth = 0

    # Methods
    def __init__(self, d):
        self.depth = d
        self.myList = []

    def __str__(self):
        return_string = "\t" * (self.depth - 1) + "{ObjectContainer}\n"
        i = 0
        for element in self.myList:
            return_string += element.getPair(i % 2)
            i += 1
        return return_string

    def __getitem__(self, key):
        return self.myList[key]

    def __len__(self):
        return len(self.myList)

    def getPair(self, key_or_value):            # this is used if this object is the value inside an object pair
        return self.__str__()[:-1] + "}\n"

    def append(self, value):
        self.myList.append(value)

