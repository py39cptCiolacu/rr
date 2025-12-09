from rr.compiler.opcodes import *

class ByteCode(object):
    def __init__(self, name, symbols, variables, constants):
        self.name = name
        self._symbols = symbols
        self._symbol_size = symbols.len()
        self._variables = variables
        self._constants = constants

        self.label_count = 100000
        self.opcodes = []
        self.startlooplabel = []
        self.endlooplabel = []
        self.pop_after_break = []
        self.updatelooplabel = []

    def compile(self):
        self.unlabel()
        compiled_opcodes = []
        prev_o = None

        for o in self.opcodes:
            if isinstance(o, RETURN) and isinstance(prev_o, RETURN):
                 continue

            compiled_opcodes.append(o)
            prev_o = o

        self.compiled_opcodes = compiled_opcodes
        # self.estimated_stack_size() - this is for JIT

    def unlabel(self):
        labels = {}
        counter = 0
        for i in range(len(self.opcodes)):
            op = self.opcodes[i]
            if isinstance(op, LABEL):
               labels[op.num] = counter
            else:
                counter += 1

        self.opcodes = [o for o in self.opcodes if not isinstance(o, LABEL)]
        for op in self.opcodes:
           if isinstance(op, BaseJump):
               op.where = labels[op.where]
    
    # this is a workaround to trick the compiler
    # opcode would look inside opcode which is in obj imported from opcodes.py
    # check for LOAD_CONSTANT should not be done + LOAD_CONSTANT should be part of opcode
    def emit(self, bc, index=-1, name="", num=-1, value=False):
        if bc == "LOAD_CONSTANT":
            opcode = LOAD_CONSTANT(index)
        elif bc == "LOAD_STRING":
            opcode = LOAD_STRING(index)
        elif bc == "ASSIGN":
            opcode = ASSIGN(index, name)
        elif bc == "LOAD_VAR":
            opcode = LOAD_VAR(index, name)
        elif bc == "JUMP_IF_FALSE":
            opcode = JUMP_IF_FALSE(num)
        elif bc == "JUMP":
            opcode = JUMP(num)
        elif bc == "LABEL":
            opcode = LABEL(num)
        elif bc == "PRINT":
            opcode = PRINT()
        elif bc == "PYTHON_CALL":
            opcode = PYTHON_CALL()
        elif bc == "LOAD_VECTOR":
            opcode = LOAD_VECTOR(num)
        elif bc == "LOAD_BOOLEAN":
            opcode = LOAD_BOOLEAN(value)
        else:    
            opcode = OpcodeMap[bc]()
        self.opcodes.append(opcode)
        return opcode

    def _opcode_count(self):
        return len(self.compiled_opcodes)

    def _get_opcode(self, pc):
        assert pc >= 0 
        return self.compiled_opcodes[pc]

    def symbol_size(self):
        return self._symbol_size

    def emit_label(self, num=-1):
        if num == -1:
            num = self.prealocate_label()
            self.emit("LABEL", num=num)
            return num
        
        self.emit("LABEL", num=num)
        return num

    def prealocate_label(self):
        num = self.label_count
        self.label_count += 1
        return num 
    
    def prealocate_endloop_label(self, pop_after_break=False):
        num = self.prealocate_label()
        self.endlooplabel.append(num)
        self.pop_after_break.append(pop_after_break)
        return num
    
    def emit_endloop_label(self, label):
        self.endlooplabel.pop()
        self.startlooplabel.pop()
        self.pop_after_break.pop()
        self.emit_label(label)

    def emit_startloop_label(self):
        num = self.emit_label()
        self.startlooplabel.append(num)
        return num

    def continue_at_label(self, label):
        self.updatelooplabel.append(label)

    def done_continue(self):
        self.updatelooplabel.pop()

def compile_ast(ast, scope, name):
    bc = ByteCode(name, scope.symbols, scope.variables[:], scope.constants[:])
    if ast is not None:
        ast.compile(bc)
    bc.compile()
    return bc
