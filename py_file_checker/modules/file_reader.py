class FileReader:
    """Class that reads the file
    """

    def __init__(self, filepath: str) -> None:
        """Class initialization

        Args:
            filepath (str): filepath
        """
        self.__filepath = filepath

    def read(self) -> str:
        """Reads the file and returns the content of the file

        Returns:
            str: The value of the read file
        """
        with open(self.__filepath, "r", encoding="utf-8") as file:
            return file.read()
