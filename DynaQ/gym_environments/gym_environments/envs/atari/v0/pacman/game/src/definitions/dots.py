
def add_score(pacman):
    pacman.score += 1

DOTS = {
    '.': {
        'radius': 2,
        'on_collide': add_score
    },
    '*': {
        'radius': 8,
        'on_collide': add_score
    }
}
