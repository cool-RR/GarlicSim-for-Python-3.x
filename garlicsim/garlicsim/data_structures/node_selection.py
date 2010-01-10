'''tododoc'''


from garlicsim.misc import GarlicSimException

from node import Node
from node_range import NodeRange

    
class CompletelyCompact(GarlicSimException):
    pass
    
from garlicsim.general_misc import cute_iter_tools

class NodeSelection(object):
    def __init__(self, ranges):
        self.ranges = [ranges] if isinstance(ranges, NodeRange) else \
                      list(ranges)
        
    def compact(self):
        for node_range in self.ranges:
            assert node_range.is_valid()
        
        try:
            while True:
                self.__partially_compact()
        except CompletelyCompact:
            return
            
    def __partially_compact(self):
        first, second = None, None
        for (r1, r2) in cute_iter_tools.orderless_combinations(self.ranges, 2):
            if r1.start in r2:
                second, first = r1, r2
                break
            elif r2.start in r1:
                first, second = r1, r2
                break
            else:
                pass
        if first is not None and second is not None:
            if second.end in first:
                pass
            else: # second.end not in first
                for current in second:
                    if current not in first:
                        break
                if current.parent is first.end:
                    self.ranges.remove(first)
                    new_range = NodeRange(start=first.start, end=second.end)
                else:
                    new_range = NodeRange(start=current, end=second.end)
                self.ranges.append(new_range)
              
            self.ranges.remove(second)
            return
        else:
            raise CompletelyCompact
    
    def __iter__(self):
        for node_range in self.ranges:
            for node in node_range:
                return(node)
    
    def __add__(self, other):
        assert isinstance(other, NodeSelection)
        return NodeSelection(self.ranges + other.ranges)
    
    def __radd__(self, other):
        return self.__add__(other)

    def copy(self):
        return NodeSelection(self.ranges)
    
    
    __copy__ = copy
    
    
    
    
    
    
    