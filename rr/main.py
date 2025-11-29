from rpython.rlib.streamio import open_file_as_stream
from rr.frontend.sourceparser import source_to_ast
from rr.compiler.bytecode import compile_ast
from rr.backend.interpreter import Interpreter

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
    ast = source_to_ast(source)

    bytecode = compile_ast(ast, ast.scope, filename)       

    #### FOR TESTING 
    if len(argv) > 2:
        if argv[2] == "--bytecode":
            print "BYTECODE" 
            for i, o in enumerate(bytecode.opcodes):
                print "%d %s" % (i, o.str()) 
            print "BYTECODE END"
    #### FOR TESTING 
    
    interpreter = Interpreter()
    interpreter.run(bytecode)
    
    return 0 

# def ast(source):
#     ast = source_to_ast(source)
#     return ast
