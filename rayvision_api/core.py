"""Initialize user, task, query, environment, tag interface."""

import json
import logging
import os

from future.moves.urllib.error import HTTPError

from rayvision_api.connect import Connect
from rayvision_api.constants import PACKAGE_NAME
from rayvision_api.exception import RayvisionError, RayvisonTaskIdError, UploadFileNotSupportError
from rayvision_api.operators import QueryOperator
from rayvision_api.operators import RenderEnvOperator
from rayvision_api.operators import TagOperator
from rayvision_api.operators import TaskOperator
from rayvision_api.operators import TransmitOperator
from rayvision_api.operators import UserOperator
from rayvision_api.task.check import RayvisionCheck
from rayvision_log import init_logger


class RayvisionAPI(object):
    """Create the request object.

    Including user action, task action, query action, environment operation
    and tag action.
    """

    def __init__(self,
                 access_id=None,
                 access_key=None,
                 domain='task.renderbus.com',
                 platform='4',
                 protocol='https',
                 logger=None):
        """Please note that this is API parameter initialization.

        Args:
            access_id (str, optional): The access id of API.
            access_key (str, optional): The access key of the API.
            domain (str, optional): The domain address of the API.
            platform (str, optional): The platform of renderFarm.
            protocol (str, optional): The requests protocol.
            logger (logging.Logger, optional): The logging logger instance.

        """
        self.logger = logger
        if not self.logger:
            init_logger(PACKAGE_NAME)
            self.logger = logging.getLogger(__name__)

        access_id = access_id or os.getenv("RAYVISION_API_ACCESS_ID")
        if not access_id:
            raise TypeError(
                'Required "access_id" not specified. Pass as argument or set '
                'in environment variable RAYVISION_API_ACCESS_ID.'
            )
        access_key = access_key or os.getenv("RAYVISION_API_KEY")
        if not access_id:
            raise TypeError(
                'Required "access_key" not specified. Pass as argument or set '
                'in environment variable RAYVISION_API_KEY.'
            )

        self._connect = Connect(access_id,
                                access_key,
                                protocol,
                                domain,
                                platform)

        # Initial all api instance.
        self.user = UserOperator(self._connect)
        self.task = TaskOperator(self._connect)
        self.query = QueryOperator(self._connect)
        self.tag = TagOperator(self._connect)
        self.env = RenderEnvOperator(self._connect)
        self.transmit = TransmitOperator(self._connect)

        try:
            self._login()
        except HTTPError:
            raise RayvisionError(20020, 'Login failed.')

    @property
    def user_info(self):
        return self.user.info

    @property
    def connect(self):
        """rayvision.api.Connect: The current connect instance."""
        return self._connect

    def _login(self):
        """Supplement user's configuration information.

        Call the API interface (query_user_profile, query_user_setting,
        get_transfer_bid) to supplement the user's configuration information

        """
        user_profile = self.user.query_user_profile()
        user_setting = self.user.query_user_setting()
        transfer_bid = self.user.get_transfer_bid()
        user_profile.update(user_setting)
        user_profile.update(transfer_bid)
        self.user._update_user_info(user_profile)

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
        Returns:
            int: The ID number of the current user.

        """
        try:
            return self.user.user_id
        except KeyError:
            raise RayvisionError(1000000, 'Failed to get user number!')

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


    def submit(self, task_id, producer=None):
        """Submit a task.

        Args:
            task_id (int): Task id.
            producer (str, optional): Producer.

        """
        if not isinstance(task_id, int):
            raise RayvisonTaskIdError(10006, "task_id must int !!!!")

        self.task.submit_task(task_id, producer)
        return True


    def submit_by_data(self, task_info, file_name="task.json", producer=None):
        """Submit tasks based on json files.

        Args:
            task_info (string): task.json content.
            file_name (string, optional): The name of the json file to be uploaded, only support ""
            producer (string, optional): Producer.

        Returns:

        """
        task_info, task_id = RayvisionCheck(self).execute(task_info, only_id=False)
        task_info = json.dumps(task_info)
        self.transmit.upload_json_content(task_id, file_name=file_name, content=task_info)
        self.task.submit_task(task_id, producer)
        return True
