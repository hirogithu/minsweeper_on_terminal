import argparse
import random
import copy
import itertools
import time

def main(args):
    def chk():
        if args.n > 99:
            args.n = 99
        if args.bomb_rate >= 1 or args.bomb_rate <= 0:
            args.bomb_rate = 0.5
        return args

    def create_mine_map(init_w, init_h):
        def num_bomb(mine_list, iw, ih):
            num_bomb = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if iw+i < 0 or iw+i >= args.n or ih+j < 0 or ih+j >= args.n:
                        continue
                    elif mine_list[iw+i][ih+j] == "B":
                        num_bomb += 1
            return num_bomb

        mine_list = [["N"] * args.n for i in range(args.n)]
        # add bomb
        n_bomb = int((args.n ** 2) * args.bomb_rate)
        bomb_count = 0
        for bomb_w in range(args.n):
            for bomb_h in range(args.n):
                # bomb設置
                if bomb_count >= n_bomb:
                    break
                if random.randint(0, 100) > 100 * (1 - args.bomb_rate):
                    # 初期入力位置と周辺は除外
                    if bomb_w != init_w and bomb_h != init_h and \
                        bomb_w != init_w - 1 and bomb_h != init_h - 1 and \
                            bomb_w != init_w + 1 and bomb_h != init_h + 1:
                                mine_list[bomb_w][bomb_h] = "B"
                                bomb_count += 1

        # increment around bomb
        for i in range(args.n):
            for j in range(args.n):
                if mine_list[i][j] == "N":
                    mine_list[i][j] = num_bomb(mine_list, i, j)
        return mine_list, bomb_count

    def open_map(mine_list, open_w, open_h, opened_ls):
        if mine_list[open_w][open_h] == "B":
            opened_ls = [[True] * args.n for i in range(args.n)]
            return opened_ls

        opened_ls[open_w][open_h] = True

        if mine_list[open_w][open_h] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if open_w + i < 0 or open_w + i >= args.n or open_h + j < 0 or open_h + j >= args.n:
                        continue
                    elif not opened_ls[open_w + i][open_h + j]:
                        opened_ls = open_map(mine_list, open_w + i, open_h + j, opened_ls)
        return opened_ls

    def plt_mine(mine_list, opened_ls, play_mode=True):
        h = args.n
        mine_list_cp = copy.deepcopy(mine_list)
        print(*["="]*(args.n+2))
        if play_mode:
            for i in range(h):
                for j in range(h):
                    if not opened_ls[i][j]:
                        mine_list_cp[i][j] = "-"
            print("PLOT MAP")
        else:
            print("PLOT MAP (All Opened)")

        print(" ", " ", *list(range(0, args.n)))
        print(*["="]*(args.n + 2))

        for i in range(h):
            print(i, ":", *mine_list_cp[:][i])

    "chk args"
    args = chk()

    "while wait input(w, h)"
    while True:
        try:
            init_w, init_h = map(int, input("input w h ({} ~ {}) >> ".format(0, args.n - 1)).split())        

            if init_w >= 0 and init_w < args.n and init_h >= 0 and init_h < args.n:
                break
            else:
                print("Over" + str(args.n))

        except ValueError:
            print("input 2 numbers. 0 0")

    "create mine"
    opened_ls = [[False] * args.n for i in range(args.n)]
    mine_list, n_bomb = create_mine_map(init_w, init_h)
    opened_ls = open_map(mine_list, init_w, init_h, opened_ls)

    "plot mine"
    plt_mine(mine_list, opened_ls, play_mode=args.debug)

    "while wait input(w, h)"
    init_time = time.time()
    init_opend_num = sum(list(itertools.chain.from_iterable(opened_ls)))

    while True:

        if all(list(itertools.chain.from_iterable(opened_ls))):
            print("!!!!!!!!BOMBED!!!!!!!!")
            break

        elif sum(list(itertools.chain.from_iterable(opened_ls))) == args.n**2 - n_bomb:
            end_time = time.time()
            print("!!!!!!!!CLEARD!!!!!!!!")
            print("YOUR TIME:{:0=3.2f}".format(end_time - init_time))
            print("OPEND:{}".format(args.n**2 - init_opend_num - n_bomb))
            break

        try:
            open_w, open_h = map(int, input("input w h ({} ~ {}) >> ".format(0, args.n - 1)).split())
    
            if open_w >= 0 and open_w < args.n and open_h >= 0 and open_h < args.n:
                "update mine"
                opened_ls = open_map(mine_list, open_w, open_h, opened_ls)

                "plot mine"
                plt_mine(mine_list, opened_ls, play_mode=args.debug)

            else:
                print("Over " + str(args.n))

        except ValueError:
            print("input 2 numbers. 0 0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=8, help="create (n, n) size")
    parser.add_argument("-b", "--bomb_rate", type=float, default=0.1, help="how many bomb in the mine.")
    parser.add_argument("-d", "--debug", action="store_false")
    args = parser.parse_args()
    main(args)

