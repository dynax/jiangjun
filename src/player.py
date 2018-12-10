import random
from time import time, sleep
import os
import numpy as np
import copy

class player:
    def __init__(self, board, is_red=True):
        self.is_red = is_red
        if True == self.is_red:
            self.name_pre = "Red"
        else:
            self.name_pre = "Black"
        self.timer = 0
        self.setBoard(board)

    def getStrategy(self, all_move_encodings):
        best_move = []
        return best_move

    def setBoard(self, board):
        self.board = board

class humanPlayer(player):
    def getStrategy(self):
        while True:
            print "local_id dest_row dest_col\t Move a piece"
            print "draw\t\t\t\t Claim a draw game"
            print "rv\t\t\t\t Revert a move"
            print "stop\t\t\t\t Stop game"
            tmp_input = raw_input()
            if tmp_input in ["draw", "rv", "pnext", "stop"]:
                return tmp_input
            if "showid" == tmp_input:
                try:
                    os.system("clear")
                except:
                    os.system("cls")
                self.board.display(self.board.is_current_red, "name")
                self.board.display(self.board.is_current_red, "id")
                continue
            try:
                segs = tmp_input.split()
                piece_local_id = int(segs[0])
                dest_x = int(segs[1])
                dest_y = int(segs[2])
                assert piece_local_id in range(16)
                if True == self.board.is_current_red:
                    return (self.board.red_pieces[piece_local_id], [dest_x, dest_y])
                else:
                    return (self.board.black_pieces[piece_local_id], [dest_x, dest_y])
            except:
                print "Invalide move input! "

class randomPlayer(player):
    def __init__(self, board, is_red=True):
        player.__init__(self, board, is_red=is_red)
        self.prob_offense = 0.9

        self.OFF_PIECES = [3, 4, 5, 6]
        self.DEF_PIECES = [0, 1, 2]

        random.seed(time())

    def getStrategy(self):
        sleep(0)
        off_moves, def_moves = self.splitOffDef(self.board.possible_next_moves)

        if len(off_moves) == 0 or ( len(def_moves) !=0 and random.random() >= self.prob_offense ):
            # defence
            return self.pickOne(def_moves)
        else:
            # offence
            return self.pickOne(off_moves)

    def splitOffDef(self, possible_next_moves):
        off_moves = []
        def_moves = []
        for move in possible_next_moves:
            if move[0].piece_type in self.OFF_PIECES:
                off_moves.append((move[0], move[1]))
            if move[0].piece_type in self.DEF_PIECES:
                def_moves.append((move[0], move[1]))
        return off_moves, def_moves

    def pickOne(self, moves):
        total = len(moves)
        return moves[random.randint(0, total-1)]

class replayPlayer(player):
    def __init__(self, path_qipu, board, is_red=True):
        player.__init__(self, board, is_red=is_red)
        self.replay = self.board.loadMoves(path_qipu)

    def getStrategy(self):
        is_done = False 
        while not is_done:
            tmp_input = raw_input("Enter\t continue...\nrv\t Revert a move\nstop \t Stop game\n")
            if tmp_input in ["rv", "stop"]:
                return tmp_input
            if self.board.count_round == self.replay["total_round"]:
                print "Reached the end of the qipu. "
            else:
                is_done = True

        current_move = self.replay["moves"][self.board.count_round]
        local_id, src_location, dest_location, is_red = self.board.deSerialMove(current_move)
        assert is_red == self.board.is_current_red
        if True == is_red:
            my_pieces = self.board.red_pieces
        else:
            my_pieces = self.board.black_pieces
        return (my_pieces[local_id], dest_location)

class treePlayer(player):
    def __init__(self, board, depth=0, is_red=True):
        player.__init__(self, board, is_red=is_red)
        self.baseEvalOptions = {}
        self.baseEvalOptions['num_simus'] = 100
        self.baseEvalOptions['max_step'] = 150
        self.depth = depth

    def getStrategy(self):
        best_move, tmp_val = self.findBestMove

    def evalBoardValue(self, board, is_for_red=True, depth=0):
        pass

    def findBestMove(self):
        best_move = None
        tmp_val = None
        return best_move, tmp_val

    def baseEvalBoardValue(self, board, is_for_red=True):
        pass


class simulator:
    def __init__(self, board, is_allow_suicide=True):
        # default settings
        self.board = board
        self.setPlayer(player="random", is_red=True)
        self.setPlayer(player="random", is_red=False)
        self.current_board = None
        self.is_allow_suicide = is_allow_suicide

    def setPlayerBoard(self, board):
        self.red_player.setBoard(board)
        self.black_player.setBoard(board)

    def setPlayer(self, player="random", is_red=True):
        assert player in ["random"]
        if True == is_red:
            # red player
            if player == "random":
                self.red_player = randomPlayer(self.board, is_red=True)
        else:
            # black player
            if player == "random":
                self.black_player = randomPlayer(self.board, is_red=False)

    def saveQipu(self, board, path):
        if not os.path.isdir(os.path.dirname(path)):
            print "Path directory does not exists. "
            return False
        board.saveMoves(path)
        return True

    def simuMultiGame(self, num_simus=100, max_step=100, is_save_qipu=False, path_qipu_prefix=None):
        cur_path_qipu = None
        if True==is_save_qipu:
            assert os.path.isdir(os.path.dirname(path_qipu_prefix))
        winner_code = []
        for i in range(num_simus):
            if True==is_save_qipu:
                cur_path_qipu = path_qipu_prefix + "-" + str(i)
            cur_winner, cur_winner_code = self.simuOneGame(max_step=max_step, is_save_qipu=is_save_qipu, path_qipu=cur_path_qipu)
            winner_code.append(cur_winner_code)
        winner_code = np.array(winner_code)
        return np.sum(winner_code, axis=0) / float(num_simus)

    def simuOneGame(self, max_step=100, is_save_qipu=False, path_qipu=None):
        winner = None
        self.current_board = copy.deepcopy(self.board)
        self.setPlayerBoard(self.current_board) # !!! So important by current design. Considering put board as an argument in getStrategy method to optimize this. 
        for step in range(max_step):
            if True == self.current_board.is_current_red:
                current_player = self.red_player
            else:
                current_player = self.black_player
            best_move = current_player.getStrategy()
            move_status = self.current_board.moveToNextRound(best_move[0], best_move[1], self.is_allow_suicide)
            if move_status['is_lost'] > 0:
                if False == self.current_board.is_winner_red:
                    winner = "black"
                    winner_code = [0, 0, 1]
                else:
                    winner = "red"
                    winner_code = [1, 0, 0]
                break
        if None == winner:
            winner = "draw"
            winner_code = [0, 1, 0]
        if True == is_save_qipu:
            self.current_board.saveMoves(path_qipu, winner)
        return winner, winner_code