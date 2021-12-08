from collections import Counter
from pprint import pprint
from typing import Optional, Dict, NoReturn

import numpy as np

from config import DATA_DIR


class SubMarineDiagnostic:
    def __init__(self, fname: Optional[str] = None):
        """

        Parameters
        ----------
        fname
        """
        self.fname = fname
        self.gamma_values = None
        self.binary_codes = None

    def prepare(self) -> NoReturn:
        """

        Parameters
        ----------
        fname

        Returns
        -------

        """
        if self.fname is None:
            path = DATA_DIR.joinpath('day3.txt')
        else:
            path = DATA_DIR.joinpath(self.fname)
        assert path.exists()

        binary_codes = []
        with open(path, 'r') as f:
            for i in f.readlines():
                binary_codes.append(list(i.strip()))

        binary_codes = np.asarray(binary_codes, dtype=int)
        threshold = binary_codes.shape[0] / 2
        self.gamma_values = (binary_codes.sum(axis=0) > threshold).astype(int)

        self.binary_codes = binary_codes

    @property
    def gamma_binary_str(self) -> str:
        """

        Returns
        -------

        """
        if self.gamma_values is None:
            self.prepare()

        return ''.join(list(self.gamma_values.astype(str)))

    @property
    def epsilon_binary_str(self) -> str:
        """

        Returns
        -------

        """
        if self.gamma_values is None:
            self.prepare()

        epsilon = (1 - self.gamma_values)

        return ''.join(list(epsilon.astype(str)))

    @property
    def gamma(self) -> int:
        """

        Returns
        -------

        """
        return int(self.gamma_binary_str, 2)

    @property
    def epsilon(self) -> int:
        """

        Returns
        -------

        """
        return int(self.epsilon_binary_str, 2)

    @property
    def power_consumption(self) -> int:
        """

        Returns
        -------

        """
        return self.gamma * self.epsilon

    @property
    def oxygen_generator_rating(self) -> int:
        if self.binary_codes is None:
            self.prepare()

        codes = self.binary_codes

        for i in range(self.binary_codes.shape[1]):
            if codes.shape[0] == 1:
                break

            cs = Counter(codes[:, i])
            most_common_value = 1 if cs.get(1, 0) >= cs.get(0, 0) else 0
            codes = codes[codes[:, i] == most_common_value]

        ogr_str = ''.join(codes.flatten().astype(str))
        return int(ogr_str, 2)

    @property
    def co2_scrubber_rating(self) -> int:
        if self.binary_codes is None:
            self.prepare()

        codes = self.binary_codes

        for i in range(self.binary_codes.shape[1]):
            if codes.shape[0] == 1:
                break

            cs = Counter(codes[:, i])
            least_common_value = 1 if cs.get(1, 0) < cs.get(0, 0) else 0
            codes = codes[codes[:, i] == least_common_value]

        co2_rating_str = ''.join(codes.flatten().astype(str))
        return int(co2_rating_str, 2)

    @property
    def life_support_rating(self):
        """

        Returns
        -------

        """
        return self.oxygen_generator_rating * self.co2_scrubber_rating

    def report(self) -> Dict[str, int]:
        return dict(
            gamma=self.gamma,
            epsilon=self.epsilon,
            power_consumption=self.power_consumption,
            oxygen_generator_rating=self.oxygen_generator_rating,
            co2_scrubber_rating=self.co2_scrubber_rating,
            life_support_rating=self.life_support_rating
        )


if __name__ == "__main__":
    diagnostic = SubMarineDiagnostic()
    res = diagnostic.report()
    pprint(res)
