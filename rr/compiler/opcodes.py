from rr.compiler.datatypes import compare_eq 

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
        pass

    #def __str__(self):
    #    return self.str()
    
class DISCARD_TOP(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        frame.pop()

class PRINT(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        item = frame.top()
        interpreter.output(item.str())

#class LOAD_NULL:...

class RETURN(Opcode):
    _stack_change = 1

    def eval(self, interpreter, bytecode, frame, space):
        return frame.pop()

class LOAD_VAR(Opcode):
    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, space):
        variable = frame.get_variable(self.index)

        if variable is None:
            raise Exception("Variable %s is not set" % self.name)

        frame.push(variable)

    def str(self):
        return "LOAD_VAR %d %s" % (self.index, self.name)

class LOAD_NULL(Opcode):
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(space.w_Null)
    
    def str(self):
        return "LOAD_NULL"

class LOAD_CONSTANT(Opcode):
    _stack_change = 1

    def __init__(self, index):
        self.index = index
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(bytecode._constants[self.index])

    def str(self):
        return "LOAD_CONSTANTS %d" % (self.index)

class LOAD_VECTOR(Opcode):
    def __init__(self, lenght):
        self.length = lenght
        self._stack_change = (-1 * self.length) + 1  # what?    
    
    def eval(self, interpreter, bytecode, frame, space):
        list_w = frame.pop_n(self.length)
        frame.push(space.wrap(list_w))
    
class BaseJump(Opcode):
    def __init__(self, where):
        self.where = where

    def eval(self, interpreter, bytecode, frame, space):
        pass

class JUMP_IF_FALSE(BaseJump):
    def do_jump(self, frame, pos):
        value = frame.pop()
        if not value.is_true():
            return self.where
        return pos + 1

    def str(self):
        return "JUMP_IF_FALSE %d" % (self.where)

class JUMP(BaseJump):

    # can I make this func without frame and pos??
    def do_jump(self, frame, pos):
        return self.where

    def str(self):
        return "JUMP %d" % (self.where)

class ASSIGN(Opcode):

    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, space):
        value = frame.pop()
        frame.store_variable(self.name, self.index, value)

        frame.push(value)

class LABEL(Opcode):

    def __init__(self, num):
        self.num = num

    def str(self):
        return "LABEL %d" % (self.num)

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
        raise NotImplementedError

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
        if name not in ["LOAD_CONSTANT", "ASSIGN", "LOAD_VAR", "JUMP_IF_FALSE", "JUMP", "LABEL", "PRINT", "LOAD_VECTOR"]:
            OpcodeMap[name] = value

opcodes = Opcodes()
for name, value in OpcodeMap.items():
    setattr(opcodes, name, value)

