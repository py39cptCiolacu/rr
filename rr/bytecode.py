from rr.opcodes import opcodes, RETURN

class ByteCode(object):
    def __init__(self, name, symbols, variables, constants):
        self.name = name
        self._symbols = symbols
        self._symbol_size = symbols.len()
        self._variables = variables
        self._constants = constants

        self.opcodes = []

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
            #if isinstance(op, LABEL):
            #    labels[op.num] = counter
            #else:
            counter += 1

        # self.opcodes = [o for o in self.opcodes if not isinstance(o, LABEL)]
        #for op in self.opcodes:
        #    if isinstance(op, BaseJump):
        #        op.where = labels[op.where]

    def emit(self, bc, *args):
        opcode = getattr(opcodes, bc)(*args)
        self.opcodes.append(opcode)
        return opcode

    def _opcode_count(self):
        return len(self.compiled_opcodes)

    def _get_opcode(self, pc):
        assert pc >= 0 
        return self.compiled_opcodes[pc]

    def symbol_size(self):
        return self._symbol_size


def compile_ast(ast, scope, name):
    bc = ByteCode(name, scope.symbols, scope.variables[:], scope.constants[:])
    if ast is not None:
        ast.compile(bc)
    bc.compile()
    return bc
