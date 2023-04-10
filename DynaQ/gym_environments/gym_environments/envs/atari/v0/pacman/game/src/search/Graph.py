

class Graph:
    def __init__(self):
        self.nodes = dict()
        self.arcs = set()

    def add_node(self, info):
        if not hasattr(info, '__hash__'):
            raise TypeError("Argument must be hashable")
        
        if info not in self.nodes:
            self.nodes[info] = set()
        
    def add_arc(self, src, tgt):
        if (src, tgt) in self.arcs:
            return
        
        if (tgt, src) in self.arcs:
            return
        
        # Ensure that both nodes are in the graph
        self.add_node(src)
        self.add_node(tgt)

        arc = (src, tgt)

        self.arcs.add(arc)

        # Add arc to the adjacent arcs of both nodes
        self.nodes[src].add(arc)
        self.nodes[tgt].add(arc)

    def get_connected_node(self, node, arc):
        s, t = arc
        return s if node == t else t
