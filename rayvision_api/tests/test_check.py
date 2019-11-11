"""Test rayvision_utils.task.check.RayvisionCheck functions."""

# Import third-party modules
# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionError


def test_check_error_warn_info(check):
    """Test _is_scene_have_error this interface.

    Test We can get an empty list if the information is normal.

    """
    assert check.check_error_warn_info() == []


def test_is_scene_have_error(check):
    """Test _is_scene_have_error this interface.

    Test We can get an ``RayvisionError`` if the information is wrong.

    """
    check.errors_number = 1
    with pytest.raises(RayvisionError):
        check.is_scene_have_error()
