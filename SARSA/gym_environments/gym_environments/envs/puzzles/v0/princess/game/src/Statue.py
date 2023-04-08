from .. import settings

from .Entity import Entity


class Statue(Entity):
    def __init__(self, x, y, game_level, movement_direction):
        super().__init__(
            x,
            y,
            settings.STATUE_WIDTH,
            settings.STATUE_HEIGHT,
            "statues",
            int(movement_direction == "backward"),
            game_level,
            {
                0: self.move_left
                if movement_direction == "forward"
                else self.move_right,
                1: self.move_down if movement_direction == "forward" else self.move_up,
                2: self.move_right
                if movement_direction == "forward"
                else self.move_left,
                3: self.move_up if movement_direction == "forward" else self.move_down,
            },
            "ST",
        )
        self.movement_direction = movement_direction

    def undo_movement(self):
        self.off_set_i *= -1
        self.off_set_j *= -1
        self.move()

    def on_player_movement(self, action):
        self.movement[action]()
