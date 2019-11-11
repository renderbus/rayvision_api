"""Set variable type.

Specifies the parameter type for setting the rendering environment
configuration.

"""

from attr import attrib, attrs


# pylint: disable=too-few-public-methods
@attrs
class Env(object):
    """Setting of the parameter type of the rendering environment."""

    cgId = attrib(type=int)
    cgName = attrib(type=str)
    cgVersion = attrib(type=str)
    renderLayerType = attrib(type=int)
    editName = attrib(type=str)
    renderSystem = attrib(type=int)
    pluginIds = attrib(type=list)
