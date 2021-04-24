from itertools import cycle
import sys
sys.path.insert(1, 'include/')
import nn

class Bird:
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
    died_at = 0
    dead = False
    fitnes = 0
    done = False
    groundCrash = 0 #-1 = false 1 = true
    over = False
    #updt
    score = 0

    def __init__(self, ind):
        # score
        # sprite info
        self.index = 0  # in sprite
        self.indexGen = cycle([0, 1, 2, 1])  # sprite cycle
        self.loopIter = 0  # to change index every 5th iteraton
        # position in screen
        self.x = -1
        self.y = -1
        self.playerShmVals = {'val': 0, 'dir': 1}
        self.GLOBAL_INDEX = ind
        self.brain = nn.neural_network(3, 1, 1) ##input = dx, dy, y
        return

    def describe(self):
        f = open("out/gnome.txt", "a")
        info = "Weights [input -> hidden]\n"
        info += str(self.brain.weights_ih.data) + "\n"
        info = "Weights [hidden -> output]\n"
        info += str(self.brain.weights_ho.data) + "\n"
        info += "Biases [Hidden]\n"
        info += str(self.brain.bias_h.data) + "\n"
        info += "Biases [Output]\n"
        info += str(self.brain.bias_o.data) + "\n"
        f.write(info)
        f.close()
    
    def reload(self):
        # player velocity, max velocity, downward accleration, accleration on flap
        self.done = False
        self.groundCrash = 0 #-1 = false 1 = true
        self.over = False
        # player velocity, max velocity, downward accleration, accleration on flap
        self.playerVelY = -9   # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10   # max vel along Y, max descend speed
        self.playerMinVelY = -8   # min vel along Y, max ascend speed
        self.playerAccY = 1#1   # players downward accleration
        self.playerRot = 45   # player's rotation
        self.playerVelRot = 3#3   # angular speed
        self.playerRotThr = 20#20   # rotation threshold
        self.playerFlapAcc = -9   # players speed on flapping
        self.playerFlapped = False  # True when player flaps


        self.died_at = 0
        self.dead = False
        self.fitnes = 0

        #updt
        self.score = 0
        self.Ydifference = 0

    def playerShm(self):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(self.playerShmVals['val']) == 8:
            self.playerShmVals['dir'] *= -1

        if self.playerShmVals['dir'] == 1:
            self.playerShmVals['val'] += 1
        else:
            self.playerShmVals['val'] -= 1

    def flap_flap(self):
        if self.over or self.done: return
        self.playerVelY = self.playerFlapAcc
        self.playerFlapped = True

    def think_move(self, pipe_x, gapY, SCREENWIDTH, SCREENHEIGHT):
        if self.over or self.done or self.y < -100: return
        ##input = dx, dy, y
        dif_x = (pipe_x - self.x) / SCREENWIDTH
        dif_y = (gapY - self.y) / SCREENHEIGHT
        pos_y = self.y / SCREENHEIGHT
        p = self.brain.predict([dif_x, dif_y, pos_y])[0]
        return 0.8 < p

    def display(self):
        print("Variables:")
        print("  playerVelRot ", self.playerVelRot)
        print("  playerVelY ", self.playerVelY)
        print("  playerMaxVelY ", self.playerMaxVelY)
        print("  playerRot ", self.playerRot)
        print("  Acceleration ", self.playerAccY)
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
    
    def process_death(self, spriteH, BASEY, baseShift):
        self.x -= 4 if not self.over else 0
        if self.y + spriteH >= BASEY - 1 and not self.dead:
            self.dead = True
            return

        # player y shift
        if self.y + spriteH < BASEY - 1:
            self.y += min(self.playerVelY, BASEY - self.y - spriteH)

        # player velocity change
        if self.playerVelY < 15:
            self.playerVelY += self.playerAccY

        # rotate only when it's a pipe crash
        if self.groundCrash == -1:
            if self.playerRot > -90:
                self.playerRot -= self.playerVelRot
    
