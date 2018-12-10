import board
import player
reload(player)

board = board.board()
simu = player.simulator(board)

print simu.simuMultiGame(num_simus=10000, max_step=200, is_save_qipu=True, path_qipu_prefix="../result/simu")
# simu.simuOneGame(max_step=200, is_save_qipu=True, path_qipu="../result/simu")