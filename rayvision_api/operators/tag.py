"""API operation on tags."""


class TagOperator(object):
    """Task tag settings."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect

    def add_label(self, new_name, status=1):
        """Add a custom label.

        Args:
            new_name (str): Label name.
            status (int, optional): Label status,0 or 1,default is 1.

        """
        data = {
            'newName': new_name,
            'status': int(status)
        }
        return self._connect.post(self._connect.url.add, data)

    def delete_label(self, del_name):
        """Delete custom label.

        Args:
            del_name (str): The name of the label to be deleted.

        """
        data = {'delName': del_name}
        return self._connect.post(self._connect.url.delete, data)

    def get_label_list(self):
        """Get custom labels.

        Returns:
            dict: Label list info.
                e.g.:
                    {
                        "projectNameList": [
                            {
                                "projectId": 3671,
                                "projectName": "myLabel"
                            }
                        ]
                    }

        """

        return self._connect.post(self._connect.url.getList, validator=False)

    def get_project_list(self):
        """Get custom labels.

        Returns:
            list: Label list info.
                e.g.:
                    [
                        {
                            "projectId": 3671,
                            "projectName": "myLabel"
                        }
                    ]

        """
        return self.get_label_list()['projectNameList']

    def add_task_tag(self, tag, task_ids):
        """Add a custom task tag.
                Args:
                    tag (str): Label name.
                    task_ids (list[int], optional): task id list.

        """
        data = {
            "label": tag,
            "taskIds": task_ids
        }
        return self._connect.post(self._connect.url.addTaskLabel, data)

    def delete_task_tag(self, tag_ids):
        """del custom task label.
                Args:
                    label_ids (list[int], optional): lable id list.

        """
        data = {
            "labelIds": tag_ids
        }
        return self._connect.post(self._connect.url.deleteTaskLabel, data)
