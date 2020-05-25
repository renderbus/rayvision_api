"""Test rayvision_api.query.Query functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import QueryOperator


@pytest.fixture()
def fixture_query(rayvision_connect):
    """Get a Query object."""
    return QueryOperator(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_platforms(fixture_query, mock_requests):
    """Test query all platforms."""
    mock_requests({'code': 200,
                   'data': [{'platform': 2,
                             'name': 'platform2'},
                            {'platform': 3,
                             'name': 'platform3'}]})
    assert fixture_query.platforms()[0]['platform'] == 2


def test_error_detail(fixture_query, mock_requests):
    """Test we can get correct error message."""
    mock_requests({'code': 200, 'data': [{'code': "12345",
                                          'solutionPath': 'c:/tests.com'}]})
    details = fixture_query.error_detail("12345")
    assert details[0]['code'] == "12345"
    assert details[0]['solutionPath'] == 'c:/tests.com'


def test_get_task_list(fixture_query, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests({'code': 404, 'data': {}, 'message': 'Get task failed.'})
    with pytest.raises(RayvisionAPIError) as err:
        fixture_query.get_task_list()
    assert 'Get task failed.' in str(err.value)


def test_all_frame_status(fixture_query, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             'executingFramesTotal': 0, 'doneFramesTotal': 11,
             'failedFramesTotal': 230, 'waitingFramesTotal': 0,
             'totalFrames': 241,
         }})
    assert fixture_query.all_frame_status()['totalFrames'] == 241
    assert fixture_query.all_frame_status()['waitingFramesTotal'] == 0


def test_supported_software(fixture_query, mock_requests):
    """Test supported_software this interface."""
    mock_requests(
        {'data': {
            'renderInfoList': [
                {
                    'cgType': 'ma;mb', 'cgId': 2000, 'isNeedProjectPath': 1,
                    'isNeedAnalyse': 1, 'iconPath': '/img/softimage/maya.png',
                    'isSupportLinux': 1, 'cgName': 'Maya'
                },
                {
                    'cgType': 'project;render', 'cgId': 2013,
                    'isNeedProjectPath': 3,
                    'isNeedAnalyse': 1,
                    'iconPath': '/img/softimage/clarisse.png',
                    'isSupportLinux': 1, 'cgName': 'Clarisse'
                }],
            'defaultCgId': 2000,
            'isAutoCommit': 2,
        }}
    )
    info = fixture_query.supported_software()['renderInfoList']
    assert info[0]['cgName'] == 'Maya'
    assert info[0]['cgType'] == 'ma;mb'


def test_get_transfer_server_msg(fixture_query, mock_requests):
    """Test supported_software this interface."""
    mock_requests(
        {'data': {
            'raysyncTransfer': {
                'port': 2542,
                'proxyIp': 'render.raysync.cn',
                'proxyPort': 32011,
                'serverIp': '127.0.0.1',
                'serverPort': 2121,
                'sslPort': 2543
            }
        }}
    )
    info = fixture_query.get_transfer_server_msg()['raysyncTransfer']
    assert info['port'] == 2542
    assert info['proxyIp'] == 'render.raysync.cn'
    assert info['proxyPort'] == 32011
    assert info['serverIp'] == '127.0.0.1'
    assert info['serverPort'] == 2121
    assert info['sslPort'] == 2543


def test_get_raysync_user_key(fixture_query, mock_requests):
    """Test supported_software this interface."""
    mock_requests(
        {'data': {
            'raySyncUserKey': '8ccb94d67c1e4c17fd0691c02ab7f753cea64e3d',
            'userName': 'test',
            'platform': 2,
        }}
    )
    info = fixture_query.get_raysync_user_key()
    assert info['raySyncUserKey'] == '8ccb94d67c1e4c17fd0691c02ab7f753cea64e3d'
    assert info['userName'] == 'test'
    assert info['platform'] == 2
