from board import board
from time import time
import os

class xiangQi:
    '''
    possible players
    '''
    def __init__(self, game_options=None):
        if None == game_options:
            # default settings
            self.game_options = {}
            self.game_options['red_player'] = "human"
            self.game_options['black_player'] = "human"
            self.game_options['red_player_options'] = None
            self.game_options['black_player_options'] = None
        else:
            self.game_options = game_options
        self.board = board()
        self._initPlayers()
        self.status = {}
        self.status['winner'] = None

    def main(self):
        self.startWords()

        timer_tic = time()
        while True:
            try:
                os.system("clear")
            except:
                os.system("cls")
            self.board.display(self.board.is_current_red, "name")
            if True == self.board.is_current_red:
                current_player = self.red_player
            else:
                current_player = self.black_player
            print current_player.name_pre+"'s turn."
            print current_player.name_pre+"'s total consumed time is " + str(current_player.timer) + " ."
            print "******************"

            best_move = current_player.getStrategy()
            if "draw" == best_move:
                print "Draw. Game over."
                break
            is_moved = self.board.moveToNextRound(best_move[0], best_move[1])
            while not is_moved:
                best_move = current_player.getStrategy()
                if "draw" == best_move:
                    print "Draw. Game over."
                    break
                is_moved = self.board.moveToNextRound(best_move[0], best_move[1])

            timer_toc = time()
            current_player.timer = current_player.timer + (timer_toc - timer_tic)
            timer_tic = timer_toc

            if True == self.board.isLost():
                if True == self.board.is_current_red:
                    self.status['winner'] = "black"
                else:
                    self.status['winner'] = "red"
                print self.status['winner'] + " won!! Game over. "
                break
        # saving
        self.saveMoves()
        
    def startWords(self):
        try:
            os.system("clear")
        except:
            os.system("cls")
        print "***********************"
        print ""
        print "Welcome to XiangQi~"
        print "    by Lex, Nov 2018"
        print ""
        print "***********************"
        print "red_player: ", self.game_options['red_player']
        print "black_player: ", self.game_options['black_player']
        print ""
        print "Press Enter to continue..."
        raw_input()

    def saveMoves(self):
        tmp_input = raw_input("Save qipu? (Y/N)\n")
        while tmp_input not in ["Y", "y", "N", "n"]:
            tmp_input = raw_input("Invalid input. \nSave qipu? (Y/N)\n")
        if tmp_input in ["Y", "y"]:
            tmp_input = raw_input("Type the path...\n")
            while not os.path.isdir(os.path.dirname(tmp_input)):
                tmp_input = raw_input("Invalid dir. Type the path...\n")
            with open(tmp_input, 'w') as fout:
                fout.write("\n".join(self.board.moves)) 

    def _initPlayers(self):
        # red player
        if self.game_options['red_player'] == "human":
            self.red_player = humanPlayer(self.board, is_red=True)
        if self.game_options['red_player'] == "AI":
            self.red_player = player(self.board, is_red=True, options=self.game_options['red_player_options'])
        # black player
        if self.game_options['black_player'] == "human":
            self.black_player = humanPlayer(self.board, is_red=False)
        if self.game_options['black_player'] == "AI":
            self.black_player = player(self.board, is_red=False, options=self.game_options['black_player_options'])

class player:
    def __init__(self, board, is_red=True, options=None):
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
            if "draw" == tmp_input:
                return "draw"
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