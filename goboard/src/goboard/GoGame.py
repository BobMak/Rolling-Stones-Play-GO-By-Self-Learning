"from sphero_formation commit 0ac14aad3"

from __future__ import print_function

from Game import Game
from GoLogic import Board
import numpy as np
from copy import deepcopy


class GoGame(Game):
    def __init__(self, n=5):
        self.n = n
        self.b = Board(self.n)
        self.pass_count = 0
        # ROS
        # flag indicating if robot stones are moved to their positions,
        # and the next move can be made
        self.board_ready = False

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        move = (int(action / self.n), action % self.n)
        if move == self.b.PASS:
            self.pass_count += 1
            return (board, -player)
        self.pass_count = 0
        self.b.pieces = deepcopy(board)
        self.b.execute_move(move, player)
        return (self.b.pieces, -player)

    # modified
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()

        self.b.pieces = deepcopy(board)
        legalMoves = self.b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    # modified
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = deepcopy(board)
        if b.has_legal_moves() and self.pass_count != 2:
            return 0
        # game ended
        black_score = b.calculate_score(-1)
        white_score = b.calculate_score(1)
        if black_score > white_score:
            return -1
        elif black_score < white_score:
            return 1
        return 0.5

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):
        n = board.shape[0]

        for y in range(n):
            print(y, "|", end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1:
                    print("w ", end="")
                elif piece == 1:
                    print("b ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")
