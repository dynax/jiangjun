# -*- coding: utf-8 -*-

import board
import player
import os
import time

board = board.board()
simu = player.simulator(board, True)

start = time.time()
print simu.simuMultiGame(num_simus=200, max_step=300, is_save_qipu=True, path_qipu_prefix="../save/simu")
print time.time() - start

# board = board.board("test")
# tree = player.randTreePlayer(board, 0)


# print tree.getStrategy()