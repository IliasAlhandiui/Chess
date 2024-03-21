# Resp. for storing all information about the current GameState.
# Also, Resp. for determining valid moves at the current state.
# Also keep a move log

class GameState:
    def __init__(self):
        # bord is a 8x8 2d list, each element has 2 characters.
        # The first character rep. color of piece
        # second character rep. type of piece "K", "Q", "R", "B", "N" or "P"
        # "--" - rep. an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    '''
    Makes a move and exc. it(does not work fpr castling, pawn promotion, en-passant)
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log move so we can undo later
        self.whiteToMove = not self.whiteToMove  # swap players

    '''
    undo last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now, we will not worry about checks

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls appropriate move functions

        return moves

    '''
    Get all pawn moves at row and col and append to list 
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves

            if self.board[r - 1][c] == "--":  # one square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))

                if r == 6 and self.board[r - 2][c] == "--":  # two square moves
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves

            if self.board[r + 1][c] == "--":  # One square moves
                moves.append(Move((r, c), (r + 1, c), self.board))

                if r == 1 and self.board[r + 2][c] == "--":  # Two Square moves
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # capture left
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    Get all Rock moves at row and col and append to list 
    '''

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        self.rowColumnAndDiagonalMoves(c, directions, moves, r)

    # def getRookMoves(self, r, c, moves): My own Attempt
    #
    #     if self.whiteToMove:  # white rook moves
    #
    #         index = 1
    #         while (r - index) >= 0:  # up moves
    #             if self.board[r - index][c] == "--":
    #                 moves.append(Move((r, c), (r - index, c), self.board))
    #             if self.board[r - index][c][0] == "b":
    #                 moves.append(Move((r, c), (r - index, c), self.board))
    #                 break
    #             if self.board[r - index][c][0] == "w":
    #                 break
    #             index += 1
    #
    #         index = 1
    #         while r + index <= 7:  # move down
    #             if self.board[r + index][c] == "--":
    #                 moves.append(Move((r, c), (r + index, c), self.board))
    #             if self.board[r + index][c][0] == "b":
    #                 moves.append(Move((r, c), (r + index, c), self.board))
    #                 break
    #             if self.board[r + index][c][0] == "w":
    #                 break
    #             index += 1
    #
    #         index = 1
    #         while c - index >= 0:  # move left
    #             if self.board[r][c - index] == "--":
    #                 moves.append(Move((r, c), (r, c - index), self.board))
    #             if self.board[r][c - index][0] == "b":
    #                 moves.append(Move((r, c), (r, c - index), self.board))
    #                 break
    #             if self.board[r][c - index][0] == "w":
    #                 break
    #             index += 1
    #
    #         index = 1
    #         while c + index <= 7:  # move right
    #             if self.board[r][c + index] == "--":
    #                 moves.append(Move((r, c), (r, c + index), self.board))
    #             if self.board[r][c + index][0] == "b":
    #                 moves.append(Move((r, c), (r, c + index), self.board))
    #                 break
    #             if self.board[r][c - index][0] == "w":
    #                 break
    #             index += 1

    '''
    Get all Knight moves at row and col and append to list 
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, 1), (-2, -1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"

        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all Bishop moves at row and col and append to list 
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        self.rowColumnAndDiagonalMoves(c, directions, moves, r)

    def rowColumnAndDiagonalMoves(self, c, directions, moves, r):
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    '''
    Get all Queen moves at row and col and append to list 
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all King moves at row and col and append to list 
    '''

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move:
    # maps key to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
