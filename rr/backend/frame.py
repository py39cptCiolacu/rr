from rr.compiler.datatypes import W_Reference

class Frame(object):
    def __init__(self, interpreter, bytecode):

        self.valuestack_pos = 0
        self.valuestack = [None] * 1024
        self.vars = [None] * bytecode.symbol_size()

        self.bytecode = bytecode

        #for num, i in enumerate(bytecode.superglobals()):
        #   pass

    def push(self, v):
        pos = self.get_pos()
        len_stack = len(self.valuestack)
        
        assert pos >= 0 and len_stack > pos

        self.valuestack[pos] = v
        self.valuestack_pos = pos + 1

    def pop(self):
        v = self.top()
        pos = self.get_pos() - 1
        assert pos >= 0
        self.valuestack[pos] = None
        self.valuestack_pos = pos
        return v

    def top(self):
        pos = self.get_pos() - 1
        assert pos >= 0
        return self.valuestack[pos]

    def get_pos(self):
        return self.valuestack_pos
    
    def _store(self, index, value):
        assert isinstance(index, int)
        assert index >= 0
        self.vars[index] = value

    def _load(self, index):
        assert isinstance(index, int)
        assert index >= 0
        return self.vars[index]

    def store_variable(self, name, index, value):
        #old_value = self._load(index, value)

        self._store(index, value)

    def get_variable(self, index):
        value = self._load(index)

        if value is None:
            return None

        if not isinstance(value, W_Reference):
           return value
        
        return value.get_value()
