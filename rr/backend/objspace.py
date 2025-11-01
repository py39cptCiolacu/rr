from rr.compiler.datatypes import W_IntObject, W_FloatObject, w_False, w_True, w_Null
from rpython.rlib.objectmodel import specialize, enforceargs

class VersionTag(object):
    pass

class NamesMap(object):
    def __init__(self, initdict={}):
        self.methods = initdict
        self.version = VersionTag()
    
class ObjectSpace(object):
    w_Null = w_Null
    #w_True = w_True
    #w_False = w_False

    def __ini__(self, global_functions):
        self.functions = NamesMap(global_functions.copy())
        self.constants = NamesMap()
    
    @specialize.argtype(1)
    def wrap(self, value):
        if isinstance(value, bool):
            return newbool(value)


def _new_binop(name):
    def func(self, left, right):
        if isinstance(left, W_IntObject):
            if isinstance(right, W_IntObject):
                return getattr(left, name)(right)
            left = W_FloatObject(left.float())
        else:
            if isinstance(right, W_IntObject):
                right = W_FloatObject(right.float())
        return getattr(left, name)(right)
    func.func_name = name
    return func

binary_operations = ["add", "sub", "mul", "div"]
for _name in binary_operations:
    if not hasattr(ObjectSpace, _name):
        setattr(ObjectSpace, _name, _new_binop(_name))

@enforceargs(bool)
def newbool(val):
    if val:
        return w_True
    return w_False
