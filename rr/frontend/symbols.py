## dumb idea: change this to Redis

class Map(object):
    NOT_FOUND = -1

    def __init__(self):
        self.index = self.NOT_FOUND
        self.forward_pointers = {}
        self.back = None
        self.name = None
    
    def __repr__(self):
        return "%(back)s, [%(index)d]:%(name)s" % \
            {"back": repr(self.back), "index": self.index, "name": self.name}
    
    def contains(self, name):
        index = self.lookup(name)
        return self.not_found(index) is False 

    def not_found(self, index):
        # here just to return bool instead of -1
        return index == self.NOT_FOUND
        
    def lookup(self, name):
        node = self._find_node_with_name(name)
        if node is not None:
            return node.index
        return self.NOT_FOUND
    
    def _find_node_with_name(self, name):
        if self.name == name:
            return self
        if self.back is not None:
            return self.back._find_node_with_name(name)
        
    def _key(self):
        return self.name
    
    def len(self):
        return self.index + 1
    
    def add(self, name):
        assert self.lookup(name) == self.NOT_FOUND
        node = self.forward_pointers.get((name), None)
        if node is None:
            node = MapNode(self, name)
            self.forward_pointers[node._key()] = node
        return node
    
class MapRoot(Map):
    def __repr__(self):
        return "[%(index)d]:%(name)s" % {"index": self.index, "name": self.name}
    
class MapNode(Map):
    def __init__(self, back, name):
        Map.__init__(self)
        self.back = back
        self.name = name
        self.index = back.index + 1

ROOT_MAP = MapRoot()

def new_map():
    return ROOT_MAP
