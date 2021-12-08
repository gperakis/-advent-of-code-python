from typing import List, NoReturn, Union, Dict

import numpy as np
from more_itertools import chunked

from config import DATA_DIR


class Bingo:
    """Bingo Solver"""

    def __init__(self, numbers: List[int], boards: List[np.ndarray]):
        """

        Parameters
        ----------
        numbers: List[int]
            An array of integers that are drawn consecutively
        boards: List[np.ndarray]
            A set of boards each consisting of a nxn grid of numbers
        """
        self.numbers = numbers
        self.boards = boards

        self.row_sums = None
        self.col_sums = None
        self.all_nums = None

    def prepare_boards(self) -> NoReturn:
        """
        This method creates metadata about the Bingo boards that are crucial
        for the searching strategy

        Returns
        -------
        NoReturn
        """
        # row sums for each board
        self.row_sums = [b.sum(axis=1) for b in self.boards]
        # column sums for each board
        self.col_sums = [b.sum(axis=0) for b in self.boards]
        # all distinct number for each board
        self.all_nums = [set(b.flatten()) for b in self.boards]

    def search_board(self, value: int, board_id: int) -> Union[None, int]:
        """
        Searches within the board for a given value. If the value is present
        it reduces to row and column sum for the given board.
        If to column or row sums becomes zero, then we have a winner board.

        Parameters
        ----------
        value: int
            The search value.
        board_id: int
            The board ID

        Returns
        -------
        Union[None, int]
            If we have a winner then it returns the board ID. Otherwise it
            returns None
        """

        if value in self.all_nums[board_id]:
            indexes = (self.boards[board_id] == value).nonzero()

            for row, col in np.asarray(indexes).T:
                self.row_sums[board_id][row] -= value
                self.col_sums[board_id][col] -= value

                if self.row_sums[board_id][row] == 0 or \
                        self.col_sums[board_id][col] == 0:
                    return board_id

        return None

    def run_win_first_strategy(self) -> Dict[str, any]:
        """
        If all numbers in any row or any column of a board are marked,
        that board wins. (Diagonals don't count.)

        Returns
        -------
        Dict[str, any]
            The winning meta
        """
        self.prepare_boards()

        out = dict(
            values_used=[],
            board_id=None,
            board=None,
            remaining=None,
            winning_value=None,
            score=None)

        for value in self.numbers:
            out['values_used'].append(value)

            for board_id in range(len(self.boards)):
                board_id = self.search_board(value, board_id)
                if board_id is None:
                    continue
                else:
                    remaining = self.row_sums[board_id].sum()
                    out['board_id'] = board_id
                    out['board'] = self.boards[board_id]
                    out['remaining'] = self.row_sums[board_id].sum()
                    out['winning_value'] = value
                    out['score'] = out['remaining'] * out['winning_value']

                    return out

        return out

    def run_win_last_strategy(self) -> Dict[str, any]:
        """
        This method figures out which board will win last and choose that one

        Returns
        -------
        Dict[str, any]
            The winning meta
        """
        self.prepare_boards()

        out = dict(
            values_used=[],
            board_id=None,
            board=None,
            remaining=None,
            winning_value=None,
            score=None)

        already_won = []

        for value in self.numbers:
            if len(already_won) == len(self.boards):
                break

            out['values_used'].append(value)

            for board_id in range(len(self.boards)):
                if board_id in already_won:
                    continue

                board_id = self.search_board(value, board_id)
                if board_id is None:
                    continue
                else:
                    already_won.append(board_id)

        last_winner = already_won[-1]

        remaining = self.row_sums[last_winner].sum()
        out['board_id'] = last_winner
        out['board'] = self.boards[last_winner]
        out['remaining'] = self.row_sums[last_winner].sum()
        out['winning_value'] = out['values_used'][-1]
        out['score'] = out['remaining'] * out['winning_value']

        return out


def main():
    """
    Loads the data and runs both stategies

    Returns
    -------
    NoReturn
    """
    path = DATA_DIR.joinpath('day4.txt')
    with open(path, 'r') as f:
        lines = f.readlines()

    inputs = list(map(int, lines[0].strip().split(',')))
    boards = list()

    for chunk in chunked(lines[1:], n=6):
        # takes into account the empty lines between the boards
        board = np.asarray([s.strip().split() for s in chunk[1:]], dtype=int)
        boards.append(board)

    bingo = Bingo(inputs, boards)
    result1 = bingo.run_win_first_strategy()
    print('First strategy')
    print(result1)

    result2 = bingo.run_win_last_strategy()
    print('Second strategy')
    print(result2)


if __name__ == "__main__":
    main()
