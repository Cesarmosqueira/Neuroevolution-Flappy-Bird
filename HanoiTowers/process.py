
def pretty_paint_towers(mat, nd):
    return
    for i in range(nd):
        i = nd - i - 1
        if i < len(mat[0]):
            print(f"{ {mat[0][i]} }", end="\t")
        else:
            print("{ }", end="\t")

        if i < len(mat[1]):
            print(f"{ {mat[1][i]} }", end="\t")
        else:
            print("{ }", end="\t")

        if i < len(mat[2]):
            print(f"{ {mat[2][i]} }", end="\t")
        else:
            print("{ }", end="\t")
        print("\n \t \t ")
    print("")
    return


def finish_game(mat, ds, index):
    if len(mat[-1]) != ds:
        return False
    else:
        print(f"[+] {index} won")
        pretty_paint_towers(mat, ds)
        return True


def valid_move(game_mat, src, dst, maxvalue):
    if src < 0 or 3 <= src or dst < 0 or 3 <= dst:
        return
    if len(game_mat[src]) == 0:
        return False
    dstval = maxvalue if len(game_mat[dst]) == 0 else game_mat[dst][-1]
    srcval = game_mat[src][-1]
    if srcval < dstval:
        return True
    return False


def move(game_mat, src, dst):
    game_mat[dst].append(game_mat[src][-1])
    game_mat[src].pop()


def create_process(index, brain, num_disks):
    turn = 0
    res = False
    mat = [[num_disks-i for i in range(num_disks)], [], []]
    src, dst = -1, -1
    ilegal = False
    while finish_game(mat, num_disks, index) == False:
        turn += 1
        if not ilegal:
            pretty_paint_towers(mat, num_disks)
        # src, dst = [int(x) for x in input("src, dst: ").split()] #FOR USER INPUT
        if turn == len(brain.moves):

            # FITNESS FUNCTION TO BRAINS  (min_required - (Closeness to win - ilegal moves))
            # MUTATE BRAINSSSS ///////////////////////////// NO IDEA XD

            break
        src, dst = brain.moves[turn-1]
        if valid_move(mat, src, dst, num_disks+10):
            ilegal = False
            move(mat, src, dst)
        else:
            ilegal = True

        print(f"[+] Process {index} succeded with move {turn}")
    return res
