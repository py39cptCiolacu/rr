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
