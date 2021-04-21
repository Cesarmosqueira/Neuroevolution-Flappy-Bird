from sys import argv
from brains import Brain
import matplotlib.pyplot as plt
import threading as th
from process import create_process


def fitness(game_mat, turn, brain):

    return


num_disks = 3  # int(argv[1])

player = Brain(num_disks)
player.generate_decision()
threads = []
for i in range(10):
    threads.append(th.Thread(target=create_process,
                             args=[i, player, num_disks]))
    threads[-1].start()
for t in threads:
    t.join()

print("Al threads terminated")
