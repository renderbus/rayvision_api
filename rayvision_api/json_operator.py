#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import codecs
import json
import os
import sys

from rayvision_api.exception import RayvisionError
from rayvision_api.paths import convert_path

VERSION = sys.version_info[0]


def json_load(json_path, encoding='utf-8'):
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
    if os.path.exists(json_path):
        with codecs.open(json_path, 'r', encoding=encoding) as f_json:
            data = json.load(f_json)

        return data


def json_save(json_path, data, encoding='utf-8', ensure_ascii=True):
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
    with codecs.open(json_path, 'w', encoding=encoding) as f_json:
        if VERSION == 3:
            json.dump(data, f_json, ensure_ascii=ensure_ascii, indent=2)
        else:
            f_json.write(str(json.dumps(data, ensure_ascii=ensure_ascii,
                                        indent=2)))


def check_upload_file(file_path, upload_info):
    """Check that the file is already in the upload list.

    Args:
        file_path (str): File path.
        upload_info (dict): Upload json info.

    Returns:
        bool.

    """
    for one_file in upload_info.get("asset"):
        if one_file["local"] == file_path:
            return True
    return False


def check_and_read(json_path):
    files_paths = json_path.replace("\\", "/")
    if not os.path.exists(files_paths):
        raise RayvisionError(1000004, "{} is not found".format(files_paths))
    return json_load(files_paths)


def append_to_task(additional_info, task_path, cover=True):
    """Add new field information in task_info.

    Args:
        additional_info (dict): Information that needs to be added
        cover (bool): If the added field already exists, whether to overwrite it,
            The default is overwrite.

    """
    task_info = check_and_read(task_path)
    task_append_info = task_info.get("additional_info", {})
    if not cover:
        for append_key in additional_info:
            if append_key in task_append_info.keys():
                raise RayvisionError(1000002, "{} already exists, cannot be added".format(append_key))
    else:
        task_append_info.update(additional_info)
        task_info["additional_info"] = task_append_info

    json_save(task_path, task_info)


def check_upload_file(file_path, upload_info):
    """Check that the file is already in the upload list.

    Args:
        file_path (str): File path.
        upload_info (dict): Upload json info.

    Returns:
        bool.

    """
    for one_file in upload_info.get("asset"):
        if one_file["local"] == file_path:
            return True
    return False


def append_to_upload(files_paths, upload_path):
    """Add the asset information you need to upload to upload_info.

    Args:
        files_paths (str or list): You need to add the uploaded asset path.
        upload_path (str): Upload json path.

    """
    upload_info = check_and_read(upload_path)
    if isinstance(files_paths, str):
        files_paths = files_paths.replace("\\", "/")
        if not os.path.exists(files_paths):
            raise RayvisionError(1000004, "{} is not found".format(files_paths))

        status = check_upload_file(files_paths, upload_info)
        if status:
            return

        upload_info["asset"].append(
            {
                "local": files_paths.replace("\\", "/"),
                "server": convert_path(files_paths),
            },
        )
    elif isinstance(files_paths, list):
        for files_path in files_paths:
            files_path = files_path.replace("\\", "/")
            if not os.path.exists(files_path):
                raise RayvisionError(1000004,
                                     "{} is not found".format(files_path))

            status = check_upload_file(files_path, upload_info)
            if status:
                continue

            upload_info["asset"].append({
                "local": files_path.replace("\\", "/"),
                "server": convert_path(files_path),
            })
    else:
        raise RayvisionError(1000003, "files_paths must be a str or list.".format(files_paths))

    json_save(upload_path, upload_info)
