from rr.compiler.datatypes import W_IntObject, W_NumericObject
from rr.frontend.symbols import new_map

class Scope(object):
    def __init__(self):
        self.symbols = new_map() 
        self.variables = []
        self.constants = []
        self.constants_ints = {}
        self.constants_numeric = {}

    def add_symbol(self, name):
        # HINT: This might be a bery good point to check for Python calls from 

        index = self.symbols.lookup(name)

        if index == self.symbols.NOT_FOUND:
            self.symbols = self.symbols.add(name)
            index = self.symbols.lookup(name)
        
        assert isinstance(index, int)
        return index

    def add_int_constant(self, value): 
        try:
            return self.constants_ints[value]
        except KeyError:
            a = len(self.constants)
            self.constants.append(W_IntObject(value))
            self.constants_ints[value] = a
            return a
        
    def add_numeric_constant(self, value): 
        try:
            return self.constants_numeric[value]
        except KeyError:
            a = len(self.constants)
            self.constants.append(W_NumericObject(value))
            self.constants_numeric[value] = a
            return a
    
    def add_variable(self, name):
        index = self.add_symbol(name)

        if name not in self.variables:
            self.variables.append(name)

        # TODO: SUPERGLOBAL might be needed (if R supprt smth like this)

        return index