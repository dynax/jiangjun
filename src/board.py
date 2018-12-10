import sys
import copy

class board:
    '''

    '''
    def __init__(self, mode="default"):
        self.red_pieces = []
        self.black_pieces = []
        self.red_board = None
        self.black_board = None
        self.is_current_red = True
        self.count_round = 0
        self.dead_pieces = {}
        self.moves = []
        self.possible_next_moves = []

        self.NUM_BOARD_COLS = 9
        self.NUM_BOARD_ROWS = 10
        if "default" == mode:
            self._init_board()

    def serialMove(self, piece, src_location, dest_location):
        return str(piece.global_id)+"\t"+str(src_location[0])+","+str(src_location[1])+"\t"+str(dest_location[0])+","+str(dest_location[1])

    def deSerialMove(self, move_code):
        tmp_segs = move_code.split("\t")
        global_id = int(tmp_segs[0])
        src_location = [int(x) for x in tmp_segs[1].split(",")]
        dest_location = [int(x) for x in tmp_segs[2].split(",")]
        local_id = global_id % 16
        is_red = global_id < 16
        return local_id, src_location, dest_location, is_red

    def saveMoves(self, path, winner):
        assert winner in ["black", "red", "draw"]
        with open(path, 'w') as fout:
            fout.write("total_round: "+str(self.count_round)+"\n")
            fout.write("winner: "+winner+"\n")
            fout.write("\n".join(self.moves)) 
            fout.write("\n")
        return True

    def loadMoves(self, path_qipu):
        replay = {}
        with open(path_qipu, "r") as fin:
            tmp = fin.readline().split()
            replay["total_round"] = int(tmp[1])
            tmp = fin.readline().split()
            replay["winner"] = tmp[1]
            replay["moves"] = fin.read().split("\n")
        return replay  

    def findAllPossibleMoves(self):
        # list all moves
        self._findAllPossibleMoves()
        # filter out forbidded moves that is under check
        # TODO
        # filter out the forbidden moves that is under check


    def _findAllPossibleMoves(self):
        # don't consider the forbidden move due to check in this function
        self.possible_next_moves = []
        if True == self.is_current_red:
            my_pieces = self.red_pieces
        else:
            my_pieces = self.black_pieces
        for piece in my_pieces:
            if True == piece.is_alive:
                src_location = piece.location
                for dest_location in piece.findPossibleMoves(self):
                    self.possible_next_moves.append((piece, src_location, dest_location))

    # def isCheck(self, is_check_red=True):
    #     if True == is_check_red:
    #         my_shuai_location = self.red_pieces[0].location
    #         killers = self.black_pieces
    #     else:
    #         my_shuai_location = self.black_pieces[0].location
    #         killers = self.black_pieces
    #     for each_killer in killers:
    #         if True==each_killer.is_alive:
    #             killer_dest_location = each_killer.findPossibleMoves()

    #     return False

    def isLost(self):
        if True == self.is_current_red:
            current_piece = self.red_pieces
        else:
            current_piece = self.black_pieces
        return not current_piece[0].is_alive

    def revertToPrevious(self):
        if self.count_round == 0:
            print "It is the first round. Invalid revert. "
            return False

        tmp_last_move = self.moves[-1]
        self.moves.remove(tmp_last_move)
        self.is_current_red = not self.is_current_red
        self.count_round = self.count_round - 1
        local_id, src_location, dest_location, is_red = self.deSerialMove(tmp_last_move)

        if True == is_red:
            piece = self.red_pieces[local_id]
            my_board = self.red_board
            opp_board = self.black_board
        else:
            piece = self.black_pieces[local_id]
            my_board = self.black_board
            opp_board = self.red_board
        # do my board
        ori_x = src_location[0]
        ori_y = src_location[1]
        dest_x = dest_location[0]
        dest_y = dest_location[1]
        try:
            reborn_piece = self.dead_pieces.pop(self.count_round)
            reborn_piece.setAlive()
            is_contain_reborn = True
        except:
            is_contain_reborn = False
        my_board[ori_x][ori_y] = my_board[dest_x][dest_y]
        if True == is_contain_reborn:
            my_board[dest_x][dest_y] = reborn_piece
        else:
            my_board[dest_x][dest_y] = None
        # do opp board
        ori_x = self.NUM_BOARD_ROWS - 1 - ori_x
        ori_y = self.NUM_BOARD_COLS - 1 - ori_y
        dest_x = self.NUM_BOARD_ROWS - 1 - dest_x
        dest_y = self.NUM_BOARD_COLS - 1 - dest_y
        opp_board[ori_x][ori_y] = opp_board[dest_x][dest_y]
        if True == is_contain_reborn:
            opp_board[dest_x][dest_y] = reborn_piece
        else:
            opp_board[dest_x][dest_y] = None
        # change the piece info
        piece.location = src_location
        return True

    def moveToNextRound(self, piece, dest_location):
        possible_moves = piece.findPossibleMoves(self)
        if True == self.isValidateMove(dest_location, possible_moves) and True == piece.is_alive:
            src_location = piece.location
            self.doMoveWithoutVal(piece, dest_location)
            self.count_round = self.count_round + 1
            self.is_current_red = not self.is_current_red
            self.moves.append(self.serialMove(piece, src_location, dest_location))
            return True
        else:
            return False

    def isValidateMove(self, dest_location, possible_moves):
        return dest_location in possible_moves

    # def findPossibleMoves(self, piece):
    #     if True == piece.is_red:
    #         return piece.findPossibleMoves(piece, self.red_board)
    #     else:
    #         return piece.findPossibleMoves(piece, self.black_board)

    def doMoveWithoutVal(self, piece, dest_location):
        '''
        remember to do the validation before truely doing the move
        '''
        if True == piece.is_red:
            my_board = self.red_board
            opp_board = self.black_board
        else:
            my_board = self.black_board
            opp_board = self.red_board
        # do my board
        ori_x = piece.location[0]
        ori_y = piece.location[1]
        dest_x = dest_location[0]
        dest_y = dest_location[1]
        if None != my_board[dest_x][dest_y]:
            self.dead_pieces[self.count_round] = my_board[dest_x][dest_y]
            my_board[dest_x][dest_y].setDeath(self.count_round)
        my_board[dest_x][dest_y] = my_board[ori_x][ori_y]
        my_board[ori_x][ori_y] = None
        # do opp board
        ori_x = self.NUM_BOARD_ROWS - 1 - ori_x
        ori_y = self.NUM_BOARD_COLS - 1 - ori_y
        dest_x = self.NUM_BOARD_ROWS - 1 - dest_x
        dest_y = self.NUM_BOARD_COLS - 1 - dest_y
        opp_board[dest_x][dest_y] = opp_board[ori_x][ori_y]
        opp_board[ori_x][ori_y] = None
        # change the piece info
        piece.location = dest_location
        return True

    def display(self, is_red, mode = "name"):
        '''
        mode in ["name", "id"]
        '''
        assert mode in ["name", "id"]
        print "*********************"
        print "Round: " + str(self.count_round)

        if True==is_red:
            current_board = self.red_board
            print "red view"
        else:
            current_board = self.black_board
            print "black view"
        print "*********************"
        print "    0 1 2 3 4 5 6 7 8"
        print "---------------------"

        for row in range(self.NUM_BOARD_ROWS): 
            row = self.NUM_BOARD_ROWS - 1 - row
            sys.stdout.write(str(row)+" |")
            for col in range(self.NUM_BOARD_COLS):
                if None == current_board[row][col]:
                    sys.stdout.write("  ")
                else:
                    if "name" == mode:
                        sys.stdout.write(current_board[row][col].dis_name)
                    if "id" == mode:
                        id = current_board[row][col].global_id % 16
                        if id < 10:
                            sys.stdout.write(" "+str(id))
                        else:
                            sys.stdout.write(str(id))
            sys.stdout.write("\n")
        sys.stdout.flush()
        print "*********************"

    def _init_board(self, mode='default'):
        if 'default' == mode:
            self._gen_pieces_default()
        if 'test' == mode:
            self._gen_pieces_test()
        self._set_board()

    def _gen_pieces_test(self):
        tmp_base = 0
        is_red = True
        my_pieces = self.red_pieces
        my_pieces.append(jiang(is_red=is_red, location=[0, 4], global_id=tmp_base+0, is_alive=True))
        my_pieces.append(shi(is_red=is_red, location=[1, 4], global_id=tmp_base+1, is_alive=True))
        my_pieces.append(shi(is_red=is_red, location=[0, 5], global_id=tmp_base+2, is_alive=False))
        my_pieces.append(xiang(is_red=is_red, location=[0, 2], global_id=tmp_base+3, is_alive=False))
        my_pieces.append(xiang(is_red=is_red, location=[0, 6], global_id=tmp_base+4, is_alive=False))
        my_pieces.append(ma(is_red=is_red, location=[0, 1], global_id=tmp_base+5, is_alive=True))
        my_pieces.append(ma(is_red=is_red, location=[0, 7], global_id=tmp_base+6, is_alive=False))
        my_pieces.append(ju(is_red=is_red, location=[0, 0], global_id=tmp_base+7, is_alive=False))
        my_pieces.append(ju(is_red=is_red, location=[0, 8], global_id=tmp_base+8, is_alive=False))
        my_pieces.append(pao(is_red=is_red, location=[2, 1], global_id=tmp_base+9, is_alive=False))
        my_pieces.append(pao(is_red=is_red, location=[2, 7], global_id=tmp_base+10, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 0], global_id=tmp_base+11, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 2], global_id=tmp_base+12, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 4], global_id=tmp_base+13, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 6], global_id=tmp_base+14, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 8], global_id=tmp_base+15, is_alive=False))
        tmp_base = 16
        is_red = False
        my_pieces = self.black_pieces
        my_pieces.append(jiang(is_red=is_red, location=[0, 4], global_id=tmp_base+0, is_alive=True))
        my_pieces.append(shi(is_red=is_red, location=[0, 3], global_id=tmp_base+1, is_alive=False))
        my_pieces.append(shi(is_red=is_red, location=[0, 5], global_id=tmp_base+2, is_alive=False))
        my_pieces.append(xiang(is_red=is_red, location=[0, 2], global_id=tmp_base+3, is_alive=False))
        my_pieces.append(xiang(is_red=is_red, location=[0, 6], global_id=tmp_base+4, is_alive=False))
        my_pieces.append(ma(is_red=is_red, location=[0, 1], global_id=tmp_base+5, is_alive=False))
        my_pieces.append(ma(is_red=is_red, location=[0, 7], global_id=tmp_base+6, is_alive=False))
        my_pieces.append(ju(is_red=is_red, location=[0, 0], global_id=tmp_base+7, is_alive=False))
        my_pieces.append(ju(is_red=is_red, location=[0, 8], global_id=tmp_base+8, is_alive=False))
        my_pieces.append(pao(is_red=is_red, location=[2, 1], global_id=tmp_base+9, is_alive=False))
        my_pieces.append(pao(is_red=is_red, location=[2, 7], global_id=tmp_base+10, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 0], global_id=tmp_base+11, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 2], global_id=tmp_base+12, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 4], global_id=tmp_base+13, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 6], global_id=tmp_base+14, is_alive=False))
        my_pieces.append(bing(is_red=is_red, location=[3, 8], global_id=tmp_base+15, is_alive=False))

    def _gen_pieces_default(self):
        self._gen_half_pieces_default(is_red=True)
        self._gen_half_pieces_default(is_red=False)

    def _gen_half_pieces_default(self, is_red=True):
        if True==is_red:
            my_pieces = self.red_pieces
            tmp_base = 0
        else:
            my_pieces = self.black_pieces
            tmp_base = 16
        my_pieces.append(jiang(is_red=is_red, location=[0, 4], global_id=tmp_base+0))
        my_pieces.append(shi(is_red=is_red, location=[0, 3], global_id=tmp_base+1))
        my_pieces.append(shi(is_red=is_red, location=[0, 5], global_id=tmp_base+2))
        my_pieces.append(xiang(is_red=is_red, location=[0, 2], global_id=tmp_base+3))
        my_pieces.append(xiang(is_red=is_red, location=[0, 6], global_id=tmp_base+4))
        my_pieces.append(ma(is_red=is_red, location=[0, 1], global_id=tmp_base+5))
        my_pieces.append(ma(is_red=is_red, location=[0, 7], global_id=tmp_base+6))
        my_pieces.append(ju(is_red=is_red, location=[0, 0], global_id=tmp_base+7))
        my_pieces.append(ju(is_red=is_red, location=[0, 8], global_id=tmp_base+8))
        my_pieces.append(pao(is_red=is_red, location=[2, 1], global_id=tmp_base+9))
        my_pieces.append(pao(is_red=is_red, location=[2, 7], global_id=tmp_base+10))
        my_pieces.append(bing(is_red=is_red, location=[3, 0], global_id=tmp_base+11))
        my_pieces.append(bing(is_red=is_red, location=[3, 2], global_id=tmp_base+12))
        my_pieces.append(bing(is_red=is_red, location=[3, 4], global_id=tmp_base+13))
        my_pieces.append(bing(is_red=is_red, location=[3, 6], global_id=tmp_base+14))
        my_pieces.append(bing(is_red=is_red, location=[3, 8], global_id=tmp_base+15))

    def _set_board(self):
        self.red_board = [[None]*self.NUM_BOARD_COLS for i in range(self.NUM_BOARD_ROWS)]
        self.black_board = [[None]*self.NUM_BOARD_COLS for i in range(self.NUM_BOARD_ROWS)]
        self._set_half_board(is_red=True)
        self._set_half_board(is_red=False)

    def _set_half_board(self, is_red=True):
        if True==is_red:
            my_piece = self.red_pieces
            my_board = self.red_board
            opp_board = self.black_board
        else:
            my_piece = self.black_pieces
            my_board = self.black_board
            opp_board = self.red_board
        for piece in my_piece:
            if True==piece.is_alive:
                tmp_x = piece.location[0]
                tmp_y = piece.location[1]
                my_board[tmp_x][tmp_y] = piece
                tmp_x = self.NUM_BOARD_ROWS - 1 - tmp_x
                tmp_y = self.NUM_BOARD_COLS - 1 - tmp_y
                opp_board[tmp_x][tmp_y] = piece

class boardEncoder:
    '''
    '''
    def __init__(self, board):
        self.board = board

    def encodeAllnextStates(self):
        pass

    def encodeCurrent(self):
        pass

class piece:
    '''
    piece_type int and real piece mapping
        jiang/shuai = 0
        shi = 1
        xiang = 2
        ma = 3
        ju = 4
        pao = 5
        bing/zu = 6
    '''
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        self.is_red = is_red
        self.location = location
        self.global_id = global_id
        self.is_alive = is_alive
        self.dead_round = None
        if True == self.is_red:
            self.dis_name = "+"
        else:
            self.dis_name = "-"

    def findPossibleMoves(self, piece, current_board):
        pass 

    def setDeath(self, count_round):
        self.is_alive = False
        self.dead_round = count_round

    def setAlive(self):
        self.is_alive = True
        self.dead_round = None

    def _isValidDest(self, dest_location, current_board):
        '''
        handling the boundary and judge whether self piece is on
        '''
        NUM_BOARD_ROWS = len(current_board)
        NUM_BOARD_COLS = len(current_board[0])
        x = dest_location[0]
        y = dest_location[1]
        if x < 0 or y < 0 or x >= NUM_BOARD_ROWS or y >= NUM_BOARD_COLS:
            return False
        if None == current_board[x][y]:
            return True
        if self.is_red == current_board[x][y].is_red:
            return False
        return True
    def _isContainPiece(self, location, current_board):
        x = location[0]
        y = location[1]
        return None != current_board[x][y]

