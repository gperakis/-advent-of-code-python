from typing import List, Optional

from more_itertools import windowed

from config import DATA_DIR

path = DATA_DIR.joinpath('day1.txt')


class Day01:
    def __init__(self):
        self.path = DATA_DIR.joinpath('day1.txt')
        self.dataset_: Optional[List[int]] = None

    @property
    def dataset(self) -> List[int]:
        """
        Reads the dataset and transforms the strings into integers

        Returns
        -------
        List[int]
            An array of integers.
        """
        if self.dataset_ is None:
            with open(path, 'r') as f:
                self.dataset_ = [int(v.strip()) for v in f.readlines()]

        return self.dataset_

    def calculate_part1(self):
        """
        Counts the number of times a depth measurement increases from the
        previous measurement. (There is no measurement before the first
        measurement.)

        For example, the changes are as follows:
        199 (N/A - no previous measurement)
        200 (increased)
        208 (increased)
        210 (increased)
        200 (decreased)
        207 (increased)
        240 (increased)
        269 (increased)
        260 (decreased)
        263 (increased)

        In this example, there are 7 measurements that are larger than the
        previous measurement.

        Returns
        -------
        int
            The number of  measurements that are larger than the previous
            measurement.
        """
        counter = 0
        values = self.dataset

        for i, value in enumerate(values[1:]):
            if value > values[i]:
                counter += 1

        return counter

    def calculate_part2(self, n: int = 3, step: int = 1):
        """
        Calculates the number of times the sum of measurements in this sliding
        window increases from the previous sum. This is a generalization of
        the calculate_part1() method. Instead of using calculate_part1()
        you may use calculate_part2(n=1)

        Parameters
        ----------
        n: int
            The size of the sliding window for the passed iterable
        step: int
            The step to use for the sliding window. Default is 1.

        Returns
        -------
        int
            The number of times the sum of measurements in this sliding window
            increases from the previous sum
        """
        counter = 0
        previous_sum = sum(self.dataset[0: n])

        for t in windowed(self.dataset[1:], n):
            current_sum = sum(t)

            if current_sum > previous_sum:
                counter += 1

            previous_sum = current_sum

        return counter


if __name__ == "__main__":
    day01 = Day01()

    res01a = day01.calculate_part1()
    res01b = day01.calculate_part2(n=3)

    print(res01a)
    print(res01b)
