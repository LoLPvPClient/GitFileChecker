import configparser
from typing import List, Any


class ResourceConfigurationReader:
    """
    A utility class for reading and retrieving configuration options from a resource configuration (RC) file.
    """

    def __init__(self, rc_file: str) -> None:
        """
        Initializes the `ResourceConfigurationReader` with a given RC file.

        Args:
            rc_file (str): The path to the resource configuration file.
        """
        self.__config: configparser.ConfigParser = configparser.ConfigParser(
            allow_no_value=True)
        self.__config.read(rc_file)

    def get_config_options(self, section_name: str) -> List[str]:
        """
        Retrieves the options available in a specific section of the configuration file.

        Args:
            section_name (str): The name of the section in the configuration file.

        Returns:
            List[str]: A list of options in the specified section. Returns an empty list if the section does not exist.
        """
        try:
            return self.__config.options(section_name)
        except configparser.NoSectionError:
            return []

    def get_value_from_section(self, section_name: str, option_name: str, default_val: Any) -> Any:
        """
        Retrieves the value of a specific option from a section in the configuration file.

        Args:
            section_name (str): The name of the section in the configuration file.
            option_name (str): The name of the option whose value is to be retrieved.
            default_val (Any): The default value to return if the section or option is not found.

        Returns:
            Any: The value of the specified option, or the default value if the option or section does not exist.
        """
        return self.__config.get(section_name, option_name, fallback=default_val)
