from rpython.rlib.rarithmetic import ovfcheck
from rpython.rlib.objectmodel import specialize, instantiate

class W_Root(object):
    pass

class W_Null(W_Root):
    def str(self):
        return "null"

    def get_value(self):
        return self

w_Null = W_Null()

class W_Number(W_Root):
    pass

class W_IntObject(W_Number):
    def __init__(self, intval):
        self.intval = intval
    
    def to_number(self):
        return float(self.intval)

    def get_int(self):
        return self.intval

    def float(self):
        return float(self.intval)

    def add(self, other):
        assert isinstance(other, W_IntObject)
        x = self.intval
        y = other.intval
        try:
            z = ovfcheck(x + y)
        except OverflowError:
            # check behaviour in R-source
            return W_FloatObject(float(x) + float(y))
        return W_IntObject(z)

    def sub(self, other):
        assert isinstance(other, W_IntObject)
        x = self.intval
        y = other.intval
        try:
            z = ovfcheck(x - y)
        except OverflowError:
            # check behaviour in R-source
            return W_FloatObject(float(x) - float(y))
        return W_IntObject(z)

    def mul(self, other):
        assert isinstance(other, W_IntObject)
        x = self.intval
        y = other.intval
        try:
            z = ovfcheck(x * y)
        except OverflowError:
            # check behaviour in R-source
            return W_FloatObject(float(x) * float(y))
        return W_IntObject(z)
    
    def div(self, other):
        # check again
        assert isinstance(other, W_IntObject)
        x = self.intval
        y = other.intval
        try:
            z = ovfcheck(x // y)
        except OverflowError:
            # check behaviour in R-source
            return W_FloatObject(float(x) / float(y))
        return W_IntObject(z)

class W_FloatObject(W_Number):
    def __init__(self, floatval):
        self.floatval = floatval

class W_Reference(W_Root):
    def __init__(self, value):
        self.value = value

    # here is an intentional error to trick the compiler
    # should be return self.value, but self.value can be None, so there is an inconsistency of return between get_value from W_Reference and W_Root
    # W_Root is returning self which is always not None
    # and if a function is calling get_value to a W_Root type of object, we get inconsistency in return 
    def get_value(self):
        return self

class W_Boolean(W_Root):
    def __init__(self, boolval):
        self.boolval = boolval

    def str(self):
        if self.boolval is True:
            return "true"
        return "false"

    def __deepcopy__(self):
        obj = instantiate(self.__class__)
        obj.boolval = self.boolval
        return obj

    def is_true(self):
        return self.boolval

w_True = W_Boolean(True)
w_False = W_Boolean(False)

def isint(w):
    return isinstance(w, W_IntObject)

def isnumber(w):
    return isinstance(w, W_Number)

@specialize.argtype(0, 1)
def _compare_eq(x, y):
    return x == y

def _base_compare(x, y, _compare):
    if isint(x) and isint(y):
        return _compare(x.get_int(), y.get_int())

    if isnumber(x) and isnumber(y):
        n1 = x.to_number()
        n2 = y.to_number()
        return _compare(n1, n2)
    
    #string comparison - comm rn because dont needed. 
    #return is not comm to trick the Rpython compiler
    s1 = x.str()
    s2 = y.str()
    return _compare(s1, s2)
    

def compare_eq(x, y):
    return _base_compare(y, x, _compare_eq)

