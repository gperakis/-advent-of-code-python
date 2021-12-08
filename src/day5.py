from collections import defaultdict

from config import DATA_DIR


class HydrothermalVentureScanner:
    def __init__(self):
        self.path = DATA_DIR.joinpath('day5.txt')

    def scan(self, include_diagonal: bool = False) -> int:
        """

        Parameters
        ----------
        include_diagonal

        Returns
        -------

        """
        coordinates = defaultdict(int)

        with open(self.path, 'r') as f:

            for line in f.readlines():
                point1, point2 = line.split(' -> ')
                x1, y1 = list(map(int, point1.split(',')))
                x2, y2 = list(map(int, point2.split(',')))

                if not include_diagonal:
                    if x1 != x2 and y1 != y2:
                        continue

                while x1 != x2 or y1 != y2:
                    coordinates[(x1, y1)] += 1

                    if x1 < x2:
                        x1 += 1

                    if x1 > x2:
                        x1 -= 1

                    if y1 < y2:
                        y1 += 1

                    if y1 > y2:
                        y1 -= 1

                coordinates[(x1, y1)] += 1

        return sum([1 for i in coordinates.values() if i > 1])


if __name__ == "__main__":
    scanner = HydrothermalVentureScanner()
    print(scanner.scan(include_diagonal=False))
    print(scanner.scan(include_diagonal=True))
