from typing import Optional, NoReturn, List, Tuple

from config import DATA_DIR


class SubMarine:
    """
    Abstract class that sets the basic API of all the Sub-marines.
    """

    def __init__(self):
        self.horizontal = 0
        self.vertical = 0

    def reset(self) -> NoReturn:
        """
        This method resets the horizontal and vertical positions

        Returns
        -------
        NoReturn
        """
        self.vertical = 0
        self.horizontal = 0

    def up(self, units: int = 0) -> int:
        raise NotImplementedError()

    def down(self, units: int = 0) -> int:
        raise NotImplementedError()

    def forward(self, units: int = 0) -> int:
        raise NotImplementedError()

    @staticmethod
    def load_instructions(fname: Optional[str] = None) -> List[
        Tuple[str, int]]:
        """
        This method loads a file with instructions for the navigation of the
        Sub-marine. The file in each row must have an action and the units.
        For example:
        up 9
        down 7
        forward 2
        down 3

        Parameters
        ----------
        fname: Optional[str]
            The filename that will be used as navigation instructions. Must be
            located in the `data` directory. If None, it uses the default
            file. Default is None.

        Returns
        -------
        List[Tuple[str, int]]
            The navigation instructions as an array of tuples.
        """
        if fname is None:
            path = DATA_DIR.joinpath('day2.txt')
        else:
            path = DATA_DIR.joinpath(fname)
        assert path.exists()

        instructions = []
        with open(path, 'r') as f:
            for i in f.readlines():
                action, value = i.strip().split()
                instructions.append((action, int(value)))

        return instructions

    def navigate(self, fname: Optional[str] = None) -> Tuple[int, int, int]:
        """
        Navigates the SubMarine based on an instructions file. The file must
        be located in the data directory of the project.

        Parameters
        ----------
        fname: Optional[]

        Returns
        -------
         Tuple[int, int, int]
        """
        self.reset()
        instructions = self.load_instructions(fname)

        for action, units in instructions:
            getattr(self, action)(units)

        return self.horizontal, self.vertical, self.horizontal * self.vertical


class SubMarineTypeA(SubMarine):
    def __init__(self):
        super().__init__()

    def up(self, units: int = 0) -> int:
        """
        Decreases the depth by X units

        Parameters
        ----------
        units: int
            The units to decrease. If 0 is passed it show the current vertical.
            Default is 0.

        Returns
        -------
        int
            The current depth (vertical position)
        """
        self.vertical -= units

        return self.vertical

    def down(self, units: int = 0) -> int:
        """
        Increases the depth by X units

        Parameters
        ----------
        units: int
            The units to increase. If 0 is passed it show the current vertical.
            Default is 0.

        Returns
        -------
        int
            The current depth (vertical position)
        """
        self.vertical += units

        return self.vertical

    def forward(self, units: int = 0) -> int:
        """
        Increases the horizontal position by X units.

        Parameters
        ----------
         units: int
            The units to increase. If 0 is passed it show the current
            horizontal position. Default is 0.

        Returns
        -------
        int
            The current horizontal position
        """
        self.horizontal += units

        return self.horizontal


class SubMarineTypeB(SubMarine):
    def __init__(self):
        super().__init__()

        self.aim = 0

    def up(self, units: int = 0):
        """
        Decreases the aim by X units

        Parameters
        ----------
        units: int
            The units to decrease. If 0 is passed it show the current
            aim position. Default is 0.

        Returns
        -------
        int
            The current aim position
        """
        self.aim -= units

        return self.aim

    def down(self, units: int = 0):
        """
        Increases the aim by X units

        Parameters
        ----------
        units: int
            The units to increase. If 0 is passed it show the current
            aim position. Default is 0.

        Returns
        -------
        int
            The current aim position
        """
        self.aim += units

        return self.aim

    def forward(self, units: int = 0):
        """
        Increases the horizontal position by X units.

        Parameters
        ----------
        units: int
            The units to increase. If 0 is passed it show the current
            aim position. Default is 0.

        Returns
        -------
        int
            The current horizontal position
        """
        self.horizontal += units
        self.vertical += self.aim * units

        return self.horizontal


if __name__ == "__main__":
    subA = SubMarineTypeA()
    resA = subA.navigate()
    print(resA)

    subB = SubMarineTypeB()
    resB = subB.navigate()
    print(resB)

    # subB.forward(5)
    # subB.down(5)
    # subB.forward(8)
    # subB.up(3)
    # subB.down(8)
    # subB.forward(2)
    # print(subB.depth)
    # print(subB.horizontal)
