from itertools import cycle


class Brain:
    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY = -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY = 10   # max vel along Y, max descend speed
    playerMinVelY = -8   # min vel along Y, max ascend speed
    playerAccY = 1   # players downward accleration
    playerRot = 45   # player's rotation
    playerVelRot = 3   # angular speed
    playerRotThr = 20   # rotation threshold
    playerFlapAcc = -9   # players speed on flapping
    playerFlapped = False  # True when player flaps

    def __init__(self, ind):
        # score
        self.score = 0
        # sprite info
        self.GLOBAL_INDEX = ind
        self.index = 0  # in sprite
        self.indexGen = cycle([0, 1, 2, 1])  # sprite cycle
        self.loopIter = 0  # to change index every 5th iteraton
        # position in screen
        self.x = -1
        self.y = -1
        self.playerShmVals = {'val': 0, 'dir': 1 if ind % 2 == 0 else -1}
        return

    def reload(self):
        # player velocity, max velocity, downward accleration, accleration on flap
        self.playerVelY = -9   # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10   # max vel along Y, max descend speed
        self.playerMinVelY = -8   # min vel along Y, max ascend speed
        self.playerAccY = 1   # players downward accleration
        self.playerRot = 45   # player's rotation
        self.playerVelRot = 3   # angular speed
        self.playerRotThr = 20   # rotation threshold
        self.playerFlapAcc = -9   # players speed on flapping
        self.playerFlapped = False  # True when player flaps

    def playerShm(self):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(self.playerShmVals['val']) == 8:
            self.playerShmVals['dir'] *= -1

        if self.playerShmVals['dir'] == 1:
            self.playerShmVals['val'] += 1
        else:
            self.playerShmVals['val'] -= 1

    def flap_flap(self):
        self.playerVelY = self.playerFlapAcc
        self.playerFlapped = True

    def process_movement(self, spriteH, BASEY):
        # rotate the player
        if self.playerRot > -90:
            self.playerRot -= self.playerVelRot

        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
            # more rotation to cover the threshold (calculated in visiself.e rotation)
            self.playerRot = 45

        self.y += min(self.playerVelY, BASEY - self.y - spriteH)
