from __future__ import division

from copy import deepcopy
from mcts import mcts
from functools import reduce
import itertools
import operator

import numpy as np


class GravityGomokuState():
    def __init__(self, N, K):
        self.N = N # board size
        self.K = K # terminal condition
        self.board = [[0] * self.N for _ in range(self.N)]
        self.currentPlayer = 1

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0 and (i+1 >= self.N or self.board[i+1][j] != 0):
                    possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    '''
    終了条件に応じて、下記の値を返す
    - player1の勝利 -> +1
    - player2の勝利 -> -1
    - 未終了 -> 0
    - 盤面いっぱいのため終了 -> +2
    '''
    def isTerminal(self):
        # 上下
        for x in range(self.N):
            for y in range(self.N-self.K+1):
                tmp = sum([self.board[x][y + i] for i in range(self.K)])
                if abs(tmp) == self.K:
                    return tmp / self.K
        # 左右
        for y in range(self.N):
            for x in range(self.N-self.K+1):
                tmp = sum([self.board[x +i][y] for i in range(self.K)])
                if abs(tmp) == self.K:
                    return tmp / self.K
        # 左上 右下
        for x in range(self.N-self.K+1):
            for y in range(self.N-self.K+1):
                tmp = sum([self.board[x+i][y+i] for i in range(self.K)])
                if abs(tmp) == self.K:
                    return tmp / self.K
        # 右上 左下
        for x in range(self.N-self.K+1):
            for y in range(self.K-1, self.N):
                tmp = sum([self.board[x+i][y-i] for i in range(self.K)])
                if abs(tmp) == self.K:
                    return tmp / self.K
        # 盤面が全て埋まっていたら終了
        return reduce(operator.mul, sum(self.board, []), 1)
    
    def getReward(self):
        for x, y in itertools.product(np.arange(self.N-self.K+1), np.arange(self.N-self.K+1)):
            # 下
            if abs(sum([self.board[x+i][y] for i in range(self.K)])) == self.K:
                return sum([self.board[x+i][y] for i in range(self.K)]) / self.K
            # 右
            if abs(sum([self.board[x][y+i] for i in range(self.K)])) == self.K:
                return sum([self.board[x][y+i] for i in range(self.K)]) / self.K
            # 右下
            if abs(sum([self.board[x+i][y+i] for i in range(self.K)])) == self.K:
                return sum([self.board[x+i][y+i] for i in range(self.K)]) / self.K
        # 盤面が全て埋まっていたら終了
        return False

    # def draw_board(self):
    #     board_str = ""
    #     for row in self.board:
    #         for r in row:
    #             if r == 0:
    #                 board_str += 'X' 
    #             else:
    #                 color = 'A' if r == 1 else 'B'                    
    #                 board_str += color
    #         board_str += '\n'  
    #     return board_str

    def draw_board(self):
            board_str = ""
            for row in self.board:
                for r in row:
                    if r == 0:
                        board_str += '\033[38;2;255;255;255m○\033[0m'
                    else:
                        color = '●' if r == 1 else '○'                    
                        board_str += color
                board_str += '\n'  
            return board_str

class Action():
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y and self.player == other.player

    def __hash__(self):
        return hash((self.x, self.y, self.player))


if __name__ == "__main__":
    initialState = NaughtsAndCrossesState()
    searcher = mcts(timeLimit=1000)
    action = searcher.search(initialState=initialState, needDetails=True)

    print(action)
    