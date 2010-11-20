
class ReasonedBool(object):

    def __init__(self, value, reason=None):
        self.value = bool(value)
        self.reason = reason
        
        
    def __repr__(self):
        if self.reason is not None:
            return '<%s because %s>' % (self.value, repr(self.reason))
        else: # self.reason is None
            return '<%s with no reason>' % self.value

        
    def __eq__(self, other):
        return bool(self) == other
    
    
    def __neq__(self, other):
        return not self.__eq__(other)

    
    def __bool__(self):
        return self.value
    __nonzero__ = __bool__