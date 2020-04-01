"""Check the analysis results.

Check the analysis of the task information and upload asset information.

"""
# Import built-in modules
import codecs
import json
import logging
import os
import sys
import time
from past.builtins import long

# Import local modules
from rayvision_api.constants import MODIFIABLE_PARAM
from rayvision_api.exception import RayvisionError
from rayvision_api.utils import json_load

# pylint: disable=useless-object-inheritance
class RayvisionCheck(object):
    """Check the analysis results."""

    def __init__(self, api, analyze=None, workspace=None):
        """Initialize instance."""
        self.logger = logging.getLogger(__name__)
        self.api = api
        workspace = self.check_workspace(workspace)
        self.workspace = workspace

        self.task_json = None
        self.tips_json = None
        self.asset_json = None
        self.upload_json = None
        self.tips_info = {}
        self.task_info = {}
        self.asset_info = {}
        self.upload_info = {}

        self.analyze = analyze
        self.check_analyze(self.analyze, self.workspace)
        self.errors_number = 0
        self.error_warn_info_list = []

    @staticmethod
    def check_path(tmp_path):
        """Check if the path exists."""
        if not os.path.exists(tmp_path):
            raise Exception("{} is not found".format(tmp_path))

    def check_workspace(self, workspace):
        """Check the working environment.

        Args:
            workspace (str):  Workspace path.

        Returns:
            str: Workspace path.

        """
        if not workspace:
            if "win" in sys.platform.lower():
                workspace = os.path.join(os.environ["USERPROFILE"], "renderfarm_sdk")
            else:
                workspace = os.path.join(os.environ["HOME"], "renderfarm_sdk")
        else:
            self.check_path(workspace)

        return workspace

    def check_analyze(self, analyze, workspace):
        """Initializes the configuration file information."""
        if not analyze:
            tmp_name = str(int(time.time()))
            self.task_json = os.path.join(workspace, tmp_name, "task.json")
            self.tips_json = os.path.join(workspace, tmp_name, "tips.json")
            self.asset_json = os.path.join(workspace, tmp_name, "asset.json")
            self.upload_json = os.path.join(workspace, tmp_name, "upload.json")
        else:
            self.task_json = analyze.task_json
            self.tips_json = analyze.tips_json
            self.asset_json = analyze.asset_json
            self.upload_json = analyze.upload_json
            self.tips_info = analyze.tips_info
            self.task_info = analyze.task_info
            self.asset_info = analyze.asset_info
            self.upload_info = analyze.upload_info

    def check_task_info(self, task_info):
        """Check and add the required parameter information."""
        if not task_info:
            raise RayvisionError(2000, "task info can't be empty.")

        task_id = task_info["task_info"].get("task_id", None)
        user_id = task_info["task_info"].get("task_id", None)
        project_id = task_info["task_info"].get("task_id", None)
        if not bool(task_id):
            task_info["task_info"]["task_id"] = self.api.get_task_id()
        if not bool(user_id):
            task_info["task_info"]["user_id"] = self.api.get_user_id()
        if not bool(project_id):
            task_info["task_info"]["project_id"] = self.api.check_and_add_project_name(task_info["task_info"]["project_name"])
        return task_info

    def execute(self, task_json, upload_json):
        """Check asset configuration information.

        Check the scene for problems and filter unwanted configuration
        information.

        """
        task_info = json_load(task_json)
        upload_info = json_load(upload_json)
        self.logger.info('[Rayvision_utils check start .....]')
        self.task_info = self.check_task_info(task_info)
        self.upload_info = upload_info or {}

        self.check_error_warn_info()
        self.is_scene_have_error()  # Check error.
        task_id = self.write()
        return task_id

    def write(self):
        """Check and write to a json file."""
        scene_info_render = self.task_info.get("scene_info_render") or self.task_info["scene_info"]
        self._edit_param_and_write(scene_info_render, self.task_info["task_info"], self.upload_info)
        self.logger.info('[Rayvision_utils check end .....]')
        return self.task_info["task_info"]["task_id"]

    def check_error_warn_info(self, language='0'):
        """Check the error in the analysis scenario.

        According to the status code of the analyzed error information, the
        API interface is called to obtain detailed error information and
        solutions, and the warning information is printed out, and the number
        of error information is recorded.

        Args:
            language (str): The language that identifies the details of the
            error obtained, 0: Chinese (default) 1: English.

        Returns:
            list: List of detailed descriptions of errors.

        """
        self.logger.info('[Rayvision_utils check_error_warn_info start .....]')
        if self.tips_info:
            for code, value in self.tips_info.items():
                code_info_list = self.api.query.error_detail(
                    code, language=language)
                for code_info in code_info_list:
                    code_info['details'] = value
                    if str(code_info['type']) == '1':  # 0:warning  1:error.
                        self.errors_number += 1
                    self.error_warn_info_list.append(code_info)

        self.logger.warning('error_warn_info_list: %s',
                            self.error_warn_info_list)
        self.logger.info('[Rayvision_utils check_error_warn_info end .....]')
        return self.error_warn_info_list

    def is_scene_have_error(self):
        """Check the scene.

        Determine whether the scene has an error based on the number of
        serious errors.

        Raises:
            RayvisionError: There is a problem with the scene.

        """
        if self.errors_number > 0:
            return_message = (r'There are {0} errors. error_warn_info_list:{1}'
                              .format(self.errors_number,
                                      self.error_warn_info_list))
            # Analysis completed with errors.
            raise RayvisionError(1000000, return_message)

    def _edit_param_and_write(self, scene_info_render=None,
                              task_info=None, upload_info=None):
        """Write configuration information to the json file.

        Write the filtered configuration information and check the correct
        scene information into the json file.

        """
        self.logger.info('INPUT:')
        self.logger.info('=' * 20)
        self.logger.info('scene_info_render: %s', scene_info_render)
        self.logger.info('task_info: %s', task_info)
        self.logger.info('=' * 20)

        if scene_info_render:
            self.task_info['scene_info_render'] = scene_info_render

        if task_info is not None:
            for key, value in task_info.items():
                if key in MODIFIABLE_PARAM:
                    if isinstance(value, (int, long, float)):
                        value = str(value)
                    self.task_info['task_info'][key] = value

        self._write_to_json_file(upload_info)

        return True

    def _write_to_json_file(self, upload_info):
        """Update json file.

        Update the processed asset information to the corresponding json file.

        Args:
            upload_info (dict): Scene path information and texture information
                used in the scene.

        """
        # Write upload.json.
        if upload_info is not None:
            self.upload_info = upload_info
            with codecs.open(self.upload_json,
                             'w', 'utf-8') as f_upload_json:
                json.dump(upload_info, f_upload_json, indent=4,
                          ensure_ascii=False)

        # Write task.json.
        with codecs.open(self.task_json,
                         'w', 'utf-8') as f_task_json:
            json.dump(self.task_info, f_task_json, indent=4,
                      ensure_ascii=False)

        # Write tips.json.
        if not os.path.exists(self.tips_json):
            with codecs.open(self.tips_json,
                             'w', 'utf-8') as f_tips_json:
                json.dump(self.tips_info, f_tips_json,
                          indent=4, ensure_ascii=False)
