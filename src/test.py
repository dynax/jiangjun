# -*- coding: utf-8 -*-

import board
import player
import os
import time

board = board.board()
simu = player.simulator(board, False)

def testBestOff():
	result = []
	grid = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	for simu.red_player.prob_offense in grid:
		for simu.red_player.prob_offense in grid: 
			cur_result = simu.simuMultiGame(num_simus=10, max_step=200, is_save_qipu=False, path_qipu_prefix="../save/simu")
			result.append

start = time.time()
print simu.simuMultiGame(num_simus=10, max_step=1600, is_save_qipu=True, path_qipu_prefix="../save/simu")
print time.time() - start

# _text_board = [
#     #u' 1  2   3   4   5   6   7   8   9',
#     u'9 ┌─┬─┬─┬───┬─┬─┬─┐',
#     u'  │  │  │  │＼│／│　│　│　│',
#     u'8 ├─┼─┼─┼─※─┼─┼─┼─┤',
#     u'  │　│　│　│／│＼│　│　│　│',
#     u'7 ├─┼─┼─┼─┼─┼─┼─┼─┤',
#     u'  │　│　│　│　│　│　│　│　│',
#     u'6 ├─┼─┼─┼─┼─┼─┼─┼─┤',
#     u'  │　│　│　│　│　│　│　│　│',
#     u'5 ├─┴─┴─┴─┴─┴─┴─┴─┤',
#     u'  │　                         　 │',
#     u'4 ├─┬─┬─┬─┬─┬─┬─┬─┤',
#     u'  │　│　│　│　│　│　│　│　│',
#     u'3 ├─┼─┼─┼─┼─┼─┼─┼─┤',
#     u'  │　│　│　│　│　│　│　│　│',
#     u'2 ├─┼─┼─┼─┼─┼─┼─┼─┤',
#     u'  │　│　│　│＼│／│　│　│　│',
#     u'1 ├─┼─┼─┼─※─┼─┼─┼─┤',
#     u'  │　│　│　│／│＼│　│　│　│',
#     u'0 └─┴─┴─┴───┴─┴─┴─┘',
#     u'  0   1   2   3   4   5   6   7   8'
#     #u'  九 八  七  六  五  四  三  二  一'
# ]
