"""Set the rendering environment configuration."""

from rayvision_api import constants


class RenderEnvOperator(object):
    """The rendering environment configuration."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect

    def add_render_env(self, data):
        """Adjust user rendering environment configuration.

        Args:
            data (dict): Rendering environment configuration.
                e.g.:
                    {
                        'cgId': "2000",
                        'cgName': 'Maya',
                        'cgVersion': '2018',
                        'renderLayerType': 0,
                        'editName': 'tests',
                        'renderSystem': 1,
                        'pluginIds': [2703]
                    }

        Returns:
            dict: Render env info.
                e.g.:
                    {
                        'editName': 'tests'
                    }

        """

        return self._connect.post(self._connect.url.addRenderEnv, data)

    def update_render_env(self, data):
        """Modify the user rendering environment configuration.

        Args:
            data (dict): Rendering environment configuration.
                e.g.:
                    {
                        'cgId': "2000",
                        'cgName': 'Maya',
                        'cgVersion': '2018',
                        'renderLayerType': 0,
                        'editName': 'tests',
                        'renderSystem': 1,
                        'pluginIds': [2703],
                    }.

        """
        return self._connect.post(self._connect.url.updateRenderEnv,
                                  data)

    def delete_render_env(self, edit_name):
        """Delete user rendering environment configuration.

        Args:
            edit_name (str): Rendering environment custom name.

        """
        data = {
            'editName': edit_name
        }
        return self._connect.post(self._connect.url.deleteRenderEnv, data)

    def set_default_render_env(self, edit_name):
        """Set the default render environment configuration.

        Args:
            edit_name (str): Rendering environment custom name.

        """
        data = {
            'editName': edit_name
        }
        return self._connect.post(self._connect.url.setDefaultRenderEnv, data)

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
        return self._connect.post(self._connect.url.getRenderEnv, data)
