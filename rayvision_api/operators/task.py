"""Interface to operate on the task."""

from rayvision_api import constants


class Task(object):
    """API task related operations."""

    TASK_PARAM = 'taskIds'

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def create_task(self, count=1, out_user_id=None, task_user_level=50, labels=None):
        """Create task ID.

        Args:
            count (int, optional): The quantity of task ID.
            out_user_id (int, optional): Non-required, external user ID, used
                to distinguish users accessing third parties.
            task_user_level (int): Set the user's task level to either 50 or 60, default is 50.
            labels (list or tuple): Custom task labels, optional.

        Returns:
            dict: Task info.
                e.g.:
                    {
                        "taskIdList": [1658434],
                        "aliasTaskIdList": [2W1658434],
                        "userId": 100093088
                    }

        """
        data = {
            'count': count,
            'taskUserLevel': task_user_level
        }
        if out_user_id:
            data['outUserId'] = out_user_id
        if labels:
            if isinstance(labels, list):
                data['labels'] = labels
            else:
                raise TypeError('Labels must be lists')
        return self._connect.post(constants.CREATE_TASK, data)

    def submit_task(self, task_id, asset_lsolation_model= None, out_user_id= None):
        """Submit task.

        Args:
            task_id (int): Submit task ID.

        """
        data = {
            "taskId": task_id
        }

        if bool(asset_lsolation_model) and isinstance(asset_lsolation_model, str):
            if asset_lsolation_model.strip().upper() in ["TASK_ID_MODEL", "OUT_USER_MODEL"]:
                data["assetIsolationModel"] = asset_lsolation_model.strip().upper()
            else:
                raise TypeError("asset_lsolation_model must be 'TASK_ID_MODEL' or 'OUT_USER_MODEL'")

        if bool(out_user_id) and isinstance(out_user_id, str):
            data["outUserId"] = out_user_id.strip()

        self._connect.post(constants.SUBMIT_TASK, data)

    def stop_task(self, task_param_list):
        """Stop the task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.STOP_TASK,
                           {self.TASK_PARAM: task_param_list})

    def start_task(self, task_param_list):
        """Start task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.START_TASK,
                           {self.TASK_PARAM: task_param_list})

    def abort_task(self, task_param_list):
        """Give up the task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.ABORT_TASK,
                           {self.TASK_PARAM: task_param_list})

    def delete_task(self, task_param_list):
        """Delete task.

        Args:
            task_param_list (list): Task ID list.

        """
        self._connect.post(constants.DELETE_TASK,
                           {self.TASK_PARAM: task_param_list})

    def update_task_level(self, task_id, task_level):
        """Update the level of the task in the render.

        Args:
            task_id (int): Task id.
            task_level (int): Task level.

        """
        data = {
            'taskId': task_id,
            'taskUserLevel': task_level,
        }
        self._connect.post(constants.UPDATE_TASK_USER_LEVEL, data)
