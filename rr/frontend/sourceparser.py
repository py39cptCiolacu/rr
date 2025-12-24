import py
from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from rpython.rlib.parsing.tree import RPythonVisitor
from rpython.rlib.parsing.parsing import ParseError
from rpython.rlib.rarithmetic import ovfcheck_float_to_int

from rr import rrdir
from rr.compiler import operations
from rr.backend.scopes import Scope

GRAMMAR_FILE = "frontend/grammar.txt"
grammar = py.path.local(rrdir).join(GRAMMAR_FILE).read("rt")
try:
    regexs, rules, ToAST = parse_ebnf(grammar)
except ParseError as e:
    print e.nice_error_message(filename=GRAMMAR_FILE, source=grammar)
    raise

_parse = make_parse_function(regexs, rules, eof = True)

class NewToAST(ToAST):
    
    def __str__(self):
        return "salut"    

def parse(code):
    t = _parse(code)
    return NewToAST().transform(t)

class Transformer(RPythonVisitor):

    BINOP_TO_CLS = {
        '+': operations.Plus,
        '-': operations.Sub,
        '*': operations.Mult,
        '/': operations.Division,
        '==': operations.Eq,
        '!=': operations.NEq,
        '<': operations.Lt,
        '>': operations.Gt,
        '<=': operations.Le,
        '>=': operations.Ge,
    }

    UNOP_TO_CLS = {
        '!': operations.Not,
    }

    def __init__(self):
        self.funclist = []
        self.scopes = []
        self.depth = - 1

    def visit_main(self, node):
        self.enter_scope()
        body = self.dispatch(node.children[0])
        scope = self.current_scope()
        return operations.Program(body, scope)
    
    def visit_sourceelements(self, node):
        self.funclist.append({})
        nodes = []
        for child in node.children:
            node = self.dispatch(child)
            if node is None:
                continue

            # if isinstance(node, operations.Global):
            #     for node in node.nodes:
            #         self.declare_global(node.get_literal())
            #     continue

            nodes.append(node)
        
        func_decl = self.funclist.pop()
        return operations.SourceElements(func_decl, nodes)

    ##### EXPERIMENTAL
    def visit_pythonexpression(self, node):
        code = self.dispatch(node.children[0])
        variables = self.dispatch(node.children[1])
        return operations.PythonCall(code, variables)
    ##### EXPERIMENTAL

    def visit_block(self, node):
        l = [self.dispatch(child) for child in node.children]
        return operations.Block(l)

    def binaryop(self, node):
        left = self.dispatch(node.children[0])
        for i in range((len(node.children) - 1) // 2):
            op = node.children[i * 2 + 1]
            right = self.dispatch(node.children[i * 2 + 2])
            result = self.BINOP_TO_CLS[op.additional_info](left, right)
            left = result
        return left

    visit_additiveexpression = binaryop
    visit_multiplicativeexpression = binaryop
    visit_equalityexpression = binaryop
    visit_relationalexpression = binaryop

    def visit_assignmentexpression(self, node):
        left = self.dispatch(node.children[0])
        operation = node.children[1].additional_info
        right = self.dispatch(node.children[2])

        return operations.AssignmentOperation(left, right, operation)

    def visit_ifstatement(self, node):
        condition = self.dispatch(node.children[0])
        ifblock = self.dispatch(node.children[1])
        if len(node.children) > 2:
            elseblock = self.dispatch(node.children[2])
        else:
            elseblock = None
        return operations.If(condition, ifblock, elseblock)
    
    def visit_printstatement(self, node):
        return operations.Print(self.dispatch(node.children[0]))
    
    def visit_whilestatement(self, node):
        condition = self.dispatch(node.children[0])
        block = self.dispatch(node.children[1])
        return operations.While(condition, block)

    def visit_vector(self, node):
        l = [self.dispatch(child) for child in node.children[0].children]
        return operations.Vector(l)

    def visit_number(self, node):
        # check type of number (int, float)
        # call declare_constant_<type>
        number = ""
        for node in node.children:
            number += node.additional_info
        try:
            if len(number) > 1:
                if number[-1] == "L" or number[-1] == "l":
                    i = int(number[:-1])
                    index = self.declare_constant_int(i)
                    return operations.ConstantInt(i, index)
            
            f = float(number)
            i = ovfcheck_float_to_int(f)
            if i != f:
                index = self.declare_constant_numeric(f)
                return operations.ConstantNumeric(f, index)
            else:
                i = int(number)
                index = self.declare_constant_int(i)
                return operations.ConstantInt(i, index)
        except (ValueError, OverflowError):
            f = float(node.additional_info)
            index = self.declare_constant_numeric(f)
            return operations.ConstantNumeric(f, index)

    ##### EXPERIMENTAL
    def visit_string(self, node):
        # TODO: make this better
        string_value = node.children[0].additional_info
        index = self.declare_string(string_value)
        return operations.String(string_value, index)
    ##### EXPERIMENTAL
    
    def visit_identifier(self, node):
        name = ""
        for node in node.children:
            name += node.additional_info
        index = self.declare_variable(name)
        return operations.VariableIdentifier(name, index)

    def visit_literal(self, node):
        if node.children[0].symbol == "number":
            return self.visit_number(node.children[0])
        
        if node.children[0].symbol == "identifier":
            return self.visit_identifier(node.children[0])
        
        if node.children[0].symbol == "booleanliteral":
            return self.visit_booleanliteral(node.children[0])

        if node.children[0].symbol == "string":
            return self.visit_string(node.children[0])

    def visit_booleanliteral(self, node):
        value =  node.children[0].additional_info
        if value == "TRUE":
            return operations.Boolean(True)
        elif value == "FALSE":
            return operations.Boolean(False)
        raise ValueError

    def declare_string(self, value):
        #adding the int into the current scope
        index = self.scopes[-1].add_string(value)
        return index
    
    def declare_constant_int(self, value):
        #adding the int into the current scope
        index = self.scopes[-1].add_int_constant(value)
        return index
    
    def declare_constant_numeric(self, value):
        #adding the int into the current scope
        index = self.scopes[-1].add_numeric_constant(value)
        return index
    
    def declare_variable(self, symbol):
        index = self.scopes[-1].add_variable(symbol)
        return index

    def enter_scope(self):
        self.depth = self.depth + 1

        new_scope = Scope()
        self.scopes.append(new_scope)
        
    def current_scope(self):
        try:
            return self.scopes[-1]
        except IndexError:
            return None

def source_to_ast(source):
    try:
        ast = parse(source)
    except ParseError, e:
        print e.nice_error_message(source=source)
        raise
    transformer = Transformer()
    return transformer.dispatch(ast)
    
