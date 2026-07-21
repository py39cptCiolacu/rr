from rr.utils.utils import get_opcodes

def test_simple_function_no_call():
    program = 'test <- function() {print("Hello")}'
    expected_opcodes = ["DECLARE_FUNCTION test", 
                        [
                           "test",
                           "LOAD_STRING 0",
                           "PRINT"
                        ],
                        "LOAD_NULL"
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_simple_function_call():
    program = 'test <- function() {print("Hello")} test()'
    expected_opcodes = ["DECLARE_FUNCTION test", 
                        [
                           "test",
                           "LOAD_STRING 0",
                           "PRINT"
                        ],
                        "CALL_FUNCTION test",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_function_and_assign_after():
    program = 'test <- function() {print("Hello")} test() x<-1'
    expected_opcodes = ["DECLARE_FUNCTION test", 
                        [
                           "test",
                           "LOAD_STRING 0",
                           "PRINT"
                        ],
                        "CALL_FUNCTION test",
                        "DISCARD TOP",
                        "LOAD_CONSTANT 0",
                        "ASSIGN 1, x",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_function_and_assign_inside_after():
    program = 'test <- function() {print("Hello") x<-1} test()'
    expected_opcodes = ["DECLARE_FUNCTION test", 
                        [  
                           "test",
                           "LOAD_STRING 0",
                           "PRINT",
                           "DISCARD TOP",
                           "LOAD_CONSTANT 1",
                           "ASSIGN 0, x",
                        ],
                        "CALL_FUNCTION test",
                        "RETURN",
                        ]

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes