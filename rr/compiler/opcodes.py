from rr.compiler.datatypes import compare_eq, compare_ge, compare_le, compare_gt, compare_lt, and_, or_, W_CodeFunction

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

    def is_terminator(self):
        return False
    
    def to_where(self):
        return -1

    #def __str__(self):
    #    return self.str()
    
class DISCARD_TOP(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        frame.pop()

    def str(self):
        return "DISCARD TOP"

class PRINT(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        item = frame.top()
        interpreter.output(item.str())
    
    def str(self):
        return "PRINT"

class RETURN(Opcode):
    _stack_change = 1

    def eval(self, interpreter, bytecode, frame, space):
        return frame.pop()
    
    def str(self):
        return "RETURN"

    def is_terminator(self):
        return True

class LOAD_VAR(Opcode):
    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, space):
        import pdb
        pdb.set_trace()
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

class LOAD_BOOLEAN(Opcode):
    def __init__(self, value):
        self.value = value

    def eval(self, interterper, bytecode, frame, space):
        if self.value:
            frame.push(space.w_True)
        else:
            frame.push(space.w_False)
        
    def str(self):
        if self.value:
            return "LOAD_BOOLEAN True"
        else:
            return "LOAD_BOOLEAN False"
    
class LOAD_CONSTANT(Opcode):
    _stack_change = 1

    def __init__(self, index):
        self.index = index
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(bytecode._constants[self.index])

    def str(self):
        return "LOAD_CONSTANT %d" % (self.index)

class LOAD_STRING(Opcode):
    _stack_change = 1

    def __init__(self, index):
        self.index = index
    
    def eval(self, interpreter, bytecode, frame, space):
        frame.push(bytecode._constants[self.index])

    def str(self):
        return "LOAD_STRING %d" % (self.index)

class LOAD_VECTOR(Opcode):
    def __init__(self, lenght):
        self.length = lenght
        self._stack_change = (-1 * self.length) + 1  # what?    
    
    def eval(self, interpreter, bytecode, frame, space):
        list_w = frame.pop_n(self.length)
        frame.push(space.wrap(list_w))
 
class DECLARE_FUNCTION(Opcode):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode

    def eval(self, interpreter, bytecode, frame, space):
        funcobj = W_CodeFunction(self.bytecode)

        if space.get_function(self.name):
            raise Exception("Function %s already declared" % self.name)

        space.declare_function(self.name, funcobj)

    def str(self):
        return "DECLARE_FUNCTION %s" % (self.name)

class CALL_FUNCTION(Opcode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def eval(self, interpreter, bytecode, frame, space):
        import pdb
        pdb.set_trace()
        funcbody = space.functions.methods.get(self.name, None)
    
        ### test
        frame.push(self.arguments[0]) # this should be store_variable
        ####

        if funcbody is None:
            raise ValueError("Function %s is not defined" % self.name)
        res = interpreter.execute(funcbody.bytecode, frame)
        frame.push(res)

    def str(self):
        return "CALL_FUNCTION %s" % (self.name)

class BaseJump(Opcode):
    def __init__(self, where):
        self.where = where

    def eval(self, interpreter, bytecode, frame, space):
        pass

    def is_terminator(self):
        return True


class JUMP_IF_FALSE(BaseJump):
    def do_jump(self, frame, pos):
        value = frame.pop()
        if not value.is_true():
            return self.where
        return pos + 1

    def str(self):
        return "JUMP_IF_FALSE %d" % (self.where)

    def to_where(self):
        return self.where

class JUMP(BaseJump):

    def do_jump(self, frame, pos):
        return self.where

    def str(self):
        return "JUMP %d" % (self.where)

    def to_where(self):
        return self.where

class ASSIGN(Opcode):

    def __init__(self, index, name):
        self.index = index
        self.name = name
    
    def eval(self, interpreter, bytecode, frame, space):
        value = frame.pop()
        frame.store_variable(self.name, self.index, value)

        frame.push(value)

    def str(self):
        return 'ASSIGN %d, %s' % (self.index, self.name)

class LABEL(Opcode):

    def __init__(self, num):
        self.num = num

    def str(self):
        return "LABEL %d" % (self.num)

class PYTHON_CALL(Opcode):

    def eval(self, interpreter, bytecode, frame, space):
        # this eval will be very tricky because might affect the entire values
        # for now - python-calls will be independent of current scope
        code = frame.top()
        interpreter.execute_python(code)

    def str(self):
        return "PYTHON_CALL"

class BaseMathOperation(Opcode):
    _stack_change = -1

class ADD(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.add(left, right))

    def str(self):
        return "ADD"

class SUB(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.sub(left, right))

    def str(self):
        return "SUB"

class MUL(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.mul(left, right))

    def str(self):
        return "MUL"

class DIV(BaseMathOperation):
    def eval(self, interpreter, bytecode, frame, space):
        right = frame.pop()
        left = frame.pop()
        frame.push(space.div(left, right))
    
    def str(self):
        return "DIV"

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

    def str(self):
        return "EQ"

class NEQ(BaseDecision):
    def decision(self, left, right):
        return not compare_eq(left, right)
    
    def str(self):
        return "NEQ"

class GT(BaseDecision):
    def decision(self, left, right):
        return compare_gt(left, right)

    def str(self):
        return "GT"

class GE(BaseDecision):
    def decision(self, left, right):
        return compare_ge(left, right)

    def str(self):
        return "GE"

class LT(BaseDecision):
    def decision(self, left, right):
        return compare_lt(left, right)

    def str(self):
        return "LT"

class LE(BaseDecision):
    def decision(self, left, right):
        return compare_le(left, right)

    def str(self):
        return "LE"
    
class AND(BaseDecision):
    def decision(self, left, right):
        return and_(left, right)
    
    def str(self):
        return "AND"

class OR(BaseDecision):
    def decision(self, left, right):
        return or_(left, right)
    
    def str(self):
        return "OR"

class Opcodes:
    pass

OpcodeMap = {}

for name, value in locals().items():
    if name.upper() == name and type(value) == type(Opcode) and issubclass(value, Opcode):
        if name not in ["LOAD_CONSTANT", "ASSIGN", "LOAD_VAR", "JUMP_IF_FALSE", "JUMP", "LABEL", "PRINT", "LOAD_VECTOR", "LOAD_BOOLEAN",
                        "LOAD_STRING", "PYTHON", "DECLARE_FUNCTION", "CALL_FUNCTION"]:
            OpcodeMap[name] = value

opcodes = Opcodes()
for name, value in OpcodeMap.items():
    setattr(opcodes, name, value)

