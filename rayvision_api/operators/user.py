"""Interface to operate the user."""

import platform
from rayvision_api.signature import hump2underline


class UserOperator(object):
    """API user information operator."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect
        self._info = {'local_os': platform.system().lower(),
                      'domain': connect.domain,
                      'platform': connect.platform}


    @property
    def info(self):
        return self._info

    @property
    def user_id(self):
        return self.query_user_profile()["userId"]

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
        return self._connect.post(self._connect.url.queryUserProfile,
                                  validator=False)

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
        return self._connect.post(self._connect.url.queryUserSetting,
                                  validator=False)

    def update_user_settings(self, task_over_time):
        """Update user settings.

        Args:
            task_over_time (int): The task timeout is set in seconds.

        """
        data = {
            "taskOverTimeSec": task_over_time
        }
        return self._connect.post(self._connect.url.updateUserSetting, data)

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
        return self._connect.post(self._connect.url.getBid,
                                  validator=False)

    def _login(self):
        """Supplement user's configuration information.

        Call the API interface (query_user_profile, query_user_setting,
        get_transfer_bid) to supplement the user's configuration information

        """
        user_profile = self.query_user_profile()
        user_setting = self.query_user_setting()
        transfer_bid = self.get_transfer_bid()
        user_profile.update(user_setting)
        user_profile.update(transfer_bid)
        self._update_user_info(user_profile)

    def _update_user_info(self, user_profile):
        """Update user's configuration information.

        Args:
            user_profile (dict): User's configuration information.
                .e.g:
                    Too much information, only the part.
                    {
                        u 'config_bid': u '30201',
                        u 'cpu_price': '0.67',
                        u 'max_ignore_map_flag': '1',
                        u 'credit': '0.0',
                        u 'share_main_capital': '0',
                        u 'user_name': u 'mxinye123',
                        u 'common_coupon': '0.018',
                        u 'job': u '',
                        u 'address': u '',
                        u 'user_type': '1',
                        u 'input_bid': u '10202',
                        u 'hide_job_charge': '0',
                        u 'houdini_flag': '1',
                        u 'display_subaccount': '1',
                        u 'business_type': '1',
                        u 'usdbalance': '0.0',
                        u 'account_type': None,
                        u 'ignore_map_flag': '0',
                        u 'picture_lever': '0',
                        u 'rmbbalance': '64.495',
                        u 'city': u 'Guangdong Zhongshan',
                        u 'assfile_switch_flag': '0',
                        u 'user_id': '100093088',
                        u 'mandatory_analyse_all_agent': '0',
                        u 'subaccount_limits': '5',
                        u 'country': u 'China',
                        u 'download_limit': '0',
                        'domain_name': u 'task.renderbus.com',
                        u 'sub_delete_task': '0',
                        'platform': u '2',
                    }

        """
        for key, value in user_profile.items():
            key_underline = hump2underline(key)
            if key_underline != "platform":
                self._info[key_underline] = value
