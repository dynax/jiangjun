import random
from time import time, sleep
import os

class player:
    def __init__(self, board, is_red=True):
        self.is_red = is_red
        if True == self.is_red:
            self.name_pre = "Red"
        else:
            self.name_pre = "Black"
        self.timer = 0
        self.board = board

    def getStrategy(self, all_move_encodings):
        best_move = []
        return best_move

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
        self.board.findAllPossibleMoves()
        off_moves, def_moves = self.splitOffDef(self.board.possible_next_moves)
        if len(off_moves) == 0 or random.random() >= self.prob_offense:
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
                off_moves.append((move[0], move[2]))
            if move[0].piece_type in self.DEF_PIECES:
                def_moves.append((move[0], move[2]))

        return off_moves, def_moves

    def pickOne(self, moves):
        total = len(moves)
        return moves[random.randint(0, total-1)]

class replayPlayer(player):
    def __init__(self, path_qipu, board, is_red=True):
        player.__init__(self, board, is_red=is_red)
        self.replay = self._loadReplay(path_qipu)

    def _loadReplay(self, path_qipu):
        replay = {}
        with open(path_qipu, "r") as fin:
            tmp = fin.readline().split()
            replay["total_round"] = int(tmp[1])
            tmp = fin.readline().split()
            replay["winner"] = tmp[1]
            replay["moves"] = fin.read().split("\n")
        return replay

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

class valuePlayer(player):
    def __init__(self, board, is_red=True):
        player.__init__(self, board, is_red=is_red)

    def getStrategy(self):
        pass

    def evalAllValue(self):
        pass

class searchTreePlayer(valuePlayer):
    def evalAllValue(self):
        pass

    def evalOneValue(self):
        pass

class networkPlayer(valuePlayer):
    def evalAllValue(self):
        pass

    def evalOneValue(self):
        pass

class simulator:
    def __init__(self):
        pass

