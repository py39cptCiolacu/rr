from rr.frontend.sourceparser import source_to_ast
from rr.compiler.bytecode import compile_ast

def get_opcodes(source):
    ast = source_to_ast(source)

    bytecode = compile_ast(ast, ast.scope, "test.R")       

    opcodes = []
    for opcode in bytecode.opcodes:
        opcodes.append(opcode.str())
        if opcode.str().startswith("DECLARE_FUNCTION"):
            function_name = opcode.str().split(" ")[1]
            function_opcodes = [function_name]
            for function_opcode in opcode.bytecode.opcodes:
                function_opcodes.append(function_opcode.str())
            opcodes.append(function_opcodes)

    return opcodes