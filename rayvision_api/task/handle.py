# -*- coding=utf-8 -*-
"""Generating tasks.

Set asset information and general configuration information for the task.

"""

# Import built-in modules
from builtins import str
import logging
import os

# Import local modules
from rayvision_api.connect import Connect
from rayvision_api.constants import CG_SETTING
from rayvision_api.constants import TASK_INFO
from rayvision_api.exception import RayvisionError
from rayvision_api.operators import Tag
from rayvision_api.operators.task import Task
from rayvision_api.operators.user import User


# pylint: disable=useless-object-inheritance
class RayvisionTask(object):
    """Build task."""

    def __init__(self, domain, platform, access_id, access_key, local_os,
                 software_version, render_software, workspace,
                 cg_file, plugin_config=None, project_name=None):
        """Initialize task information.

        Initial configuration information and asset information of the
        initialization task.

        Args:
            domain (str): Url name.
            platform (str): Platform id.
            access_id (str): An authorization id that identifies the API
                caller.
            access_key (str):Authorization key for encrypting signature strings
                and server-side verification signature strings.
            local_os (str): system name.
            software_version (str): CG software version, usually have version.
                names like this:
                    Examples:
                        houdini: "17.5.293"
                        clarisse: "clarisse_ifx_4.0_sp3"
                        maya: "2018"
            render_software (str): CG software name, Note that the first letter
                should be capitalized.
                    Examples:
                        "Maya", "Houdini", "Clarisse"
            workspace (str): the SDK working directory (containing
                configuration files) By default, it is the workspace directory
                of the path where the SDK program is located.
            cg_file (str): CG rendering resources, is required.
            plugin_config (dict): Plug-in directory, is optional,default is
                None.
            project_name (str): The label name, or project name, is optional,
                default is None.

        """
        self.domain = domain
        self.platform = platform
        self.access_id = access_id
        self.access_key = access_key
        self.local_os = local_os  # "Windows"/"linux".
        self.software_version = software_version
        self.render_software = render_software
        self.workspace = workspace
        self.cg_file = cg_file
        self.plugin_config = plugin_config if plugin_config else {}
        self.project_name = project_name if project_name else ""
        self.logger = logging.getLogger(__name__)

        self.connect = Connect(
            access_id=self.access_id,
            access_key=self.access_key,
            domain=self.domain,
            platform=self.platform,
            protocol='https',
            headers=None
        )
        self.task_id = self.get_task_id()
        self.user_id = self.get_user_id()
        # Work directory.
        work_dir = os.path.join(self.workspace, 'work', self.task_id)
        self.ckeck_and_mk(work_dir)
        self.work_dir = work_dir

        # Log directory.
        log_dir = os.path.join(self.workspace, 'log', 'analyse')
        self.ckeck_and_mk(log_dir)

        # Process asset path.
        self.task_json_path = os.path.join(work_dir, 'task.json')
        self.asset_json_path = os.path.join(work_dir, 'asset.json')
        self.tips_json_path = os.path.join(work_dir, 'tips.json')
        self.upload_json_path = os.path.join(work_dir, 'upload.json')

        # Process asset info.
        self.task_info = TASK_INFO
        self.set_render_config()
        self.task_info['task_info']['task_id'] = self.task_id
        self.task_info['task_info']['platform'] = self.platform
        self.task_info['task_info']['user_id'] = self.user_id
        self.asset_info = {}  # Asset.json.
        self.tips_info = {}  # Tips.json.
        self.upload_info = {}  # Upload.json.
        self.preparatory_analyse(self.cg_file)

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
        task_id_info = Task(self.connect).create_task(count=1,
                                                      out_user_id=None)
        task_id = task_id_info.get('taskIdList', [''])[0]
        if task_id == '':
            # Task ID creating failed
            raise RayvisionError(1000000,
                                 r'Failed to create task number!')
        return str(task_id)

    def get_user_id(self):
        """Get user id.

        Example:
          >>> user_profile_info = {
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
        user_profile_info = User(self.connect).query_user_profile()
        user_id = user_profile_info.get('userId', '')
        if user_id == '':
            raise RayvisionError(1000000, r'Failed to get user number!')
        return str(user_id)

    @staticmethod
    def ckeck_and_mk(dir_path):
        """Check if the file exists,create if it does not."""
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def set_render_config(self):
        """Add the configuration of the rendering environment in task_info.

        Raises: RayvisionError
            if the software name is not supported software or if the cg_id is
                null.

        """
        self.logger.info('[Rayvision_utils set rendering configuration'
                         ' information start .....]')
        self.logger.info('INPUT:')
        self.logger.info('=' * 20)
        self.logger.info('cg_name: %s', self.render_software)
        self.logger.info('cg_version: %s', self.software_version)
        self.logger.info('plugin_config: %s', self.plugin_config)
        self.logger.info('project_name: %s', self.project_name)
        self.logger.info('=' * 20)

        try:
            cg_id = CG_SETTING[self.render_software]
        except KeyError:
            raise RayvisionError(1000000, (
                'Not matching the correct DCC software {},'
                'please check again'.format(self.render_software)))

        if cg_id is None:
            raise RayvisionError(1000000, r'Please input correct cg_name!')

        self.task_info['task_info']['cg_id'] = cg_id

        if self.project_name is not None:
            project_id = self.check_and_add_project_name(self.project_name)

            self.task_info['task_info']['project_name'] = self.project_name
            self.task_info['task_info']['project_id'] = project_id

        software_config_dict = dict()
        software_config_dict['cg_name'] = self.render_software
        software_config_dict['cg_version'] = self.software_version
        software_config_dict['plugins'] = self.plugin_config
        self.task_info['software_config'] = software_config_dict

        self.logger.info('[Rayvision_utils set rendering configuration'
                         'information end .....]')

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
        tag = Tag(self.connect)
        for _ in range(2):
            label_dict_list = (tag.get_label_list().
                               get('projectNameList', []))
            for label_dict in label_dict_list:
                if label_dict['projectName'] == project_name:
                    is_label_exist = True
                    project_id = str(label_dict['projectId'])
                    break
            # Add a label if the no label exists.
            if not is_label_exist:
                tag.add_label(project_name, '0')
            else:
                if project_id == '':
                    continue
                break

        return project_id

    def preparatory_analyse(self, cg_file, project_dir=''):
        """Set the scenario and project path before analysis.

        Handling the path and project path of the scene.

        Args:
            cg_file (str): Scene path.
            project_dir (str): Project path for scene production.

        """
        self.logger.info('[Rayvision_utils preparatory_analyse start .....]')

        self.logger.info('INPUT:')
        self.logger.info('=' * 20)
        self.logger.info('cg_file: %s', cg_file)
        self.logger.info('project_dir: %s', project_dir)
        self.logger.info('=' * 20)

        # self.is_analyse = True.
        # Pass self.task, directly modify task.
        self.task_info['task_info']['input_cg_file'] = (
            cg_file.replace('\\', '/'))
        if project_dir:
            self.task_info['task_info']['input_project_path'] = project_dir
        self.logger.info('[Rayvision_utils preparatory_analyse end .....]')
