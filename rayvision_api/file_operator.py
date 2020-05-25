"""Provide file operator functions."""

# Import built-in modules
import codecs
import json

# Import third-party modules
import yaml


def read_yaml(file_path):
    """Read a YAML file by the given path.

    Args:
        file_path (str): The absolute path of the YAML file.

    Returns:
        dict: The data spec_reader from given YAML file.

    """
    with open(file_path, "r") as file_object:
        return yaml.safe_load(file_object)


def write_yaml(file_path, data):
    """Write data into the YAML file by the given data and file path.

    Args:
        file_path (str): The absolute path of the YAML file.
        data (dict): The data want to write.

    """
    with open(file_path, "w") as file_object:
        yaml.dump(data, file_object)


def write_json(json_path, data, encoding='utf-8', ensure_ascii=True):
    """Will save to the json file according to the specified encoded data.

    Args:
        json_path (str): Json file path.
        data (dict): Asset information data.
            e.g.:
                {
                    "scene_info": {
                        "defaultRenderLayer":{
                            "renderable": "1",
                            "is_default_camera": "1",
                        }
                    }
                }
        encoding (str): Encoding, default is ``utf-8``.
        ensure_ascii (bool): Whether to ignore the error, default ``True``.

    """
    with codecs.open(json_path, "w", encoding=encoding) as f_json:
        json.dump(data, f_json, ensure_ascii=ensure_ascii, indent=2)


def read_load(json_path, encoding='utf-8'):
    """Load the data from the json file.

    Args:
        json_path (str): Json file path.
        encoding (str): Encoding, default is ``utf-8``.

    Returns:
        dict: Data in the json file.
            e.g.:
                {
                    "task_info"
                }

    """
    with codecs.open(json_path, "r", encoding=encoding) as f_json:
        return json.load(f_json)
