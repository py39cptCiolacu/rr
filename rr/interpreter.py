from rr.frame import Frame
from rr.opcodes import RETURN, BaseJump
from rr.objspace import ObjectSpace

class Interpreter(object):
    def __init__(self):
        self.space = ObjectSpace()
        self.output_buffer = []
        self.superglobals = []

    def run(self, bytecode):
        frame = Frame(self, bytecode)
        self.execute(bytecode, frame)
        #if result:
        #    print result.intval
        while len(self.output_buffer) > 0:
            buffer = self.end_buffer()
            self.output(buffer)

    def execute(self, bytecode, frame):
        from rr.bytecode import ByteCode
        assert isinstance(bytecode, ByteCode)


        if bytecode._opcode_count() == 0:
            return None 

        pc = 0
        while True:
            if pc >= bytecode._opcode_count():    
                return None

            opcode = bytecode._get_opcode(pc)
            
            if isinstance(opcode, RETURN):
                return frame.pop()
            
            opcode.eval(self, bytecode, frame, self.space)

            if isinstance(opcode, BaseJump):
                new_pc = opcode.do_jump(frame, pc)
                pc = new_pc
                continue
            else:
                pc += 1
