class Node(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and 
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return self.str()
    
    def str(self):   #might require a unicode return because of py2.7
        #return self.__class__.__name__
        return unicode(self.__class__.__name_)
    
    def _indent(self, block):
        return "\n".join(["\t" + line for line in block])

    def _indent_block(self, block):
        return self._indent(block.str().split("\n"))


class Statement(Node):
    pass

class Expression(Statement):
    pass

class ListOp(Expression):
    def __init__(self, nodes):
        self.nodes = nodes

class Program(Statement):
    def __init__(self, body, scope):
        self.body = body
        self.scope = scope

    def compile(self, ctx):
        self.body.compile(ctx)
    
    def str(self):
        body = self._indent_block(self.body)
        return "Program (\n%s\n)" % body
    
class ListOp(Expression):
    def __init__(self, nodes):
        self.nodes = nodes

class SourceElements(Statement):
    def __init__(self, func_decl, nodes):
        self.func_decl = func_decl
        self.nodes = nodes
    
    def compile(self, ctx):
        for _ , funccode in self.func_decl.items():
            funccode.compile(ctx)
        
        if len(self.nodes) > 1:
            for node in self.nodes[:-1]:
                node.compile(ctx)

                if not isinstance(node, Return):
                    ctx.emit("DISCARD_TOP")
        
        if len(self.nodes) > 0:
            node = self.nodes[-1]
            node.compile(ctx)
        else:
            ctx.emit("LOAD_NULL")
        
        if self.nodes and not isinstance(self.nodes[-1], Return):
            ctx.emit("RETURN")
    
    def str(self):
        string = []
        for node in self.func_decl.values():
            for line in node.str().split("\n"):
                string.append(line)
        for node in self.nodes:
            for line in node.str().split("\n"):
                string.append(line)
        body = self._indent(string)
        return "SourceElements (\n%s\n)" % body        

class Global(ListOp):
    def __init__(self, nodes):
        self.nodes = nodes

class ConstantInt(Node):
    def __init__(self, intval, index):
        self.intval = intval
        self.index = index
    
    def compile(self, ctx):
        ctx.emit("LOAD_CONSTANT", index=self.index)
    
    def str(self):
        return "ConstantInt %d" % self.intval
    
class VariableIdentifier(Expression):
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def get_literal(self):
        return self.identifier
    
    def compile(self, ctx):
        ctx.emit("LOAD_VAR", self.index, self.identifier)
    
    def str(self):
        return "VaribleIdentifier (%d, %s)" % (self.index, self.identifier)

class Return(Statement):
    pass

def create_binary_op(name):
    #possible error point ! 
    class BinaryOP(Expression):
        def __init__(self, left, right):
            self.left = left
            self.right = right
        
        def compile(self, ctx):
            self.left.compile(ctx)
            self.right.compile(ctx)
            ctx.emit(name)
        
        def str(self):
            return name + "(%s, %s)" % (self.left.str(), self.right.str())
    
    BinaryOP.__name__ = name
    return BinaryOP

Plus = create_binary_op('ADD')
Sub = create_binary_op('SUB')
Mult = create_binary_op('MUL')
Division = create_binary_op('DIV')

class BaseAssignment(Expression):
    
    def compile(self, ctx):
    
        self.right.compile(ctx)
        self.compile_store(ctx)

class AssignmentOperation(BaseAssignment):
    def __init__(self, left, right, operand):
        self.left = left
        self.index = left.index
        self.right = right
        self.operand = operand
    
    def compile_store(self, ctx):
        ctx.emit("ASSIGN", self.index, self.left.get_literal())
    
    def str(self):
        return "AssignOperation (%s, %s, %s)" % (self.left.str(), self.operand, self.right.str())
