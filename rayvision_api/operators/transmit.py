#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class TransmitOperator(object):
    """The interface to perform the transfer."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect

    def upload_json_content(self, task_id, content, file_name="task.json"):
        """upload task json file.upload_json_format

        """
        data = {
            "taskId": task_id,
            "fileName": file_name,
            "content": content,
        }

        return self._connect.post(self._connect.url.taskJsonFile, data=data)

    def get_transfer_config(self):
        """upload task json file.upload_json_format

        """
        return self._connect.post(self._connect.url.getConfig, validator=False)

    def get_output_files(self, task_id=None, tree_path="/"):
        """Get the specified path under the user output storage or the file path under the task.

        Args:
            task_id (int): small task id, the unlayered main task ID is the same as the subtask ID,
                           and the hierarchical rendering subtask ID is the task ID of each layer,
            tree_path (string): file relative output path,
                           example:"/1484861_muti_layer_test/layer3",
                           Warnings:tree_path will default to "/" when task_id is not empty.

        Returns:

        """
        data = {
            "treePath": tree_path,
        }
        if task_id:
            data["taskId"] = task_id
            data["treePath"] = "/"

        return self._connect.post(self._connect.url.getOutputUserDirFile, data=data)