from .. import settings
from .Dot import Dot
from .Map import Map
from .entity.BaseEntity import Direction
from .entity.Ghost import Ghost
from .entity.Pacman import Pacman
from .search.Pathfinder import PathFinder
from .definitions.dots import DOTS


def distance(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def distance_v(v1, v2):
    return distance(v1.x, v2.x, v1.y, v2.y)


class Scene:
    def __init__(self):
        self.map = None
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.__load_environment()
        self.pathfinder = PathFinder(self.map)
        self.lose = False
  
    def __load_environment(self):
        with open(settings.CHARMAP, "r") as f:
            rows, cols = f.readline().split("x")
            rows, cols = int(rows), int(cols)
            self.map = Map(rows, cols)

            for i in range(rows):
                row = f.readline()
                for j in range(cols):
                    s = row[j]
                    if s in ('.', '*'):
                        x, y = j * settings.TILE_SIZE + settings.TILE_SIZE // 2, i * settings.TILE_SIZE + settings.TILE_SIZE // 2
                        defs = DOTS[s]
                        self.dots.append(Dot(x, y, defs))
                    else:
                        self.map.charmap[i][j] = s
                    

            row, col, speed, interval = f.readline().split(",")
            row, col, speed, interval = int(row), int(col), float(speed), float(interval)
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
            self.pacman = Pacman(x, y, settings.TILE_SIZE, settings.TILE_SIZE, speed, settings.TEXTURES['pacman'], settings.FRAMES['pacman'], interval, self)

            num_ghosts = int(f.readline())

            for _ in range(num_ghosts):
                row, col, color, speed, interval, mode = f.readline().split(",")
                row, col, color, speed, interval = int(row), int(col), int(color), float(speed), float(interval)
                x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE
                if mode[-1] == '\n':
                    mode = mode[:-1]
                self.ghosts.append(
                    Ghost(x, y, settings.TILE_SIZE, settings.TILE_SIZE, speed, settings.TEXTURES['ghosts'], settings.FRAMES['ghosts'][color], interval, self, mode)
                )


    def reset(self):
        self.map = None
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.__load_environment()
        self.pathfinder = PathFinder(self.map)
        return self.get_state()

    def get_state(self):
        dg1 = distance_v(self.pacman.position, self.ghosts[0].position)
        dg2 = distance_v(self.pacman.position, self.ghosts[1].position)
        ip, jp = int(self.pacman.position.y // settings.TILE_SIZE), int(self.pacman.position.x // settings.TILE_SIZE) 
        id, jd = self.pathfinder.find_closest_by_pred((ip, jp), lambda i, j: self.map.charmap[i][j] in ('.', '*'))
        dcd = distance(jp, jd, ip, id) * settings.TILE_SIZE
        max_dist = distance(0, 10, 0, 10) * settings.TILE_SIZE

        pacman_dir = self.pacman.dir_to_num()

        pacman_moving_left = 1 if pacman_dir == Direction.LEFT else 0
        pacman_moving_down = 1 if pacman_dir == Direction.DOWN else 0
        pacman_moving_right = 1 if pacman_dir == Direction.RIGHT else 0
        pacman_moving_up = 1 if pacman_dir == Direction.UP else 0

        return [dg1/max_dist, dg2/max_dist, dcd/max_dist, pacman_moving_left, pacman_moving_down, pacman_moving_right, pacman_moving_up]

    def check_win(self):
        return len(self.dots) == 0
    
    def check_lose(self):
        return self.lose
    
    def apply_action(self, action):
        return self.pacman.apply_action(action)
    
    def update(self, dt):
        self.pacman.update(dt)

        for dot in self.dots:
            if self.pacman.get_collision_rect().colliderect(dot.get_collision_rect()):
                dot.eaten = True
                dot.on_collide(self.pacman)
        
        self.dots = [d for d in self.dots if not d.eaten]

        for ghost in self.ghosts:
            ghost.update(dt)

            if self.pacman.get_collision_rect().colliderect(ghost.get_collision_rect()):
                self.lose = True
    
    def render(self, surface):
        self.map.render(surface)
        for dot in self.dots:
            dot.render(surface)
        self.pacman.render(surface)
        for ghost in self.ghosts:
            ghost.render(surface)

        # To debug
        # self.pathfinder.render(surface, settings.TILE_SIZE)
