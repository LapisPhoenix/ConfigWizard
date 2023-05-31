import os
import json
import tomllib
import tomli_w


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
        update_content: Update the contents of the configuration file with new values.
        destroy_config: Destroy the configuration file by removing it from the file system.

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

    def update_content(self, new_values: dict):
        """
        Update the contents of the configuration file with new values.

        Args:
            new_values (dict): The new values to update the configuration file.

        Raises:
            ValueError: If the new values are not in dictionary format.

        """
        if not isinstance(new_values, dict):
            raise ValueError("New Values must be in a dict format!")

        file_contents = self.get_content()

        with open(self.file_path, 'w') as f:
            if self.file_type == '.json':
                file_contents.update(new_values)
                json.dump(file_contents, f, indent=2)
            elif self.file_type == '.toml':
                file_contents.update(new_values)
                self.add_content(file_contents)

    def destroy_config(self):
        """
        Destroy the configuration file by removing it from the file system.
        """
        os.remove(self.file_path)


if __name__ == '__main__':
    test_file = Config('test', '')
    test_file.add_content({'test': 'test'})
    print(test_file.get_content())
    test_file.update_content({'test2': 'test2'})
    print(test_file.get_content())
    test_file.destroy_config()
