"""API operation on tags."""


class TagOperator(object):
    """Task tag settings."""

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def add_label(self, new_name, status=1):
        """Add a custom label.

        Args:
            new_name (str): Label name.
            status (int, optional): Label status,0 or 1,default is 1.

        """
        data = {
            'newName': new_name,
            'status': status
        }
        return self._connect.post(self._connect.url.addLabel, data)

    def delete_label(self, del_name):
        """Delete custom label.

        Args:
            del_name (str): The name of the label to be deleted.

        """
        return self._connect.post(self._connect.url.deleteLabel,
                                  {'delName': del_name})

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
        return self._connect.post(self._connect.url.getLabelList,
                                  validator=False)

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
