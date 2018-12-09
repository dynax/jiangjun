from board import board
from time import time
import datetime
import os
import random
from player import humanPlayer, randomPlayer

class xiangQi:
    '''
    possible players: human, random
    '''
    def __init__(self):
        self.game_options = {}
        self.game_options['red_player'] = None
        self.game_options['black_player'] = None
        self.game_options['red_player_options'] = None
        self.game_options['black_player_options'] = None
        self.status = {}
        self.status['winner'] = None
        self.VALID_PLAYER = ["human", "random"]

        self.startWords()
        self.board = board()
        self._initPlayers()

    def main(self):
        timer_tic = time()
        is_end = False
        while not is_end:
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
            print current_player.name_pre+"'s total consumed time is " + str(datetime.timedelta(current_player.timer / 1000)) + " ."
            print "******************"

            is_moved = False
            while not is_moved:
                best_move = current_player.getStrategy()
                # signal for draw
                if "draw" == best_move:
                    self.endWords("draw")
                    is_end = True
                    is_moved = True
                    continue
                # signal for revert a round
                if "rv" == best_move:
                    is_moved = self.board.revertToPrevious()
                    continue
                if "pnext" == best_move:
                    is_moved = False
                    self.board.findAllPossibleMoves()
                    for each_move in self.board.possible_next_moves:
                        print each_move
                    continue
                is_moved = self.board.moveToNextRound(best_move[0], best_move[1])

            timer_toc = time()
            current_player.timer = current_player.timer + (timer_toc - timer_tic)
            timer_tic = timer_toc

            if True == self.board.isLost():
                self.endWords("won")
                is_end = True
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
        print "    by Lex, Dec 2018"
        print ""
        print "***********************"
        print "Press Enter to continue..."
        raw_input()
        print "Setting players"
        print "Valid players: " + " ".join(self.VALID_PLAYER)
        is_set = False
        while not is_set:
            tmp_input = raw_input("Red player: ")
            is_set = tmp_input in self.VALID_PLAYER
        self.game_options['red_player'] = tmp_input
        is_set = False
        while not is_set:
            tmp_input = raw_input("Black player: ")
            is_set = tmp_input in self.VALID_PLAYER
        self.game_options['black_player'] = tmp_input
        print "***********************"
        print "red_player: ", self.game_options['red_player']
        print "black_player: ", self.game_options['black_player']
        print ""
        print "Press Enter to continue..."
        raw_input()

    def endWords(self, state):
        try:
            os.system("clear")
        except:
            os.system("cls")
        print "*       **    *       *  "
        print "*      *  *   *       *  "
        print "*      *  *   *          "
        print "****    **    ****    *  "
        print " "

        if "won" == state:
            if True == self.board.is_current_red:
                self.status['winner'] = "black"
            else:
                self.status['winner'] = "red"
            print self.status['winner'] + " won!! Game over. "
        elif "draw" == state:
            print "Draw game. Game over. "

        raw_input("Press enter to continue...")
        self.board.display(not self.board.is_current_red, "name")        
        print ""

    def saveMoves(self):
        tmp_input = raw_input("Save qipu? (Y/N)\n")
        while tmp_input not in ["Y", "y", "N", "n"]:
            tmp_input = raw_input("Invalid input. \nSave qipu? (Y/N)\n")
        if tmp_input in ["Y", "y"]:
            tmp_input = raw_input("Type the path...\n")
            while not os.path.isdir(os.path.dirname(tmp_input)):
                tmp_input = raw_input("Invalid dir. Type the path...\n")
            with open(tmp_input, 'w') as fout:
                fout.write("total_round: "+str(self.board.count_round)+"\n")
                fout.write("winner: "+self.status['winner']+"\n")
                fout.write("\n".join(self.board.moves)) 
                fout.write("\n")

    def _initPlayers(self):
        # red player
        if self.game_options['red_player'] == "human":
            self.red_player = humanPlayer(self.board, is_red=True)
        if self.game_options['red_player'] == "random":
            self.red_player = randomPlayer(self.board, is_red=True)
        if self.game_options['red_player'] == "AI":
            self.red_player = player(self.board, is_red=True, options=self.game_options['red_player_options'])
        # black player
        if self.game_options['black_player'] == "human":
            self.black_player = humanPlayer(self.board, is_red=False)
        if self.game_options['black_player'] == "random":
            self.black_player = randomPlayer(self.board, is_red=False)
        if self.game_options['black_player'] == "AI":
            self.black_player = player(self.board, is_red=False, options=self.game_options['black_player_options'])

if __name__ == "__main__":
    interface = xiangQi()
    interface.main()
