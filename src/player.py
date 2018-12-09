import random
from time import time, sleep

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
        tmp_input = raw_input("Type in the move. (piece_local_id dest_row dest_col) Or type \"showid\" to show the piece ids\n")
        while True:
            if tmp_input in ["draw", "rv", "pnext"]:
                return tmp_input
            if "showid" == tmp_input:
                try:
                    os.system("clear")
                except:
                    os.system("cls")
                self.board.display(self.board.is_current_red, "name")
                self.board.display(self.board.is_current_red, "id")
                tmp_input = raw_input("Type in the move. (piece_local_id dest_row dest_col)\n")
            segs = tmp_input.split()
            try:
                piece_local_id = int(segs[0])
                dest_x = int(segs[1])
                dest_y = int(segs[2])
                assert piece_local_id in range(16)
                if True == self.board.is_current_red:
                    return (self.board.red_pieces[piece_local_id], [dest_x, dest_y])
                else:
                    return (self.board.black_pieces[piece_local_id], [dest_x, dest_y])
            except:
                tmp_input = raw_input("Invalide move input. Type in the move again. (piece_local_id dest_row dest_col) Or type \"showid\" to show the piece ids\n")

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

