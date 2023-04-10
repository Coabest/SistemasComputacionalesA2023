import pygame

from .Graph import Graph
from .Path import Path
from .Queue import Queue
from .Stack import Stack


class PathFinder:
    MODE_TABLE = {
        "DepthFirst": Stack,
        "BreadthFirst": Queue
    }

    def __init__(self, charmap):
        """
        :attr environment: A dict with the environment information: width, height, tile_width, tile_height
        """
        self.graph = Graph()
        self.__build_graph(charmap)

    def __build_graph(self, charmap):
        for i in range(charmap.rows):
            for j in range(charmap.cols):
                if charmap.charmap[i][j] == '#':
                    continue

                c = (i, j)

                if i > 0 and charmap.charmap[i - 1][j] != '#':
                    u = (i - 1, j)
                    self.graph.add_arc(c, u)

                if j > 1 and charmap.charmap[i][j - 1] != '#':
                    l = (i, j - 1)
                    self.graph.add_arc(c, l)
    
    def find_path(self, src, tgt, mode):
        if src not in self.graph.nodes or tgt not in self.graph.nodes:
            return Path()

        if src == tgt:
            return Path()
        
        visited = set()
        parent = dict()
        data_structure = self.MODE_TABLE[mode](len(self.graph.nodes))
        
        data_structure.add(src)
        visited.add(src)
        parent[src] = None

        while (not data_structure.is_empty()):
            p = data_structure.take()

            if p == tgt:
                break

            for arc in self.graph.nodes[p]:
                if arc in visited:
                    continue
                visited.add(arc)

                q = self.graph.get_connected_node(p, arc)

                if q in visited:
                    continue

                visited.add(q)
                parent[q] = p
                data_structure.add(q)
    
        result = Path()
        result.add(tgt)
        pp = parent[tgt]

        while pp is not None:
            result.add(pp)
            pp = parent[pp]

        result.take()
        
        return result

    def find_closest_by_pred(self, src, pred):
        if src not in self.graph.nodes:
            raise RuntimeError(f"Node {src} does not exist")
        visited = set()
        queue = Queue(len(self.graph.nodes))
        queue.add(src)
        visited.add(src)

        while (not queue.is_empty()):
            p = queue.take()

            if pred(*p):
                return p

            for arc in self.graph.nodes[p]:
                if arc in visited:
                    continue
                visited.add(arc)

                q = self.graph.get_connected_node(p, arc)

                if q in visited:
                    continue

                visited.add(q)
                queue.add(q)

        return src

    
    def render(self, surface, tile_size):
        image = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        image.fill((255, 69, 0, 50))
        for i, j in self.graph.nodes:
            x = j * tile_size
            y = i * tile_size
            surface.blit(image, (x, y))

        for (i, j), (k, l) in self.graph.arcs:
            x1 = j * tile_size + tile_size // 2
            y1 = i * tile_size + tile_size // 2
            x2 = l * tile_size + tile_size // 2
            y2 = k * tile_size + tile_size // 2
            pygame.draw.line(surface, (255, 69, 0), (x1, y1), (x2, y2))