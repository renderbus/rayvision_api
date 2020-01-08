"""Interface to operate the user."""

from rayvision_api import constants


class User(object):
    """API user information operation."""

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def query_user_profile(self):
        """Get user profile.

        Returns:
            dict: User profile info.
                e.g.:
                    {
                        "userId": 10001136,
                        "userName": "rayvision",
                        "platform": 2,
                        "phone": "173333333333",
                        "email": "",
                        "company": "",
                        "name": "",
                        "job": "",
                        "communicationNumber": "",
                        "softType": 2000,
                        "softStatus": 1,
                        "businessType": 1,
                        "status": 1,
                        "infoStatus": 0,
                        "accountType": 1,
                    }

        """
        return self._connect.post(constants.QUERY_USER_PROFILE)

    def query_user_setting(self):
        """Get user setting.

        Returns:
            dict: The information of the user settings.
                e.g.:
                    {
                        "infoStatus": null,
                        "accountType": null,
                        "shareMainCapital": 0,
                        "subDeleteTask": 0,
                        "useMainBalance": 0,
                        "singleNodeRenderFrames": "1",
                        "maxIgnoreMapFlag": "1",
                        "autoCommit": "2",
                        "separateAccountFlag": 0,
                        "mifileSwitchFlag": 0,
                        "assfileSwitchFlag": 0,
                        "manuallyStartAnalysisFlag": 0,
                        "downloadDisable": 0,
                        "taskOverTime": 12
                    }

        """
        return self._connect.post(constants.QUERY_USER_SETTINGS)

    def update_user_settings(self, task_over_time):
        """Update user settings.

        Args:
            task_over_time (int): The task timeout is set in seconds.

        """
        data = {
            'taskOverTimeSec': task_over_time
        }
        return self._connect.post(constants.UPDATE_USER_SETTINGS, data)

    def get_transfer_bid(self):
        """Get user transfer BID.

        Returns:
            dict: Transfer bid info.
                e.g.:
                    {
                        "config_bid": "30201",
                        "output_bid": "20201",
                        "input_bid": "10201"
                    }

        """
        return self._connect.post(constants.GET_TRANSFER_BID)
