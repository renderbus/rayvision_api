"""Initialize user, task, query, environment, tag interface."""

import logging

from future.moves.urllib.error import HTTPError

from rayvision_api import utils
from rayvision_api.connect import Connect
from rayvision_api.exception import RayvisionError
from rayvision_api.exception import RayvisonTaskIdError
from rayvision_api.operators import Query
from rayvision_api.operators import RenderEnv
from rayvision_api.operators import Tag
from rayvision_api.operators import Task
from rayvision_api.operators import User


class RayvisionAPI(object):
    """Create the request object.

    Including user action, task action, query action, environment operation
    and tag action.
    """

    def __init__(self, access_id, access_key, domain='task.renderbus.com',
                 platform='4', protocol='https', local_os='windows',
                 logger=None):
        """Please note that this is API parameter initialization.

        Args:
            access_id (str): The access id of API.
            access_key (str): The access key of the API.
            domain (str, optional): The domain address of the API.
            platform (str, optional): The platform of renderFarm.
            protocol (str, optional): The requests protocol.
            local_os (str, optional): The name of current system,support
                "window" and "linux"
            logger (logging.Logger, optional): The logging logger instance.

        """
        self.logger = logger or logging.getLogger(__name__)
        self.user_info = {'local_os': local_os, 'domain': domain, 'platform': platform}
        connect = Connect(access_id, access_key, protocol, domain, platform)
        self.user = User(connect)
        self.task = Task(connect)
        self.query = Query(connect)
        self.tag = Tag(connect)
        self.env = RenderEnv(connect)

        try:
            self._login()
        except HTTPError:
            self.logger.error('Login failed.')
            raise RayvisionError(20020, 'Login failed.')

    def _login(self):
        """Supplement user's configuration information.

        Call the API interface (query_user_profile, query_user_setting,
        get_transfer_bid) to supplement the user's configuration information

        """
        self.logger.info('Starting login.')
        user_profile = self.user.query_user_profile()
        user_setting = self.user.query_user_setting()
        transfer_bid = self.user.get_transfer_bid()
        user_profile.update(user_setting)
        user_profile.update(transfer_bid)
        self._update_user_info(user_profile)
        self.logger.debug('User information: %s', self.user_info)

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
            key_underline = utils.hump2underline(key)
            if key_underline != 'platform':
                self.user_info[key_underline] = value

    def get_task_id(self):
        """Get task id.

        Example::

            task_id_info = {
                    "taskIdList": [1658434],
                    "aliasTaskIdList": [2W1658434],
                    "userId": 100093088
                }

        Returns: str

        """
        task_id_info = self.task.create_task(count=1, out_user_id=None)
        task_id = task_id_info.get('taskIdList', [''])[0]
        if task_id == '':
            # Task ID creating failed
            raise RayvisionError(1000000,
                                 r'Failed to create task number!')
        return str(task_id)

    def get_user_id(self):
        """Get user id.

        Example:
            user_profile_info = {
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
        Returns: str

        """
        user_profile_info = self.user.query_user_profile()
        user_id = user_profile_info.get('userId', '')
        if user_id == '':
            raise RayvisionError(1000000, r'Failed to get user number!')
        return str(user_id)

    def check_and_add_project_name(self, project_name):
        """Get the tag id.

        Call the API interface to obtain all the label information of the
        user, determine whether the label name to be added already exists,
        and obtain the label id if it exists. If the label does not exist,
        the API interface is repeatedly requested. The request is up to three
        times. If the third time does not exist, the empty string is returned.

        Args:
            project_name (str): The name of the tag to be added.

        Returns:
            int: Tag id.

        """
        is_label_exist = False
        project_id = ''
        for _ in range(2):
            label_dict_list = (self.tag.get_label_list().
                               get('projectNameList', []))
            for label_dict in label_dict_list:
                if label_dict['projectName'] == project_name:
                    is_label_exist = True
                    project_id = str(label_dict['projectId'])
                    break
            # Add a label if the no label exists.
            if not is_label_exist:
                self.tag.add_label(project_name, '0')
            else:
                if project_id == '':
                    continue
                break

        return project_id

    def submit(self, task_id):
        """Submit a task.

        Args:
            task_id (int): Task id.

        """
        if isinstance(task_id, int):
            self.task.submit_task(task_id)
        else:
            raise RayvisonTaskIdError(10006, "task_id must int !!!!")

        return True