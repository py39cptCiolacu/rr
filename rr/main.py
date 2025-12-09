from rpython.rlib.streamio import open_file_as_stream
from rr.frontend.sourceparser import source_to_ast
from rr.compiler.bytecode import compile_ast
from rr.backend.interpreter import Interpreter
from rr.utils.bytecode_printer import print_bytecode
from rpython.rlib.parsing.deterministic import LexerError

def read_file(filename):
    f = open_file_as_stream(filename)
    data = f.readall()
    f.close()

    return data 

def main(argv):
    if len(argv) < 1:
        print "Missing File"
        return -1

    filename = argv[1]
    source = read_file(filename)

    try:
        ast = source_to_ast(source)
    except LexerError:
        raise SyntaxError 
    bytecode = compile_ast(ast, ast.scope, filename)       
    
    if len(argv) > 2 and argv[2] == "--bytecode":
        print("BYTECODE")
        print_bytecode(bytecode)
        print("BYTECODE END")

    interpreter = Interpreter()
    interpreter.run(bytecode)
    
    return 0 

# def ast(source):
#     ast = source_to_ast(source)
#     return ast
