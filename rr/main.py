from rpython.rlib.streamio import open_file_as_stream
from rr.sourceparser import source_to_ast
from rr.bytecode import compile_ast
from rr.interpreter import Interpreter

import os

def read_file(filename):
    f = open_file_as_stream(filename)
    data = f.readall()
    f.close()

    return data 

def main(argv):
    if len(argv) < 1:
        raise FileNotFoundError

    filename = argv[1]

    source = read_file(filename)
    ast = source_to_ast(source)

    bytecode = compile_ast(ast, ast.scope, filename)

    interpreter = Interpreter()
    interpreter.run(bytecode)
    
    return 0 

# def ast(source):
#     ast = source_to_ast(source)
#     return ast
