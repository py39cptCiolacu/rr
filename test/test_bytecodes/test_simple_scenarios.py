from rr.frontend.sourceparser import source_to_ast
from rr.compiler.bytecode import compile_ast

def get_opcodes(source):
    ast = source_to_ast(source)

    bytecode = compile_ast(ast, ast.scope, "test.R")       
    opcodes = [opcode.str() for opcode in bytecode.opcodes]

    return opcodes

def test_assign_x():
    program = "x<-1"
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "ASSIGN 0, x",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes


def test_add():
    program = "x<-1+1"
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 0", 
                        "ADD", 
                        "ASSIGN 0, x",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_sub():
    program = "x<-1-1"
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 0", 
                        "SUB", 
                        "ASSIGN 0, x",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_mult():
    program = "x<-1*1"
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 0", 
                        "MUL", 
                        "ASSIGN 0, x",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_div():
    program = "x<-1/1"
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 0", 
                        "DIV", 
                        "ASSIGN 0, x",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if():
    program = "if (TRUE) {x <- 1}"
    expected_opcodes = ["LOAD_BOOLEAN True", 
                        "JUMP_IF_FALSE 5",
                        "LOAD_CONSTANT 0",
                        "ASSIGN 0, x",
                        "JUMP 6",
                        "LOAD_NULL",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes