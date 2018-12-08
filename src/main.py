import board

reload(board)
board = board.board()
board.display(True)

piece = board.red_pieces[11]

print "Test for the possible moves"
print ""
print board.findPossibleMoves(piece)

print "Move it a little bit"
dest_location = [3, 3]
board.doMoveWithoutVal(piece, dest_location)
board.display(True)
print board.findPossibleMoves(piece)

print "Move it a little bit"
dest_location = [6, 3]
board.doMoveWithoutVal(piece, dest_location)
board.display(True)
print board.findPossibleMoves(piece)

# print "Move it a little bit"
# dest_location = [1, 3]
# board.doMoveWithoutVal(piece, dest_location)
# board.display(True)
# print board.findPossibleMoves(piece)
