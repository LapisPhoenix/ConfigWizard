import os   # For file system operations
import json  # For JSON loading/dumping
import tomllib  # For TOML loading
import base64  # For base64, 32, 16 encoding
import binascii  # For hex encoding
import tomli_w  # For TOML writing


class Config:
    """
    Config class for handling configuration files.

    Args:
        file_name (str): The name of the configuration file.
        file_type (str): The type of the configuration file (e.g., 'json', 'toml').
        default_directory (str, optional): The default directory to store the configuration file.
                                            Defaults to the current working directory.

    Raises:
        ValueError: If the file type is not supported.

    Attributes:
        ACCEPTED_CONFIG_TYPES (list): The accepted configuration file types.

    Methods:
        add_content: Add contents to the configuration file.
        get_content: Get the contents of the configuration file.
        remove_content: Remove values from the configuration file.
        update_content: Update the contents of the configuration file with new values or delete values.
        destroy_config: Destroy the configuration file by removing it from the file system.
        encode_config: Encode the configuration file in memory.

    """
    def __init__(self, file_name: str, file_type: str, default_directory: str = None):
        """
        Initialize a Config instance.

        Args:
            file_name (str): The name of the configuration file.
            file_type (str): The type of the configuration file (e.g., 'json', 'toml').
            default_directory (str, optional): The default directory to store the configuration file.
                                                Defaults to the current working directory.

        Raises:
            ValueError: If the file type is not supported.

        """
        self.config_name = file_name
        self.file_type = file_type
        self.default_directory = default_directory or os.getcwd()
        self.ACCEPTED_CONFIG_TYPES = ['json', 'toml']

        if not any(config_type.lower() in file_type.lower() for config_type in self.ACCEPTED_CONFIG_TYPES):
            raise ValueError(f"Config File must contain one of these types: {', '.join(self.ACCEPTED_CONFIG_TYPES)}!")

        self._check_file_type()

        self.file_path = os.path.join(self.default_directory, self.config_name + self.file_type)

        if not os.path.exists(self.default_directory):
            os.makedirs(self.default_directory)

        if not os.path.exists(self.file_path):
            self.add_content({})

    def _check_file_type(self):
        if '.' not in self.file_type:
            new = '.' + self.file_type

            self.file_type = new

    def add_content(self, contents):
        """
        Add contents to the configuration file.

        Args:
            contents (dict): The contents to be added to the configuration file.

        Raises:
            ValueError: If the contents are not valid TOML code for TOML files.

        """
        if self.file_type == '.json':
            with open(self.file_path, 'w') as f:
                json.dump(contents, f)
        elif self.file_type == '.toml':
            with open(self.file_path, 'wb') as f:
                # Convert the contents dictionary to a string representation
                contents_str = tomli_w.dumps(contents)

                # Check if the contents are valid TOML
                try:
                    tomllib.loads(contents_str)
                except tomllib.TOMLDecodeError:
                    raise ValueError("The following is not valid TOML code:\n" + contents_str)
                # Convert the string representation to bytes
                contents_bytes = contents_str.encode('utf-8')

                # Write the contents to the file
                f.write(contents_bytes)

    def get_content(self):
        """
        Get the contents of the configuration file.

        Returns:
            dict: The contents of the configuration file.

        """
        if not os.path.exists(self.file_path):
            return {}

        with open(self.file_path, 'rb') as f:
            if self.file_type == '.json':
                return json.load(f)
            elif self.file_type == '.toml':
                # Convert the binary contents to a string
                contents_bytes = f.read()
                contents_str = contents_bytes.decode('utf-8')

                return tomllib.loads(contents_str)

    def remove_content(self, remove_values: list):
        """
        Remove values from the configuration file.

        Args:
            remove_values (list): The values to remove from the configuration file.

        """
        file_contents = self.get_content()

        for value in remove_values:
            if value in file_contents:
                del file_contents[value]

        self.add_content(file_contents)

    def update_content(self, new_values: dict, remove_values: list = None):
        """
        Update the contents of the configuration file with new values.

        Args:
            new_values (dict): The new values to update the configuration file.
            remove_values (list, optional): The values to remove from the configuration file.

        Raises:
            ValueError: If the new values are not in dictionary format.

        """
        if not isinstance(new_values, dict):
            raise ValueError("New values must be in dictionary format!")

        if not isinstance(remove_values, list):
            remove_values = []

        file_contents = self.get_content()

        with open(self.file_path, 'w') as f:
            if self.file_type == '.json':
                file_contents.update(new_values)
                json.dump(file_contents, f, indent=2)
            elif self.file_type == '.toml':
                file_contents.update(new_values)
                self.add_content(file_contents)

        if remove_values:
            self.remove_content(remove_values)

    def destroy_config(self):
        """
        Destroy the configuration file by removing it from the file system.
        """
        os.remove(self.file_path)

    def __repr__(self):
        return f"Config({self.config_name}, {self.file_type}, {self.default_directory})"

    def __str__(self):
        return f"Config({self.config_name}, {self.file_type}, {self.default_directory})"

    def encode_config(self, type_of_encoding: str):
        """
        Encode the configuration file in memory.

        Args:
            type_of_encoding (str): The type of codec to use to encode the configuration file.
                                    Must be one of the following: 'base64', 'hex', 'base32', 'base16'

        Returns:
            The encoded configuration file in memory.

        """

        accepted_types = ['base64', 'hex', 'base32', 'base16']

        if type_of_encoding.casefold() not in accepted_types:
            raise ValueError(f"Encoding type must be one of the following: {', '.join(accepted_types)}")

        with open(self.file_path, 'rb') as f:
            contents = f.read()

            if type_of_encoding == 'base64':
                contents = base64.b64encode(contents).decode('utf-8')
            elif type_of_encoding == 'hex':
                contents = contents.hex()
            elif type_of_encoding == 'base32':
                contents = base64.b32encode(contents).decode('utf-8')
            elif type_of_encoding == 'base16':
                contents = contents.hex().upper()

            return contents
