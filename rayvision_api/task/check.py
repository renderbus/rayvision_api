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
import re

from rayvision_api.constants import MODIFIABLE_PARAM, CG_SETTING
from rayvision_api.exception import RayvisionError, HardwareConfigIdError, NotSupportPluginError, NotSupportCGSoftwareError, NotSupportHardwareCodeError
# Import local modules
from rayvision_api.utils import json_load, exists_or_create, update_task_info, json_save


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
                workspace = os.path.join(os.environ["USERPROFILE"],
                                         "renderfarm_sdk")
            else:
                workspace = os.path.join(os.environ["HOME"], "renderfarm_sdk")
        else:
            self.check_path(workspace)

        return workspace

    def check_analyze(self, analyze, workspace, is_cover=True):
        """Initializes the configuration file information."""

        if analyze:
            self.task_json = analyze.task_json
            self.tips_json = analyze.tips_json
            self.asset_json = analyze.asset_json
            self.upload_json = analyze.upload_json
            self.tips_info = analyze.tips_info
            self.task_info = analyze.task_info
            self.asset_info = analyze.asset_info
            self.upload_info = analyze.upload_info
            tmp_dir_name = os.path.dirname(analyze.task_json)

        elif is_cover:
            self.task_json = os.path.join(workspace, "task.json")
            self.tips_json = os.path.join(workspace, "tips.json")
            self.asset_json = os.path.join(workspace, "asset.json")
            self.upload_json = os.path.join(workspace, "upload.json")
            tmp_dir_name = workspace

        else:
            tmp_name = str(int(time.time()))
            tmp_dir_name = os.path.join(self.workspace, tmp_name)
            exists_or_create(tmp_dir_name)
            self.task_json = os.path.join(tmp_dir_name, "task.json")
            self.tips_json = os.path.join(tmp_dir_name, "tips.json")
            self.asset_json = os.path.join(tmp_dir_name, "asset.json")
            self.upload_json = os.path.join(tmp_dir_name, "upload.json")

        return tmp_dir_name

    def check_task_info(self, task_info):
        """Check and add the required parameter information."""
        if not task_info:
            raise RayvisionError(2000, "task info can't be empty.")

        task_id = task_info["task_info"].get("task_id", None)
        user_id = task_info["task_info"].get("user_id", None)
        project_id = task_info["task_info"].get("project_id", None)
        if not bool(task_id):
            task_info["task_info"]["task_id"] = str(self.api.task._generate_task_id())
        if not bool(user_id):
            task_info["task_info"]["user_id"] = str(self.api.get_user_id())
        if not bool(project_id):
            if task_info["task_info"].get("project_name"):
                project_id = str(self.api.check_and_add_project_name(task_info["task_info"]["project_name"]))
            else:
                project_id = "0"
            task_info["task_info"]["project_id"] = project_id
        return task_info

    def get_json_info(self, data):
        if isinstance(data, dict):
            return data
        elif os.path.isfile(data):
            return json_load(data)

    def execute(self, hardware_config, task_json, upload_json="", asset_json="", is_cover=True, only_id=True):
        """Check asset configuration information.

        Check the scene for problems and filter unwanted configuration
        information.
        Args:
            is_cover (bool): Whether the updated json file overwrites the file under the original path,
                             by default 'True'.

        """
        workspace = self.workspace if isinstance(task_json, dict) else os.path.dirname(task_json)
        tmp_dir_name = self.check_analyze(analyze=self.analyze,
                                          workspace=workspace,
                                          is_cover=is_cover)
        if isinstance(task_json, dict):
            json_save(self.task_json, task_json)
        self.check_plugin(self.get_json_info(task_json))

        self.set_custom_hardware(hardware_config, self.get_json_info(task_json), self.task_json)

        task_info = self.get_json_info(task_json)
        upload_info = self.get_json_info(upload_json)
        asset_info = self.get_json_info(asset_json)
        self.logger.info('[Rayvision_utils check start .....]')
        self.task_info = self.check_task_info(task_info)
        self.upload_info = upload_info or {}
        self.asset_info = asset_info

        language = "0" if self.api._connect.domain.startswith("task") else "1"
        self.check_error_warn_info(language=language)
        self.is_scene_have_error()  # Check error.
        data = self.write(only_id=only_id)
        return data

    def write(self, only_id=True):
        """Check and write to a json file."""
        scene_info_render = self.task_info.get("scene_info_render") or \
                            self.task_info["scene_info"]
        self._edit_param_and_write(scene_info_render,
                                   self.task_info["task_info"],
                                   self.upload_info)
        if only_id:
            return int(self.task_info["task_info"]["task_id"])
        self.logger.info('[Rayvision_utils check end .....]')
        return self.task_info, int(self.task_info["task_info"]["task_id"])

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
                    if isinstance(value, (int, str, float)):
                        value = str(value)
                    self.task_info['task_info'][key] = value

        self._write_to_json_file()

        return True

    def _write_json(self, data, path):
        """write to json."""

        if data and path is not None and os.path.isfile(path):
            with codecs.open(path, "w", "utf-8") as f_json:
                json.dump(data, f_json, indent=4, ensure_ascii=False)

    def _write_to_json_file(self):
        """Update json file.

        """
        self._write_json(self.task_info, self.task_json)
        self._write_json(self.upload_info, self.upload_json)
        self._write_json(self.asset_info, self.asset_json)
        self._write_json(self.tips_info, self.tips_json)

    def check_plugin(self, task_data):
        version = task_data["software_config"]["cg_version"]
        cg_name = task_data["software_config"]["cg_name"]
        cg_id = task_data["task_info"]["cg_id"]
        plugin_name_list = self.api.query.supported_plugin(CG_SETTING[str(cg_id)].lower())["cgVersion"]
        cg_id = None
        all_version = []

        for pn_info in plugin_name_list:
            cg_version = pn_info["cgVersion"]
            all_version.append(cg_version)
            if cg_version == version:
                cg_id = pn_info["id"]
                break
        if not cg_id:
            raise RayvisionError(1000000, "%s %s is not support, supported versions:%s" % (
                cg_name, version, ",".join(sorted(all_version))))

    def set_custom_hardware(self, custom_hardware, task_info, task_path):
        """Check whether the hardware configuration information exists and whether it meets the requirements."""
        hardware_config_list = self.api.user.get_hardware_config()
        platform = task_info['task_info'].get('platform', self.api.platform)
        cg_id = task_info['task_info']['cg_id']
        plugins = task_info['software_config']['plugins']
        check_keys = ['model', 'ram', 'gpuNum']
        gpu_num = custom_hardware.get('gpuNum')
        hardware_id = ''
        exist_not_support_code = False
        allow_hardware_config = []
        if task_info['software_config']['cg_name'] == "CINEMA 4D" and task_info['software_config']['cg_version'] in ["2024", "2025"]:
            if custom_hardware.get('model').lower() in ["1080ti"] and custom_hardware.get('gpuNum').lower() in ["2*gpu"] and self.api.platform in ["21", "59", "61"]:
                raise HardwareConfigIdError(1000001, "CINEMA 4D 2024&2025 GPU area hardware configuration model does"
                                                     " not allow 1080Ti with 2*GPU")

        for one_hardware_config in hardware_config_list:
            if not one_hardware_config['status']:
                continue
            not_support_cgid = one_hardware_config['notSupportCgId']
            if not_support_cgid and cg_id in not_support_cgid:
                if all(map(lambda key: custom_hardware[key] == one_hardware_config[key], check_keys)):
                    raise NotSupportCGSoftwareError
            not_support_code = one_hardware_config['notSupportCode']
            not_support_code_list = [item for item in self.tips_info.keys() if item in not_support_code]
            if (len(not_support_code_list) > 0) and (custom_hardware["model"] == one_hardware_config["model"]):
                exist_not_support_code = True
                continue
            if one_hardware_config['platform'] != int(platform):
                continue
            if len(not_support_code_list) == 0:
                allow_hardware_config.append(str({'model': one_hardware_config["model"], 'ram': one_hardware_config["ram"],
                                    'gpuNum': one_hardware_config["gpuNum"]}))
            if not all(map(lambda key: custom_hardware[key] == one_hardware_config[key], check_keys)):
                continue
            not_support_plugin_list = one_hardware_config['notSupportPluginList']
            if not_support_plugin_list:
                for plugin_str in not_support_plugin_list:
                    for plugin_name, plugin_ver in plugins.items():
                        plugin_data = "%s %s" % (plugin_name, plugin_ver)
                        re_result = re.findall(plugin_str, plugin_data, re.I)
                        if re_result and re_result[0]:
                            raise NotSupportPluginError(1000000, "%s is not support %s%s" % (custom_hardware, plugin_name, plugin_ver))

            hardware_id = str(one_hardware_config.get('id', ""))

        if exist_not_support_code:
            raise NotSupportHardwareCodeError(1000000, "It was detected that the rendering file does not match the hardware settings, please choose from the following options:%s" % ",".join(
                allow_hardware_config))
        if not hardware_id:
            raise HardwareConfigIdError(1000000, "Allowed Hardware Configuration Information:%s" % ",".join(
                allow_hardware_config))

        update_hardware_config = {
            "hardwareConfigId": hardware_id,
            "ram": custom_hardware["ram"].replace("GB", ""),
            "graphics_cards_num": gpu_num[0] if gpu_num else "2"
        }
        update_task_info(update_hardware_config, task_path)

