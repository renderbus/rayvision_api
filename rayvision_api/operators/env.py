"""Set the rendering environment configuration."""

from cattr import unstructure

from rayvision_api import constants, fields


class RenderEnv(object):
    """Rendering environment configuration."""

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def add_render_env(self, render_env):
        """Adjust user rendering environment configuration.

        Args:
            render_env (dict): Rendering environment configuration.
                e.g.:
                    {
                        'cgId': "2000",
                        'cgName': 'Maya',
                        'cgVersion': '2018',
                        'renderLayerType': 0,
                        'editName': 'tests',
                        'renderSystem': '1',
                        'pluginIds': 2703
                    }

        Returns:
            dict: Render env info.
                e.g.:
                    {
                        'editName': 'tests'
                    }

        """
        if isinstance(render_env, dict):
            render_env = fields.Env(**render_env)
        data = unstructure(render_env)
        return self._connect.post(constants.ADD_RENDER_ENV, data)

    def update_render_env(self, render_env):
        """Modify the user rendering environment configuration.

        Args:
            render_env (dict): Rendering environment configuration.
                e.g.:
                    {
                        'cgId': "2000",
                        'cgName': 'Maya',
                        'cgVersion': '2018',
                        'renderLayerType': 0,
                        'editName': 'tests',
                        'renderSystem': '1',
                        'pluginIds': 2703,
                    }.

        """
        if isinstance(render_env, dict):
            render_env = fields.Env(**render_env)
        data = unstructure(render_env)
        return self._connect.post(constants.UPDATE_RENDER_ENV, data)

    def delete_render_env(self, edit_name):
        """Delete user rendering environment configuration.

        Args:
            edit_name (str): Rendering environment custom name.

        """
        data = {
            'editName': edit_name
        }
        return self._connect.post(constants.DELETE_RENDER_ENV, data)

    def set_default_render_env(self, edit_name):
        """Set the default render environment configuration.

        Args:
            edit_name (str): Rendering environment custom name.

        """
        data = {
            'editName': edit_name
        }
        return self._connect.post(constants.SET_DEFAULT_RENDER_ENV, data)

    def get_render_env(self, name):
        """Get the user rendering environment configuration.

        Args:
            name (str): The name of the DCC.
            e.g.:
                maya,
                houdini,
                3dsmax

        Return:
            list: Software info.
                e.g.:
                     [
                        {
                            "cgId": 2000,
                            "editName": "testRenderEnv332",
                            "cgName": "Maya",
                            "cgVersion": "2020",
                            "osName": 0,
                            "renderLayerType": 0,
                            "isDefault": 0,
                            "respUserPluginInfoVos": [
                                {
                                    "pluginId": 1166,
                                    "pluginName": "wobble",
                                    "pluginVersion": "wobble 0.9.5"
                                }
                            ]
                        },
                        {
                            "cgId": 2000,
                            "editName": "testRenderEnv222",
                            "cgName": "Maya",
                            "cgVersion": "2020",
                            "osName": 0,
                            "renderLayerType": 0,
                            "isDefault": 0,
                            "respUserPluginInfoVos": [
                                {
                                    "pluginId": 1166,
                                    "pluginName": "wobble",
                                    "pluginVersion": "wobble 0.9.5"
                                }
                    ]

        """
        cg_id = constants.DCC_ID_MAPPINGS[name]
        data = {'cgId': cg_id}
        return self._connect.post(constants.GET_RENDER_ENV, data)
