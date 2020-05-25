"""The plugin of the pytest.

The pytest plugin hooks do not need to be imported into any test code, it will
load automatically when running pytest.

References:
    https://docs.pytest.org/en/2.7.3/plugins.html

"""
import os
import re
import sys

# pylint: disable=import-error
import pytest


@pytest.fixture(name='user_info_dict')
def user_info():
    """Get the user's login information."""
    return {
        'domain': 'task.renderbus.com',
        'platform': '2',
        'access_id': 'test_access_id',
        'access_key': 'test_access_key',
        'protocol': 'https'
    }


@pytest.fixture()
def mock_requests(requests_mock, user_info_dict):
    """Decorator, simulate the request, request API."""

    def _mock_requests(data):
        data_ = {
            'code': 200,
            'data': {},
            'message': 'There is no response',
        }
        data_.update(data)
        matcher = re.compile('.+{}.+'.format(user_info_dict['domain']))
        requests_mock.register_uri('POST', matcher, json=data_)

    return _mock_requests


@pytest.fixture()
def header():
    """Get the request header information."""
    return {
        'accessId': 'xxx',
        'channel': '4',
        'platform': '2',
        'UTCTimestamp': '32166266',
        'nonce': '1465',
        'version': 'dev',
    }


@pytest.fixture()
def task_info(tmpdir):
    """Get user info."""
    return {
        "domain": "task.renderbus.com",
        "platform": "2",
        "access_id": "df6d1d6s3dc56ds6",
        "access_key": "fa5sd565as2fd65",
        "local_os": 'windows',
        "workspace": "c:/workspace",
        "render_software": "Maya",
        "software_version": "2018",
        "project_name": "Project1",
        "plugin_config": {
            "mtoa": "3.1.2.1"
        },
        'cg_file': str(tmpdir.join('muti_layer_test.ma'))
    }


@pytest.fixture()
def render_env():
    """Get render environment information."""
    return {
        'cgId': 2000,
        'cgName': 'Maya',
        'cgVersion': '2018',
        'renderLayerType': 0,
        'editName': 'tests',
        'renderSystem': 1,
        'pluginIds': [2703]
    }


@pytest.fixture()
def rayvision_connect(user_info_dict):
    """Create connect API object."""
    from rayvision_api.connect import Connect
    user_info_dict['headers'] = {'version': 'dev'}
    return Connect(**user_info_dict)


@pytest.fixture()
def check(task, tmpdir):
    """Create an RayvisionCheck object."""
    from rayvision_api.task.check import RayvisionCheck
    if "win" in sys.platform.lower():
        os.environ["USERPROFILE"] = str(tmpdir)
    else:
        os.environ["HOME"] = str(tmpdir)
    return RayvisionCheck(task)
