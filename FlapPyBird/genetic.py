#reinforcement learning (deep?)
#genetic algorithm
#not backpropatagion | supervised learning
from random import choice
from agent import Bird

def get_new_population(birds):
    #get best 2
    best_2 = sorted(birds, key = lambda b: b.fitness)[-2:]
    print("The best two birds are:")
    for b in best_2:
        print(f"Index   = {b.GLOBAL_INDEX}")
        print(f"Fitness = {b.fitness}\n")

    new_pop = []
    for _ in range(len(birds)):
        new_brain = choice(best_2).brain.copy() ##chose a brain from the best genomes
        new_brain.mutate(0.02) ## mutate brain 
        new_bird = Bird(_) ## create a regular bird with random brain
        new_bird.brain = new_brain #replace its brain xd
        new_pop.append(new_bird)
    return new_pop


def pick_parents(old):

    return n



