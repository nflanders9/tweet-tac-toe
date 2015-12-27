"""
tic-tac-tweet.py
Nick Flanders

Twitter bot that plays Tic-Tac-Toe through tweets and replies
"""
__author__ = 'Nick Flanders'
from enum import Enum
import sys
import math
import random

class GamePiece(Enum):
    """
    Represents the possible states of any given square in the model
    """
    EMPTY = 0
    X = 1
    O = 2


class GameModel:
    """
    Represents a model for a game of Tic Tac Toe
    """
    def __init__(self, board=None, turn=GamePiece.X):
        if board is None:
            self.board = [[GamePiece.EMPTY, GamePiece.EMPTY, GamePiece.EMPTY],
                          [GamePiece.EMPTY, GamePiece.EMPTY, GamePiece.EMPTY],
                          [GamePiece.EMPTY, GamePiece.EMPTY, GamePiece.EMPTY]]
        else:
            self.board = board
        self.turn = turn

    def check_winner(self):
        """
        Check to see if this game has been won
        :return: the GamePiece value of the winner (including Empty if the game has not been won)
        """
        # check to see if there are any winners in any of the columns
        for col in self.board:
            check_piece = col[0]
            all_equal = True
            for piece in col:
                if piece != col[0] or check_piece == GamePiece.EMPTY:
                    all_equal = False
                    break
            if all_equal:
                return check_piece

        # check to see if there are any winners in any of the rows of this game
        for row_index in range(len(self.board)):
            check_piece = self.board[0][row_index]
            all_equal = True
            for col_index in range(len(self.board)):
                if self.board[col_index][row_index] != check_piece or check_piece == GamePiece.EMPTY:
                    all_equal = False
                    break
            if all_equal:
                return check_piece

        # check the two diagonals to see if the game has been won
        check_piece = self.board[0][0]
        all_equal = True
        for index in range(len(self.board)):
            if self.board[index][index] != check_piece or check_piece == GamePiece.EMPTY:
                all_equal = False
                break
        if all_equal:
            return check_piece

        check_piece = self.board[0][-1]
        all_equal = True
        for index in range(len(self.board)):
            if self.board[index][len(self.board) - 1 - index] != check_piece or check_piece == GamePiece.EMPTY:
                all_equal = False
                break
        if all_equal:
            return check_piece

        return GamePiece.EMPTY

    def _get_open_spots(self):
        """
        Return the list of tuples containing the coordinates of all of the
        available spaces in the board of this game
        :return:    list of ordered pairs of available spaces in this game
        """
        empty = []
        for col_index in range(len(self.board)):
            for row_index in range(len(self.board[col_index])):
                if self.board[col_index][row_index] == GamePiece.EMPTY:
                    empty.append((col_index, row_index))
        return empty

    def _do_move(self, col, row):
        """
        Returns a copy of this board after performing the given move
        :param col: the column to insert a new piece at
        :param row: the row to insert a new piece at
        :return:    a list of lists representing the new board
        """
        # performa a deep copy of this current board
        new_board = [[piece for piece in column] for column in self.board]
        if new_board[col][row] != GamePiece.EMPTY:
            raise RuntimeError("Trying to move over a populated space")
        new_board[col][row] = self.turn
        return new_board

    def _get_opponent(self):
        """
        Get the player who is the opponent to the current player
        :return:  GamePiece of the opposing player
        """
        if self.turn == GamePiece.X:
            return GamePiece.O
        else:
            return GamePiece.X

    def get_best_move(self):
        """
        Perform a minimax search in order to find the optimal move from this point in
        the game. Positive scores indicate a situation that is favorable for X and
        negative scores indicate a result which is favorable to O
        :return: the tuple containing the ordered pair that is the optimal move based
        on the current game state or None if the game is already over
        """
        winner = self.check_winner()
        if winner != GamePiece.EMPTY:
            return None
        moves = self._get_open_spots()
        scores = []
        for move in moves:
            new_state = GameModel(board=self._do_move(*move), turn=self._get_opponent())
            scores.append(new_state.minimax_values(0))
        if self.turn == GamePiece.X:
            return moves[random_index(scores, max(scores))]
        else:
            return moves[random_index(scores, min(scores))]


    def minimax_values(self, depth):
        """
        Perform minimax search where states favorable to X are positive and state favorable
        to O are negative
        :return: goodness value for the current state
        """
        winner = self.check_winner()
        if winner == GamePiece.X:
            return 10 - depth
        elif winner == GamePiece.O:
            return -10 + depth
        else:
            moves = self._get_open_spots()
            scores = []
            for move in moves:
                next_state = GameModel(board=self._do_move(*move), turn=self._get_opponent())
                scores.append(next_state.minimax_values(depth + 1))
            if len(scores) == 0:
                return 0
            if self.turn == GamePiece.X:
                return max(scores)
            else:
                return min(scores)

    def game_over(self):
        """
        Is this game over?
        :return: True if the game is over, False, otherwise
        """
        if self.check_winner() == GamePiece.EMPTY:
            for col in self.board:
                for piece in col:
                    if piece == GamePiece.EMPTY:
                        return False
        return True

    def __str__(self):
        """
        Return the string representation of the current game
        :return: the string representation of the current game
        """
        output = ""
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board)):
                if self.board[col_index][row_index] == GamePiece.EMPTY:
                    piece = " "
                else:
                    piece = self.board[col_index][row_index].name
                output += "[" + piece + "]"
            output += "\n"
        return output

    @classmethod
    def parse_board(cls, board_str):
        """
        Create a new game based on the given ASCII board
        :return:    a GameModel based on the given ASCII board
        """
        board_str = board_str.replace("[]", "[ ]").replace("[", "").replace("]", "").replace("\n", "")
        size = int(math.sqrt(len(board_str)))
        board = []
        num_x = 0
        num_o = 0
        for col in range(size):
            board.append([])
            for row in range(size):
                character = board_str[col + 3 * row].upper()
                if character == "X":
                    board[col].append(GamePiece.X)
                    num_x += 1
                elif character == "O":
                    board[col].append(GamePiece.O)
                    num_o += 1
                elif character == " ":
                    board[col].append(GamePiece.EMPTY)
                else:
                    print(character)
        if abs(num_o - num_x) > 1:
            raise ValueError("invalid board string")
        turn = GamePiece.X if num_x <= num_o else GamePiece.O
        return GameModel(board=board, turn=turn)

def random_index(list, obj):
    """
    Return the index of a random occurrence of the given object in the given list
    :param list: list that contains the given object
    :param obj:  object to search for in the list
    :return:     int index of the object in the list
    """
    temp = [item for item in list]
    if obj not in list:
        raise IndexError("given value not in list")
    else:
        occurrences = temp.count(obj)
        if occurrences == 1:
            return list.index(obj)
        occurrence = random.randint(0, temp.count(obj) - 2)
        for _ in range(occurrence):
            temp.remove(obj)
            temp = [0] + temp
        return temp.index(obj)


if __name__ == "__main__":
    # test for the minimax search algorithm
    game = GameModel.parse_board(
    "[][ ][]\n[][][]\n[][][]"
    )
    print(game)
    while not game.game_over():
        game.board = game._do_move(*(game.get_best_move()))
        game.turn = game._get_opponent()
        print(game)