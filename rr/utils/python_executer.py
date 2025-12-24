def python_executer(some_code, variables):
    test = ""
    for s in some_code.get_string():
        test +=s
        if s == "x":
            test += "x"

    return test

def modify_code(code, variables):
    # assuming all neded variables comes in order ? HOW??
    # assuming we have a also a list on variables IN ORDER needed for this 
    
    test = ""
    for s in code.stringval:
        test += s
        if s == "x":
            test += "x"

    needed_variables_in_order = ["x"]
    new_line_of_code = needed_variables_in_order[0] + "=" + "%d \n" % variables[0].intval
    x = test + new_line_of_code
    
    return x