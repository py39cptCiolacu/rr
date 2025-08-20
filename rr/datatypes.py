from rpython.rlib.rarithmetic import ovfcheck

class W_Root(object):
    pass

class W_Number(W_Root):
    pass

class W_IntObject(W_Number):
    def __init__(self, intval):
        self.intval = intval

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
