# configwizard

configwizard is a Python package for handling configuration files. It provides a `Config` class that allows you to easily create, read, update, and delete configuration files in different formats such as JSON and TOML.

# [Changelog](./Changelog.md)

## Installation

You can install configwizard using pip:

```bash
pip install configwizard
```

## Usage
Here's an example of how to use configwizard:

```python
from configwizard import Config

# Create a new configuration file
config = Config('config', 'json')

# Add content to the configuration file
config.add_content({'key': 'value'})

# Get the contents of the configuration file
contents = config.get_content()
print(contents)  # Output: {'key': 'value'}

# Update the contents of the configuration file
config.update_content({'key2': 'value2'})

# Get the updated contents
contents = config.get_content()
print(contents)  # Output: {'key': 'value', 'key2': 'value2'}

# Destroy the configuration file
config.destroy_config()
```

In the example above, we create a Config instance with a file name of 'config' and a file type of 'json'. We then add content to the configuration file using the add_content method and retrieve the contents using the get_content method. We update the contents with new values using the update_content method and finally destroy the configuration file with the destroy_config method.

## Supported File Types

configwizard supports the following file types for configuration files:

- JSON (.json)
- TOML (.toml)

When creating a Config instance, make sure to provide the appropriate file type.

## License

This project is licensed under the MIT License. See the __LICENSE__ file for more information.