from rr.compiler.datatypes import W_Reference

class Frame(object):
    def __init__(self, interpreter, bytecode):

        self.valuestack_pos = 0
        self.valuestack = [None] * 32
        self.vars = [None] * (1+bytecode.symbol_size())
        # self.vars = [None] * 10
        self.bytecode = bytecode
        #self.names = []

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

    def pop_n(self, n):
        if n < 1:
            return []

        res = []
        i = n
        while i > 0:
            i -= 1
            element = self.pop()
            res = [element] + res
        
        return res

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
    
    def store_name(self, name, index):
        pass

    def store_variable(self, name, index, value):
        old_value = self._load(index)
        
        if not isinstance(old_value, W_Reference):
            self._store(index, value)
        else:
            old_value.put_value(value)
        self._store(index, value)

    def get_variable(self, index):
        value = self._load(index)

        if value is None:
            return None

        if not isinstance(value, W_Reference):
           return value
        
        return value.get_value()
