from garlicsim.general_misc.ordered_set import OrderedSet
from garlicsim_wx.general_misc.emitters import Emitter

class EmittingOrderedSet(OrderedSet):
    def __init__(self, emitter, iterable=()):
        if emitter:
            assert isinstance(emitter, Emitter)
            self.emitter = emitter
        OrderedSet.__init__(self, iterable)
        
    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self.map[key] = [key, curr, end]
            if self.emitter:
                self.emitter.emit()

    def discard(self, key):
        if key in self.map:        
            key, prev, next = self.map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev
            if self.emitter:
                self.emitter.emit()
    
    def set_emitter(self, emitter):
        self.emitter = emitter