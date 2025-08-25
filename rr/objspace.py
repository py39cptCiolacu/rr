from rr.datatypes import W_IntObject, W_FloatObject

class VersionTag(object):
    pass

class NamesMap(object):
    def __init__(self, initdict={}):
        self.methods = initdict
        self.version = VersionTag()
    
class ObjectSpace(object):
    def __ini__(self, global_functions):
        self.functions = NamesMap(global_functions.copy())
        self.constants = NamesMap()

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
