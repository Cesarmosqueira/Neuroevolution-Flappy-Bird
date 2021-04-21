from random import choice


class Brain:
    def __init__(self, disks):
        self.disks = disks

    def generate_decision(self):
        # random  (2 times the shortest solution)
        self.moves = []
        towers = [x for x in range(self.disks)]
        for _ in range((2**self.disks)*2):
            pos = towers.copy()
            src = choice(pos)
            pos.remove(src)
            dst = choice(pos)
            self.moves.append([src, dst])
