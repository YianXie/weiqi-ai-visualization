class CoordinateHelper:
    """A class that helps to solve coordinate issues"""

    GTP_LETTERS = "ABCDEFGHJKLMNOPQRST"  # I is skipped

    def __init__(self) -> None:
        pass

    def convert_to_gtp(self, row: int, col: int):
        """A method that convert row-col coordinate system to GTP format

        Args:
            row (int): the row (x)-coordinate
            col (int): the col (y)-coordinate
        """
        return (
            f"{self.GTP_LETTERS[row]}{col + 1}"  # GTP uses 1-based indexing for columns
        )

    def convert_to_row_col(self, value: str):
        """A method that convert GTP format coordinates to row-col

        Args:
            value (str): the gtp-formatted coordinates
        """
        return (
            self.GTP_LETTERS.index(value[0]),
            int(value[1:]),
        )

    def convert_to_pygame(self, height: int, x: int, y: int):
        """A method that converts normal coords to pygame format (top left as origin)

        Args:
            board_size (int): the height of the pygame screen
            row (int): the x-coord
            col (int): the y-coord

        Returns:
            tuple: (x, y)
        """
        return (x, height - y)
