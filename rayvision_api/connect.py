"""Request, request header and request result processing."""

import copy
import functools
import json
import logging
from pprint import pformat
import time

import requests
from tenacity import retry
from tenacity import stop_after_attempt, wait_random

from rayvision_api.constants import HEADERS
from rayvision_api.exception import RayvisionAPIError
from rayvision_api import signature
from rayvision_api.validator import validate_data
from rayvision_api.url import ApiUrl
from rayvision_api.url import assemble_api_url


class Connect(object):
    """Connect operation with the server, request."""

    def __init__(self, access_id, access_key, protocol, domain, platform,
                 headers=None, session=None):
        """Connect parameter initialization.

        Args:
            access_id (str): The access id of API.
            access_key (str): The access key of the API.
            domain (str, optional): The domain address of the API.
            platform (str, optional): The platform of renderFarm.
            protocol (str, optional): The requests protocol.
            session (requests.Session, optional): The session of the requests
                instance.

        """
        self.logger = logging.getLogger(__name__)
        self.url = ApiUrl
        self.domain = domain
        self.platform = platform
        self._access_key = access_key
        # Example: https://task.renderbus.com
        self._protocol = protocol
        self._protocol_domain = '{0}://{1}'.format(protocol, self.domain)
        if headers:
            HEADERS.update(headers)
        self._headers = HEADERS
        self._headers['accessId'] = access_id
        self._session_request = session or requests.Session()
        self._headers['platform'] = self.platform

    @property
    def headers(self):
        """Get request headers dic."""
        return self._headers

    @retry(reraise=True, stop=stop_after_attempt(5),
           wait=wait_random(min=1, max=2))
    def post(self, api_url, data=None, validator=True):
        """Send an post request and return data object if no error occurred.

        Request processing through the decorator, if the request fails more
        than five times, then the exception is ran out.

        Args:
            api_url (rayvision_api.api.url.URL or str): The URL address of the
                corresponding action network Request.
                    e.g.:
                        /api/render/common/queryPlatforms
                        /api/render/user/queryUserProfile
                        /api/render/user/queryUserSetting
            data (dict, optional): Request data.
            validator (bool, optional): Validator the data.

        Returns:
            dict or List: Response data.

        Raises:
            RayVisionAPIError: The request failed, It returns the error ID,
                the error message, and the request address.

        """
        data = data or {}
        schema_name = api_url.split("/")[-1]
        if validator:
            data = validate_data(data, schema_name)
        request_address = assemble_api_url(self.domain, api_url,
                                           protocol=self._protocol)
        headers = self._handle_headers(api_url, data)
        data = json.dumps(data)
        self.logger.debug('POST: %s', request_address)
        self.logger.debug('HTTP Headers: %s', pformat(headers))
        self.logger.debug('HTTP Body: %s', data)
        response = self._session_request.post(request_address, data, headers=headers)
        json_response = response.json()
        self.logger.debug('HTTP Response: %s', json_response)
        code = json_response["code"]
        if code != 200:
            raise RayvisionAPIError(code, json_response['message'],
                                    response.url)
        return json_response["data"]

    def _handle_headers(self, api_url, data):
        """Add the necessary parameters to the request header.

        Args:
            api_url (str): The api url.
            data (dict): Request data.

        Returns:
            dict: The headers information of the request.
                e.g.:
                    {
                        'accessId': 'xxx',
                        'channel': '4',
                        'platform': '2',
                        'UTCTimestamp': '32166266',
                        'nonce': '1465',
                        'signature': 'af465a4f6agfasgfafa45',
                        'version': '1.0.0',
                        'Content-Type': 'application/json'
                    }

        """
        headers = copy.deepcopy(self._headers)
        headers['UTCTimestamp'] = str(int(time.time()))
        headers['nonce'] = signature.generate_nonce()
        msg = signature.generate_headers_body_str(self.domain, api_url,
                                                  headers, data)
        headers['signature'] = signature.generate_signature(self._access_key,
                                                            msg)
        return headers
