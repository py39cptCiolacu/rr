from rr.utils.utils import get_opcodes

EXPECTED_OPCODES_AFTER_OPERATION = [
        "ASSIGN 2, z",
        "RETURN",
    ]

def generate_expected_opcodes_same_length(operation):
    EXPECTED_OPCODES_BEFORE_OPERATION = [
        "LOAD_CONSTANT 0",
        "LOAD_CONSTANT 1",
        "LOAD_CONSTANT 2",
        "LOAD VECTOR",
        "ASSIGN 0, x",
        "DISCARD TOP",
        "LOAD_CONSTANT 0",
        "LOAD_CONSTANT 1",
        "LOAD_CONSTANT 2",
        "LOAD VECTOR",
        "ASSIGN 1, y",
        "DISCARD TOP",
        "LOAD_VAR 0 x",
        "LOAD_VAR 1 y",
    ]

    return EXPECTED_OPCODES_BEFORE_OPERATION + [operation] + EXPECTED_OPCODES_AFTER_OPERATION

def generate_expected_opcodes_diff_length(operation):
    EXPECTED_OPCODES_BEFORE_OPERATION = [
        "LOAD_CONSTANT 0",
        "LOAD_CONSTANT 1",
        "LOAD_CONSTANT 2",
        "LOAD_CONSTANT 3",
        "LOAD VECTOR",
        "ASSIGN 0, x",
        "DISCARD TOP",
        "LOAD_CONSTANT 0",
        "LOAD_CONSTANT 1",
        "LOAD_CONSTANT 2",
        "LOAD VECTOR",
        "ASSIGN 1, y",
        "DISCARD TOP",
        "LOAD_VAR 0 x",
        "LOAD_VAR 1 y",
    ]

    return EXPECTED_OPCODES_BEFORE_OPERATION + [operation] + EXPECTED_OPCODES_AFTER_OPERATION

def test_add_vector_same_length():
    program = "x<-c(1, 2, 3) y<-c(1, 2, 3) z<-x+y"
    expected_opcodes = generate_expected_opcodes_same_length("ADD")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_add_vector_diff_length():
    program = "x<-c(1, 2, 3, 4) y<-c(1, 2, 3) z<-x+y"
    expected_opcodes = generate_expected_opcodes_diff_length("ADD")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_sub_vector_same_length():
    program = "x<-c(1, 2, 3) y<-c(1, 2, 3) z<-x-y"
    expected_opcodes = generate_expected_opcodes_same_length("SUB")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_sub_vector_diff_length():
    program = "x<-c(1, 2, 3, 4) y<-c(1, 2, 3) z<-x-y"
    expected_opcodes = generate_expected_opcodes_diff_length("SUB")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_mul_vector_same_length():
    program = "x<-c(1, 2, 3) y<-c(1, 2, 3) z<-x*y"
    expected_opcodes = generate_expected_opcodes_same_length("MUL")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_mul_vector_diff_length():
    program = "x<-c(1, 2, 3, 4) y<-c(1, 2, 3) z<-x*y"
    expected_opcodes = generate_expected_opcodes_diff_length("MUL")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_div_vector_same_length():
    program = "x<-c(1, 2, 3) y<-c(1, 2, 3) z<-x/y"
    expected_opcodes = generate_expected_opcodes_same_length("DIV")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes

def test_div_vector_diff_length():
    program = "x<-c(1, 2, 3, 4) y<-c(1, 2, 3) z<-x/y"
    expected_opcodes = generate_expected_opcodes_diff_length("DIV")

    opcodes = get_opcodes(program)
    assert expected_opcodes == opcodes