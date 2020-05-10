from builtins import bytes
import base64
import collections
import copy
import hashlib
import hmac
import random
import re
import time


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
