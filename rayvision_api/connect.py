"""Request, request header and request result processing."""

import copy
import json
import logging
from pprint import pformat

import requests
from tenacity import retry
from tenacity import stop_after_attempt, wait_random

from rayvision_api import utils
from rayvision_api.constants import HEADERS
from rayvision_api.exception import RayvisionAPIError


class Connect(object):
    """Connect operation with the server, request."""

    def __init__(self, access_id, access_key, protocol, domain, platform,
                 headers=None):
        """Connect parameter initialization.

        Args:
            access_id (str): The access id of API.
            access_key (str): The access key of the API.
            domain (str, optional): The domain address of the API.
            platform (str, optional): The platform of renderFarm.
            protocol (str, optional): The requests protocol.

        """
        self.logger = logging.getLogger(__name__)
        self.domain = domain
        self._access_key = access_key
        # Example: https://task.renderbus.com
        self._protocol = protocol
        self._protocol_domain = '{0}://{1}'.format(protocol, self.domain)
        if headers:
            HEADERS.update(headers)
        self._headers = HEADERS
        self._headers['accessId'] = access_id
        self._headers['platform'] = platform

    @property
    def headers(self):
        """Get request headers dic."""
        return self._headers

    @staticmethod
    def assemble_api_url(domain, operators, protocol='https'):
        """Assemble the requests api url."""
        return '{}://{}{}'.format(protocol, domain, operators)

    @retry(reraise=True, stop=stop_after_attempt(5), wait=wait_random(min=1, max=2))
    def post(self, api_url, data=None):
        """Send an post request and return data object if no error occurred.

        Request processing through the decorator, if the request fails more
        than five times, then the exception is ran out.

        Args:
            api_url (str): The URL address of the corresponding action network
                Request.
                e.g.:
                    /api/render/common/queryPlatforms
                    /api/render/user/queryUserProfile
                    /api/render/user/queryUserSetting
            data (dict, optional): Request data.

        Returns:
            dict or List: Response data.

        Raises:
            RayVisionAPIError: The request failed, It returns the error ID,
                the error message, and the request address.

        """
        data = data or {}
        url = self.assemble_api_url(self.domain, api_url,
                                    protocol=self._protocol)
        headers = self._handle_headers(api_url, data)
        data = json.dumps(data)
        self.logger.debug('POST: %s', url)
        self.logger.debug('HTTP Headers: %s', pformat(headers))
        self.logger.debug('HTTP Body: %s', data)
        response = requests.post(url, data, headers=headers)
        json_response = response.json()
        self.logger.debug('HTTP Response: %s', json_response)
        code = json_response['code']
        if code != 200:
            raise RayvisionAPIError(code, json_response['message'],
                                    response.url)
        return json_response['data']

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
        headers['UTCTimestamp'] = utils.generate_timestamp()
        headers['nonce'] = utils.generate_nonce()
        msg = utils.generate_headers_body_str(self.domain, api_url,
                                              headers, data)
        headers['signature'] = utils.generate_signature(self._access_key, msg)
        return headers
