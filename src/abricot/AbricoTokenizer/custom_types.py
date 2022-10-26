## Custom Types for code understanding ##


## Parsing options

class ParsingOptions():

    def __init__(self, fromLine : int, fromColumn : int, toLine : int, toColumn : int):
        self.fromLine : int = fromLine
        self.fromColumn : int = fromColumn
        self.toLine : int = toLine
        self.toColumn : int = toColumn

    def getOptions(self):
        return self.__dict__


## Token Object ##
class TokenObject():

    def __init__(self, column : int = 0, file : str = '', line : int = 1, name : str = '', raw : str = '', type : str = 'identifier', value : str = '', cur_column : int = 0):

        self.column = column
        self.file = file
        self.line = line
        self.name = name
        self.raw = raw
        self.type = type
        self.value = value
        self.cur_column = cur_column

    def getTokenValue(self):
        return self.__dict__


class PCPPToken():

    def __init__(self, value : str, lineno : int, lexpos : int, type : str, source : str):
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos
        self.type = type
        self.source = source

## Token List ##
class TokenSequence(list):
    
    def __init__(self, iterable):
        super().__init__(item for item in iterable)

    def __setitem__(self, index : int, item : TokenObject):
        super().__setitem__(index, item)

    def insert(self, index : int, item : TokenObject):
        super().insert(index, item)

    def append(self, item : TokenObject):
        super().append(item)

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            raise TypeError('Bad type use in insert')

    def __len__(self):
        return super().__len__()

    

    