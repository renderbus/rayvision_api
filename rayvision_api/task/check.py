"""Check the analysis results.

Check the analysis of the task information and upload asset information.

"""
# Import built-in modules
import codecs
import json
import logging
import os

from past.builtins import long

# Import local modules
from rayvision_api.constants import MODIFIABLE_PARAM
from rayvision_api.exception import RayvisionError
from rayvision_api.operators.query import Query


# pylint: disable=useless-object-inheritance
class RayvisionCheck(object):
    """Check the analysis results."""

    def __init__(self, task):
        """Initialize instance."""
        self.logger = logging.getLogger(__name__)
        self.task = task
        self.errors_number = 0
        self.error_warn_info_list = []

    def execute(self, task_info, upload_info):
        """Check asset configuration information.

        Check the scene for problems and filter unwanted configuration
        information.

        """
        self.logger.info('[Rayvision_utils check start .....]')
        self.check_error_warn_info()
        self.is_scene_have_error()  # Check error.

        self._edit_param_and_write(task_info['scene_info_render'],
                                   task_info, upload_info)
        self.logger.info('[Rayvision_utils check end .....]')

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
        if self.task.tips_info:
            for code, value in self.task.tips_info.items():
                code_info_list = Query(self.task.connect).error_detail(
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
            self.task.task_info['scene_info_render'] = scene_info_render

        if task_info is not None:
            for key, value in task_info.items():
                if key in MODIFIABLE_PARAM:
                    if isinstance(value, (int, long, float)):
                        value = str(value)
                    self.task.task_info['task_info'][key] = value

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
            self.task.upload_info = upload_info
            with codecs.open(self.task.upload_json_path,
                             'w', 'utf-8') as f_upload_json:
                json.dump(upload_info, f_upload_json, indent=4,
                          ensure_ascii=False)

        # Write task.json.
        with codecs.open(self.task.task_json_path,
                         'w', 'utf-8') as f_task_json:
            json.dump(self.task.task_info, f_task_json, indent=4,
                      ensure_ascii=False)

        # Write tips.json.
        if not os.path.exists(self.task.tips_json_path):
            with codecs.open(self.task.tips_json_path,
                             'w', 'utf-8') as f_tips_json:
                json.dump(self.task.tips_info, f_tips_json,
                          indent=4, ensure_ascii=False)
