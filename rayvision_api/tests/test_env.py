"""Test rayvision_api.env.RenderEnv functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import RenderEnvOperator


# pylint: disable=redefined-outer-name
@pytest.fixture()
def fixture_env(rayvision_connect):
    """Initialize the user object."""
    return RenderEnvOperator(rayvision_connect)


def test_add_render_env(fixture_env, render_env, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             'cgId': 2000,
             'cgName': 'Maya',
             'cgVersion': '2018',
             'renderLayerType': 0,
             'editName': 'tests',
             'renderSystem': 1,
             'pluginIds': [2703]
         }})
    assert fixture_env.add_render_env(render_env)['editName'] == 'tests'


def test_update_render_env(fixture_env, render_env, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Update render env failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        fixture_env.update_render_env(render_env)
    assert 'Update render env failed.' in str(err.value)


def test_delete_render_env(fixture_env, mock_requests):
    """Test if code ``500`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 500, 'data': {},
            'message': 'Delete render env failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        edit_name = 'test_ray'
        fixture_env.delete_render_env(edit_name)
    assert 'Delete render env failed.' in str(err.value)


def test_set_default_render_env(fixture_env, mock_requests):
    """Test if code ``600`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 600, 'data': {},
            'message': 'Set default render env failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        edit_name = 'test_ray'
        fixture_env.set_default_render_env(edit_name)
    assert 'Set default render env failed.' in str(err.value)
