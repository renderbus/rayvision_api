"""A Python-based API for Using Renderbus cloud rendering service."""

# pylint: disable=import-error
from pkg_resources import DistributionNotFound, get_distribution

# Import local modules
from rayvision_api.core import RayvisionAPI

# All API of the public.
__all__ = ['RayvisionAPI']

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # Package is not installed.
    __version__ = '0.0.0-dev.1'
