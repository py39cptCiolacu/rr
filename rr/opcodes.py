class Opcode(object):
    _stack_change = 1
    
    def __init__(self):
        pass

    def get_name(self):
        return self.__class__.__name__
    
    def eval(self, intepreter, bytecode, frame, space):

        raise NotImplementedError(self.get_name() + ".eval")
    
    def stack_change(self):
        return self._stack_change
    
    def str(self):
        return self._stack_change
    
    def __str__(self):
        return self.str()
    
#class DISCARD_TOP:...

#class LOAD_NULL:...

class RETURN(Opcode):
    _stack_change = 1

    def eval(self, interpreter, bytecode, frame, space):
        return frame.pop()

class LOAD_CONSTANT(Opcode):
    _stack_change = 1

    def __init__(self, index):
        self.index = index
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(bytecode._constants[self.index])

    def str(self):
        return "LOAD_CONSTANTS %d" % (self.index)

#class LOAD_VAR:...

#class ASSIGN:...

class BaseMathOperation(Opcode):
    _stack_change = -1

class ADD(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.add(left, right))

class SUB(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.sub(left, right))

class MUL(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.mul(left, right))

class DIV(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.div(left, right))

class Opcodes:
    pass

OpcodeMap = {}

for name, value in locals().items():
    if name.upper() == name and type(value) == type(Opcode) and issubclass(value, Opcode):
        OpcodeMap[name] = value

opcodes = Opcodes()
for name, value in OpcodeMap.items():
    setattr(opcodes, name, value)

