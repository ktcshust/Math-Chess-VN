import random

from AI.AI import AI


class Negascout(AI):

    def findMove(self, gs, valid_moves):
        random.shuffle(valid_moves)
        self.findMoveNegaScout(gs, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if gs.red_to_move else -1)
        return self.next_move

    def findMoveNegaScout(self, gs, valid_moves, depth, alpha, beta, turn):
        if depth == 0 or self.isQuiescent(gs):
            return turn * self.scoreMaterial(gs.board)
        bestValue = -self.CHECKMATE
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getAllPossibleMoves()
            score = - self.findMoveNegaScout(gs, next_moves, depth - 1, -beta, -alpha, -turn)
            gs.undoMove()
            if score >= beta:
                return score
            if score > alpha:
                alpha = score
                beta = alpha + 1
                bestValue = alpha
        return bestValue

    def isQuiescent(self, gs):
        for row in gs.board:
            for square in row:
                if square[0] != "--" and square[1] != "0":
                    return False
        return True
