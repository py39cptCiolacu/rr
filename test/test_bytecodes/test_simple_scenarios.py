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

def test_print():
    program = 'print("hello")'
    expected_opcodes = ["LOAD_STRING 0", 
                        "PRINT", 
                        "RETURN", 
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
    
def test_if_else():
    program = "if (FALSE) {x <- 1} else {x<-2}"
    expected_opcodes = ["LOAD_BOOLEAN False", 
                        "JUMP_IF_FALSE 5",
                        "LOAD_CONSTANT 0",
                        "ASSIGN 0, x",
                        "JUMP 7",
                        "LOAD_CONSTANT 1",
                        "ASSIGN 0, x",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_or():
    program = 'if (FALSE || FALSE) {print("Hello")}'
    expected_opcodes = ["LOAD_BOOLEAN False", 
                        "LOAD_BOOLEAN False",
                        "OR",
                        "JUMP_IF_FALSE 7",
                        "LOAD_STRING 0",
                        "PRINT",
                        "JUMP 8",
                        "LOAD_NULL",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_and():
    program = 'if (FALSE && FALSE) {print("Hello")}'
    expected_opcodes = ["LOAD_BOOLEAN False", 
                        "LOAD_BOOLEAN False",
                        "AND",
                        "JUMP_IF_FALSE 7",
                        "LOAD_STRING 0",
                        "PRINT",
                        "JUMP 8",
                        "LOAD_NULL",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_le():
    program = 'if (1<=2){print("hello")}'
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 1", 
                        "LE", 
                        "JUMP_IF_FALSE 7", 
                        "LOAD_STRING 2", 
                        "PRINT", 
                        "JUMP 8",
                        "LOAD_NULL", 
                        "RETURN", 
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_lt():
    program = 'if (1<2){print("hello")}'
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 1", 
                        "LT", 
                        "JUMP_IF_FALSE 7", 
                        "LOAD_STRING 2", 
                        "PRINT", 
                        "JUMP 8",
                        "LOAD_NULL", 
                        "RETURN", 
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_ge():
    program = 'if (1>=2){print("hello")}'
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 1", 
                        "GE", 
                        "JUMP_IF_FALSE 7", 
                        "LOAD_STRING 2", 
                        "PRINT", 
                        "JUMP 8",
                        "LOAD_NULL", 
                        "RETURN", 
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_if_gt():
    program = 'if (1>2){print("hello")}'
    expected_opcodes = ["LOAD_CONSTANT 0", 
                        "LOAD_CONSTANT 1", 
                        "GT", 
                        "JUMP_IF_FALSE 7", 
                        "LOAD_STRING 2", 
                        "PRINT", 
                        "JUMP 8",
                        "LOAD_NULL", 
                        "RETURN", 
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_while():
    program = 'while(FALSE){print("Hello")}'
    expected_opcodes = ["LOAD_NULL",
                        "LOAD_BOOLEAN False", 
                        "JUMP_IF_FALSE 7",
                        "LOAD_STRING 0",
                        "PRINT",
                        "DISCARD TOP",
                        "JUMP 1",
                        "RETURN"
                        ]
    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_while_or():
    program = 'while(FALSE && TRUE){print("Hello")}'
    expected_opcodes = ["LOAD_NULL",
                        "LOAD_BOOLEAN False", 
                        "LOAD_BOOLEAN True",
                        "AND",
                        "JUMP_IF_FALSE 9",
                        "LOAD_STRING 0",
                        "PRINT",
                        "DISCARD TOP",
                        "JUMP 1",
                        "RETURN"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_while_and():
    program = 'while(FALSE && FALSE){print("Hello")}'
    expected_opcodes = ["LOAD_NULL",
                        "LOAD_BOOLEAN False", 
                        "LOAD_BOOLEAN False",
                        "AND",
                        "JUMP_IF_FALSE 9",
                        "LOAD_STRING 0",
                        "PRINT",
                        "DISCARD TOP",
                        "JUMP 1",
                        "RETURN"
                        ]
    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_while_eq():
    program = 'while(1==2){print("Hello")}'
    expected_opcodes = ["LOAD_NULL",
                        "LOAD_CONSTANT 0",
                        "LOAD_CONSTANT 1",
                        "EQ",
                        "JUMP_IF_FALSE 9",
                        "LOAD_STRING 2",
                        "PRINT",
                        "DISCARD TOP",
                        "JUMP 1",
                        "RETURN"
                        ]
    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_while_ge():
    program = 'while(1>=2){print("Hello")}'
    expected_opcodes = ["LOAD_NULL",
                        "LOAD_CONSTANT 0",
                        "LOAD_CONSTANT 1",
                        "GE",
                        "JUMP_IF_FALSE 9",
                        "LOAD_STRING 2",
                        "PRINT",
                        "DISCARD TOP",
                        "JUMP 1",
                        "RETURN"
                        ]
    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes