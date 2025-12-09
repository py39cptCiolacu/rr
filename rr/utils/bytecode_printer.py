def _edit_bytecode_str(bytecode):
    instructions = []
    
    for opcode in bytecode.opcodes:
        op_str = opcode.str()

        if op_str.startswith("LOAD_CONSTANT"):
            index = int(op_str.split(" ")[-1])
            constant = bytecode._constants[index]
            op_str = "%s (%s)" % (op_str, constant.str())

        instructions.append(op_str)

    return instructions


def compute_block_index(opcodes):
    n = len(opcodes)
    block_of = [0] * n
    jump_targets = [0] * n
    jt_count = 0

    i = 0
    while i < n:
        op = opcodes[i]
        tgt = op.to_where()
        if tgt != -1:
            jump_targets[jt_count] = tgt
            jt_count += 1

        i += 1

    block_id = 0
    i = 0
    while i < n:
        j = 0
        while j < jt_count:
            if jump_targets[j] == i:
                block_id += 1
                break
            j += 1

        block_of[i] = block_id

        op = opcodes[i]
        if op.is_terminator():
            block_id += 1

        i += 1

    return block_of


def print_bytecode(bytecode):
    instructions = _edit_bytecode_str(bytecode)
    block_of = compute_block_index(bytecode.opcodes)

    current_block = -1

    for i, instr in enumerate(instructions):
        block_id = block_of[i]

        if block_id != current_block:
            print "B%d:" % block_id
            current_block = block_id

        print "   %d: %s" % (i, instr)