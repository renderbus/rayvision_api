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
