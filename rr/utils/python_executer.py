def python_executer(some_code):
    same_code = ""

    for c in some_code:
        same_code += c
        if c == "c":
            same_code+= "new"
    
    return same_code