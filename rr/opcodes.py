from rr.datatypes import compare_eq 

class Opcode(object):
    _stack_change = 1
    
    def __init__(self, *args):
        pass

    def get_name(self):
        return self.__class__.__name__
    
    def eval(self, intepreter, bytecode, frame, space):
        raise NotImplementedError(self.get_name() + ".eval")
    
    def stack_change(self):
        return self._stack_change
    
    def str(self):
        return self._stack_change
    
    #def __str__(self):
    #    return self.str()
    
class DISCARD_TOP(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        frame.pop()

#class LOAD_NULL:...

class RETURN(Opcode):
    _stack_change = 1

    def eval(self, interpreter, bytecode, frame, space):
        return frame.pop()

class LOAD_VAR(Opcode):
    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, scope):
        variable = frame.get_variable(self.name, self.index)

        if variable is None:
            raise Exception("Variable %s is not set" % self.name)

        frame.push(variable)

        def str(self):
            return "LOAD_VAR %d %s" % (self.index, self.name)

class LOAD_CONSTANT(Opcode):
    _stack_change = 1

    def __init__(self, index):
        self.index = index
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(bytecode._constants[self.index])

    def str(self):
        return "LOAD_CONSTANTS %d" % (self.index)

#class LOAD_VAR:...

class ASSIGN(Opcode):

    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, space):
        value = frame.pop()
        frame.store_variable(self.name, self.index, value)

        frame.push(value)

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

class BaseDecision(Opcode):
    _stack_change = -1

    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        res = self.decision(left, right)
        frame.push(space.wrap(res))
    
    def decision(self, op1, op2):
        raise NotImplemented

class EQ(BaseDecision):
    def decision(self, left, right):
        return compare_eq(left, right)

class NEQ(BaseDecision):
    def decision(self, left, right):
        return not compare_eq(left, right)

class Opcodes:
    pass

OpcodeMap = {}

for name, value in locals().items():
    if name.upper() == name and type(value) == type(Opcode) and issubclass(value, Opcode):
        if name not in ["LOAD_CONSTANT", "ASSIGN", "LOAD_VAR"]:
            OpcodeMap[name] = value

opcodes = Opcodes()
for name, value in OpcodeMap.items():
    setattr(opcodes, name, value)

