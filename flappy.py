import random
import pygame
from pygame.locals import *
from agent import *
import time
import genetic as gen


FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}
GLOBAL_DRAW = True

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range


SAMPLE_SIZE = 200
def main():
    global SCREEN, FPSCLOCK
    global agents
    agents = [Bird(ind) for ind in range(SAMPLE_SIZE)]
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load(
        'assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load(
        'assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load(
        'assets/sprites/base.png').convert_alpha()

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing' + soundExt)
    gen = 1
    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(
            BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        IMAGES['player'] = []
        for _ in range(SAMPLE_SIZE):
            randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)

            IMAGES['player'].append((
                pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
            ))

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = []
        for b in range(SAMPLE_SIZE):
            HITMASKS['player'].append((
                getHitmask(IMAGES['player'][b][0]),
                getHitmask(IMAGES['player'][b][1]),
                getHitmask(IMAGES['player'][b][2]),
            ))
        print("Gen #", gen)
        agents = mainGame(0)
        gen += 1




def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # INFO ON BRAIN() CONSTRUCTOR
    # index of player to blit on screen
    #playerIndex = 0
    #playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    #loopIter = 0
    # load pos to every brain
    for b in agents:
        b.x = int(SCREENWIDTH * 0.2)
        b.y = int((SCREENHEIGHT - IMAGES['player'][0][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    # playerShmVals = {'val': 0, 'dir': 1} #defined on brain

    ##### VOLUME #####
    smallfont = pygame.font.SysFont('Corbel', 20)
    sound_off = True
    text = smallfont.render(
        'SOUND OFF' if sound_off else "SOUND ON", True, (0, 51, 0))
    button_color_light = (170, 170, 170)
    # dark shade of the button
    button_color_dark = (100, 100, 100)
    button_rectangle = (SCREENWIDTH-(SCREENWIDTH//3.5),
                        0, 200, SCREENHEIGHT//30)
    for s in SOUNDS:
        SOUNDS[s].set_volume(0.0 if sound_off else 0.80)
    autostart = 0
    #while True:
    #    autostart += 1
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            SOUNDS['wing'].play()
            return mainGame(basex)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if button_rectangle[0] <= mouse[0] <= button_rectangle[0]+button_rectangle[2] \
                    and button_rectangle[1] <= mouse[1] <= button_rectangle[1]+button_rectangle[3]:
                sound_off = not sound_off
                for s in SOUNDS:
                    SOUNDS[s].set_volume(0.0 if sound_off else 0.80)
                text = smallfont.render(
                    'SOUND OFF' if sound_off else "SOUND ON", True, (0, 51, 0))

    if 20 < autostart:
            # make first flap sound and return values for mainGame
        SOUNDS['wing'].play()
    # draw background
    if GLOBAL_DRAW: SCREEN.blit(IMAGES['background'], (0, 0))

    # to all the players
    # adjust playery, playerIndex, basex
    # and draw them
    for b in agents:
        if (b.loopIter + 1) % 5 == 0:
            b.index = next(b.indexGen)
        b.loopIter = (b.loopIter + 1) % 30
        b.playerShm()
        # draw sprites
        if GLOBAL_DRAW: SCREEN.blit(IMAGES['player'][b.GLOBAL_INDEX][b.index],(b.x, b.y + b.playerShmVals['val']))

    # move the base and draw it with the message
    basex = -((-basex + 4) % baseShift)
    if GLOBAL_DRAW: SCREEN.blit(IMAGES['message'], (messagex, messagey))
    if GLOBAL_DRAW: SCREEN.blit(IMAGES['base'], (basex, BASEY))

    # draw volume button
    # if mouse is hovered on a button it

    mouse = pygame.mouse.get_pos()

    # VOLUME CONTROL
    # if mouse is hovered on a button it
    # changes to lighter shade
    if button_rectangle[0] <= mouse[0] <= button_rectangle[0]+button_rectangle[2] \
            and button_rectangle[1] <= mouse[1] <= button_rectangle[1]+button_rectangle[3]:
        pygame.draw.rect(SCREEN, button_color_dark, button_rectangle)

    else:
        pygame.draw.rect(SCREEN, button_color_light, button_rectangle)

    # superimposing the text onto our button
    if GLOBAL_DRAW: SCREEN.blit(text, (button_rectangle[:2]))

    if GLOBAL_DRAW:
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(basex):
    global FPS
    global GLOBAL_DRAW
    for s in SOUNDS:
        SOUNDS[s].set_volume(0.0)
    for ind in range(len(agents)):
        agents[ind].reload()
        agents[ind].x = int(SCREENWIDTH * 0.2)
        agents[ind].y = int((SCREENHEIGHT - IMAGES['player'][0][0].get_height()) / 2)

    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    # playerVelY = -9   # player's velocity along Y, default same as playerFlapped
    # playerMaxVelY = 10   # max vel along Y, max descend speed
    # playerMinVelY = -8   # min vel along Y, max ascend speed
    # playerAccY = 1   # players downward accleration
    # playerRot = 45   # player's rotation
    # playerVelRot = 3   # angular speed
    # playerRotThr = 20   # rotation threshold
    # playerFlapAcc = -9   # players speed on flapping
    # playerFlapped = False  # True when player flaps
    OVER = False
    BEGINING = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse is at", pygame.mouse.get_pos())
                avg = 0
                for b in agents:
                    avg += get_next_pipe(lowerPipes, b.x)
                avg /= SAMPLE_SIZE
                print(f"And next pipe on agents is {avg} on average")
                if avg.is_integer():
                    pipe = lowerPipes[get_next_pipe(lowerPipes, b.x)]
                    gapY = pipe['y'] - (PIPEGAPSIZE / 2)
                    xpos = pipe['x']
                    print(f"Pipe pos(x,y) = ({xpos}, {gapY})")


            # jump controlls must be called from each brain
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if agents[0].y > -2 * IMAGES['player'][b.GLOBAL_INDEX][0].get_height():
                    agents[0].flap_flap()
                    SOUNDS['wing'].play()
            if event.type == KEYDOWN and event.key == K_s:
                best_bird = max(agents, key = lambda b: b.score)
                print("Gnome code saved at 'out/'")
                best_bird.describe()
            if event.type == KEYDOWN and event.key == K_j:
                FPS -= 5
                print(f"FPS: {FPS}. default =30")
            if event.type == KEYDOWN and event.key == K_k:
                FPS += 5
                print(f"FPS: {FPS}. default =30")
            if event.type == KEYDOWN and event.key == K_d:
                GLOBAL_DRAW = not GLOBAL_DRAW

        for b in agents:
            if b.done:
                continue
            pipe = lowerPipes[get_next_pipe(lowerPipes, b.x)]
            gapY = pipe['y'] - (PIPEGAPSIZE / 2)
            xpos = pipe['x']
            if b.think_move(xpos, gapY, SCREENWIDTH, SCREENHEIGHT):
                b.flap_flap()
        for b in agents:
            if not b.done: 
                crashTest = checkCrash({'x': b.x, 'y': b.y, 'index': b.index}, upperPipes, lowerPipes, b.GLOBAL_INDEX)
                if crashTest[0]:
                    end = time.time() - BEGINING
                    b.fitness = end #time alive
                    b.done = True
                    pipe = lowerPipes[get_next_pipe(lowerPipes, b.x)]
                    gapY = pipe['y'] - (PIPEGAPSIZE / 2)
                    #xpos = pipe['x']
                    b.died_at = b.y
                    b.fitness -= abs(gapY- b.y)  / SCREENHEIGHT
                    b.groundCrash = 1 if crashTest[1] else -1
        
        # apply for entire sample
        for b in agents:
            # check for score
            playerMidPos = b.x + \
                IMAGES['player'][b.GLOBAL_INDEX][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    b.score += 1
                    SOUNDS['point'].play()

            # playerIndex basex change (basex is before for loop)
            if (b.loopIter + 1) % 3 == 0:
                b.index = next(b.indexGen)
            b.loopIter = (b.loopIter + 1) % 30


            spriteH = IMAGES['player'][b.GLOBAL_INDEX][b.index].get_height()
            if not b.done: b.process_movement(spriteH, BASEY)
            else: 
                b.process_death(spriteH, BASEY, baseShift)
                
        # NO PLAYER HERE
        # UNTIL HERE

        over = all(b.done for b in agents)
        if over:
            total_time = time.time() - BEGINING
            #if GLOBAL_DRAW: SCREEN.blit(IMAGES['base'], (basex, BASEY))
            if GLOBAL_DRAW: SCREEN.blit(IMAGES['background'], (0, 0))
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                if GLOBAL_DRAW: SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                if GLOBAL_DRAW: SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            if GLOBAL_DRAW: SCREEN.blit(IMAGES['base'], (basex, BASEY))

            for b in agents:
                b.over = True
                # Player rotation has a threshold
                visibleRot = b.playerRotThr
                if b.playerRot <= b.playerRotThr:
                    visibleRot = b.playerRot
                if not b.done:
                    playerSurface = pygame.transform.rotate(
                        IMAGES['player'][b.GLOBAL_INDEX][b.index], visibleRot)
                    if GLOBAL_DRAW: SCREEN.blit(playerSurface, (b.x, b.y))
                else:
                    playerSurface = pygame.transform.rotate(
                        IMAGES['player'][b.GLOBAL_INDEX][1], b.playerRot)
                    if GLOBAL_DRAW: SCREEN.blit(playerSurface, (b.x, b.y))
            if GLOBAL_DRAW: SCREEN.blit(IMAGES['gameover'], (50, 180))
            if all(b.dead for b in agents):
                print(f"done after {round(total_time,2)}s aprox")
                return gen.get_new_population(agents)
                #return [Bird(ind, False) for ind in range(SAMPLE_SIZE)]

        else: 
            # move base
            basex = -((-basex + 100) % baseShift)
            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
                
            # draw sprites
            if GLOBAL_DRAW: SCREEN.blit(IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                if GLOBAL_DRAW: SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                if GLOBAL_DRAW: SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            if GLOBAL_DRAW: SCREEN.blit(IMAGES['base'], (basex, BASEY))

            # print score so player overlaps the score
            maxscore = max(agents, key = lambda b: b.score).score
            showScore(maxscore if 0 <= maxscore else 0)
            for b in agents:
                if b.x < -10: continue
                # Player rotation has a threshold
                visibleRot = b.playerRotThr
                if b.playerRot <= b.playerRotThr:
                    visibleRot = b.playerRot
                if not b.done:
                    playerSurface = pygame.transform.rotate(
                        IMAGES['player'][b.GLOBAL_INDEX][b.index], visibleRot)
                    if GLOBAL_DRAW: SCREEN.blit(playerSurface, (b.x, b.y))
                else:
                    playerSurface = pygame.transform.rotate(
                        IMAGES['player'][b.GLOBAL_INDEX][1], b.playerRot)
                    if GLOBAL_DRAW: SCREEN.blit(playerSurface, (b.x, b.y))




        if GLOBAL_DRAW:
            pygame.display.update()
            FPSCLOCK.tick(FPS)


# def playerShm(playerShm):
#    """oscillates the value of playerShm['val'] between 8 and -8"""
#    if abs(playerShm['val']) == 8:
#        playerShm['dir'] *= -1
#
#    if playerShm['dir'] == 1:
#        playerShm['val'] += 1
#    else:
#        playerShm['val'] -= 1

def get_next_pipe(pipes, x):
    for i in range(len(pipes)):
        if x <= pipes[i]['x']: return i
    raise Exception("asdasd")
    return -10
def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipeA
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        if GLOBAL_DRAW: SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes, INDEX):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][INDEX][0].get_width()
    player['h'] = IMAGES['player'][INDEX][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                                 player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][INDEX][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(
                playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(
                playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


if __name__ == '__main__':
    main()
