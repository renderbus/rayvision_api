"""The utils function of the rayvision api."""

# import built-in models
from builtins import bytes
import base64
import collections
import copy
import hashlib
import hmac
import platform
import random
import re
import time
import os
import json
import codecs
import sys

from .exception import RayvisionError, UploadFileNotSupportError

VERSION = sys.version_info[0]


def generate_timestamp():
    """str: The timestamp."""
    return str(int(time.time()))


def generate_nonce():
    """Generate random Numbers for verification."""
    return str(random.randrange(100000, 999999))


def generate_signature(key, msg):
    """Generate a signature string.

    First use the sha256 algorithm to calculate the summary of the msg
    hashed key and then use the base64 algorithm to get the signature
    string.

    Args:
        key (str): String added to the processing.
        msg (str): Source string.

    Returns:
        str: Decoded string.

    """
    hash_obj = hmac.new(bytes(key, encoding='utf8'),
                        msg=bytes(msg, encoding='utf8'),
                        digestmod=hashlib.sha256)
    return base64.b64encode(hash_obj.digest())


def generate_headers_body_str(domain_name, api_url, header, body):
    """Generate formatted strings.

    Based on header and body for generating signatures (signature and
    Content-Type do not participate in signatures).

    Format is Request Method + Domain Name + API URI + Request String.

    Args:
        domain_name (str): Domain name.
        api_url (str): Requested path.
        header (dict): Request header.
            e.g.:
                {
                  'accessId': 'xxx',
                  'channel': '4',
                  'platform': '2',
                  'UTCTimestamp': '32166266',
                  'nonce': '1465',
                  'signature': '',
                  'version': '1.0.0',
                  'Content-Type': 'application/json',
                }

            e.g.:
                {
                    'accessId': 'xxx',
                    'channel': '4',
                    'platform': '2',
                    'UTCTimestamp': '32166266',
                    'nonce': '1465',
                    'signature': '',
                    'version': '1.0.0',
                    'Content-Type': 'application/json'
                }
        body (dict): Request body.

    Returns:
        str: Stitched string.

    """
    header = copy.deepcopy(header)
    body = copy.deepcopy(body)
    try:
        header.pop('signature')
        header.pop('Content-Type')
    except KeyError:
        pass

    header_body_dict = headers_body_sort(header, body)
    header_body_list = [
        '{0}={1}'.format(key, value)
        for key, value in header_body_dict.items()
    ]
    result_str = '[POST]{domain_name}:{api_url}&{header_body_str}'.format(
        domain_name=domain_name,
        api_url=api_url,
        header_body_str='&'.join(header_body_list)
    )
    return result_str


def headers_body_sort(header, body):
    """Generate a new processed dictionary.

    The http request header and request parameters are sorted in
    ascending order by the lexicographic order (ASCII) of the parameter
    names.

    Args:
        header (dict): Request header.
            e.g.:
                {
                    'accessId': 'xxx',
                    'channel': '4',
                    'platform': '2',
                    'UTCTimestamp': '32166266',
                    'nonce': '1465',
                    'signature': '',
                    'version': '1.0.0',
                    'Content-Type': 'application/json'
                }
        body (dict): Request body.

    Returns:
        dict: Ordered dictionary object after request header and
            request parameters are sorted.

    """
    copy_header = copy.deepcopy(header)
    body = copy.deepcopy(body)
    copy_header.update(body)
    new_header = formatted_headers(copy_header)
    sorted_key_list = sorted(new_header)
    new_dict = collections.OrderedDict()
    for key in sorted_key_list:
        new_dict[key] = new_header[key]
    return new_dict


def formatted_headers(headers):
    """Please formatted dictionary.

    Possible data types in the dictionary: numbers.Number, str, bytes,
    list, dict, None (json's key can only be string, json's value may
    be number, string, logical value, array, object, null).

    Args:
        headers (dict): The headers of the ``Post``.
            e.g.:
              {
               "taksId": "2",
               "renderEnvs": [
                 {
                   "envId": 1,
                    "pluginIds": [2, 3, 4]
                 },
                 {
                   "envId": 3,
                    "pluginIds": [7, 8, 10]
                 }
               ]

    Returns:
        dict: Handled request header.

    """
    new_header = {}

    def _format_dict(header, key=None):
        """Format request header.

        Args:
            header (dict): Request header.
            key (str, optional): If the key is None, the value is the source
                dictionary object.

        Example:
            header = {
                'accessId': '',
                'channel': '4',
                'platform': '',
                'UTCTimestamp': '',
                'nonce': '',
                'signature': '',
                'version': '1.0.0',
                'Content-Type': 'application/json'
            }

        """
        if isinstance(header, dict):
            for key_new_part, value in header.items():
                if not key:
                    new_key = key_new_part
                else:
                    new_key = '{0}.{1}'.format(key, key_new_part)
                _format_dict(value, new_key)

        elif isinstance(header, list):
            for index, value in enumerate(header):
                new_key = '{0}{1}'.format(key, index)
                _format_dict(value, new_key)
        else:
            new_header[key] = header

    _format_dict(headers)

    return new_header


def hump2underline(hump_str):
    """Convert the hump name to a snake shape.

    Args:
        hump_str (str): The name to be converted.

    Returns:
        str: Convert to a snake-like name.

    """
    # https://regex101.com/r/xZYoLp/1
    patt = re.compile(r'([a-z]|\d)([A-Z])')
    underline_str = re.sub(patt, r'\1_\2', hump_str).lower()
    return underline_str


def get_os():
    """Get system name.

    Returns:
        str: The system/OS name.
            e.g.:
                ``Linux`` or ``Windows``.

    """
    return platform.system().lower()


def to_bytes(string):
    """Convert string to bytes type."""
    if isinstance(string, str):
        string = string.encode('utf-8')
    return string


def assemble_api_url(domain, operators, protocol='https'):
    """Assemble the requests api url."""
    return '{}://{}{}'.format(protocol, domain, operators)


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


def convert_path(path):
    """Convert to the path the server will accept.

    Args:
        path (str): Local file path.
            e.g.:
                "D:/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    Returns:
        str: Path to the server.
            e.g.:
                "/D/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    """
    lower_path = path.replace('\\', '/')
    if lower_path[1] == ":":
        path_lower = lower_path.replace(":", "")
        path_server = "/" + path_lower
    else:
        path_server = lower_path[1:]

    return path_server


def check_and_read(json_path):
    files_paths = json_path.replace("\\", "/")
    if not os.path.exists(files_paths):
        raise RayvisionError(1000004, "{} is not found".format(files_paths))
    return json_load(files_paths)


def update_task_info(update_info, task_path):
    """Update the task Settings.

    Args:
        update_info (dict): Information that needs to be updated.
        task_path ( str or dict): task.json absolute path or dict info.
    """
    task_info = check_and_read(task_path)
    for update_key in update_info.keys():
        if update_key not in task_info.get("task_info"):
            raise RayvisionError(1000002,
                                 "{} does not exist in the task setting and cannot be updated".format(update_key))

    task_info["task_info"].update(update_info)
    json_save(task_path, task_info)


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


def exists_or_create(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return os.path.exists(folder)