class jiang(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=0
        self.dis_name += "J"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        # up
        cx = x+1
        cy = y
        if cx <= 2 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # down
        cx = x-1
        cy = y
        if cx >= 0 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # left
        cx = x
        cy = y-1
        if cy >= 3 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # right
        cx = x
        cy = y+1
        if cy <= 5 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        ## he jiu
        is_align = False
        ty = y
        for tx in range(7, 10):
            if self._isContainPiece([tx, ty], current_board) and 0 == current_board[tx][ty].piece_type:
                is_align = True
                break
        if True == is_align:
            is_block = False
            oy = y
            for ox in range(x+1, tx):
                if self._isContainPiece([ox, oy], current_board):
                    is_block = True
                    break
            if False == is_block:
                possible_moves.append([tx, ty])
        return possible_moves

class shi(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=1
        self.dis_name += "S"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        # top-left
        cx = x+1
        cy = y-1
        if cx <= 2 and cy >= 3 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # top-right
        cx = x+1
        cy = y+1
        if cx <= 2 and cy <= 5 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # bot-left
        cx = x-1
        cy = y-1
        if cx >= 0 and cy >= 3 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # bot-right
        cx = x-1
        cy = y+1
        if cx >= 0 and cy <= 5 and self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        return possible_moves

class xiang(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=2
        self.dis_name += "X"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        # top-left
        cx = x+2
        cy = y-2
        ox = x+1
        oy = y-1
        if cx <= 4 and self._isValidDest([cx, cy], current_board) and None == current_board[ox][oy]:
            possible_moves.append([cx, cy])
        # top-right
        cx = x+2
        cy = y+2
        ox = x+1
        xy = y+1
        if cx <= 4 and self._isValidDest([cx, cy], current_board) and None == current_board[ox][xy]:
            possible_moves.append([cx, cy])
        # bot-left
        cx = x-2
        cy = y-2
        ox = x-1
        xy = y-1
        if self._isValidDest([cx, cy], current_board) and None == current_board[ox][oy]:
            possible_moves.append([cx, cy])
        # bot-right
        cx = x-2
        cy = y+2
        ox = x-1
        oy = y+1
        if self._isValidDest([cx, cy], current_board) and None == current_board[ox][oy]:
            possible_moves.append([cx, cy])
        return possible_moves

class ma(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=3
        self.dis_name += "M"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        # top-two
        ox = x+1
        oy = y
        if True == self._isValidDest([ox, oy], current_board) and False == self._isContainPiece([ox, oy], current_board):
            cx = ox+1
            cy = oy-1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
            cx = ox+1
            cy = oy+1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
        # bot-two
        ox = x-1
        oy = y
        if True == self._isValidDest([ox, oy], current_board) and False == self._isContainPiece([ox, oy], current_board):
            cx = ox-1
            cy = oy-1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
            cx = ox-1
            cy = oy+1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
        # left-two
        ox = x
        oy = y-1
        if True == self._isValidDest([ox, oy], current_board) and False == self._isContainPiece([ox, oy], current_board):
            cx = ox-1
            cy = oy-1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
            cx = ox+1
            cy = oy-1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
        # right-two
        ox = x
        oy = y+1
        if True == self._isValidDest([ox, oy], current_board) and False == self._isContainPiece([ox, oy], current_board):
            cx = ox-1
            cy = oy+1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
            cx = ox+1
            cy = oy+1
            if True == self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
        return possible_moves

class ju(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=4
        self.dis_name += "U"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        NUM_BOARD_ROWS = len(current_board)
        NUM_BOARD_COLS = len(current_board[0])
        # top
        cy = y
        cx = x+1
        while cx < NUM_BOARD_ROWS:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cx = cx+1
        # bot
        cy = y
        cx = x-1
        while cx >= 0:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cx = cx-1
        # left
        cx = x
        cy = y-1
        while cy >= 0:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cy = cy-1
        # right
        cx = x
        cy = y+1
        while cy < NUM_BOARD_COLS:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cy = cy+1
        return possible_moves

class pao(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=5
        self.dis_name += "P"

    def findPossibleMoves(self, board):
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        NUM_BOARD_ROWS = len(current_board)
        NUM_BOARD_COLS = len(current_board[0])
        # top
        cy = y
        cx = x+1
        while cx < NUM_BOARD_ROWS:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                break
            cx = cx+1
        cx = cx+1
        while cx < NUM_BOARD_ROWS:
            if True == self._isContainPiece([cx, cy], current_board):
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cx = cx+1
        # bot
        cy = y
        cx = x-1
        while cx >= 0:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                break
            cx = cx-1
        cx = cx-1
        while cx >= 0:
            if True == self._isContainPiece([cx, cy], current_board):
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cx = cx-1
        # left
        cx = x
        cy = y-1
        while cy >= 0:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                break
            cy = cy-1
        cy = cy-1
        while cy >= 0:
            if True == self._isContainPiece([cx, cy], current_board):
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cy = cy-1
        # right
        cx = x
        cy = y+1
        while cy < NUM_BOARD_COLS:
            if False == self._isContainPiece([cx, cy], current_board):
                possible_moves.append([cx, cy])
            else:
                break
            cy = cy+1
        cy = cy+1
        while cy < NUM_BOARD_COLS:
            if True == self._isContainPiece([cx, cy], current_board):
                if True == self._isValidDest([cx, cy], current_board):
                    possible_moves.append([cx, cy])
                break
            cy = cy+1

        return possible_moves

class bing(piece):
    def __init__(self, is_red=True, location=None, global_id=None, is_alive=True):
        piece.__init__(self, is_red=is_red, location=location, global_id=global_id, is_alive=is_alive)
        self.piece_type=6
        self.dis_name += "Z"

    def findPossibleMoves(self, board):
        possible_moves = []
        x = self.location[0]
        y = self.location[1]
        if True == self.is_red:
            current_board = board.red_board
        else:
            current_board = board.black_board
        # up
        cx = x+1
        cy = y
        if self._isValidDest([cx, cy], current_board):
            possible_moves.append([cx, cy])
        # guo he
        if x >= 5:    
            # left
            cx = x
            cy = y-1
            if self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])
            # right
            cx = x
            cy = y+1
            if self._isValidDest([cx, cy], current_board):
                possible_moves.append([cx, cy])

        return possible_moves