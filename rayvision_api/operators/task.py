"""Interface to operate on the task."""


class TaskOperator(object):
    """API task related operations."""

    TASK_PARAM = "taskIds"

    def __init__(self, connect):
        """Initialize instance."""
        self._connect = connect

    def create_task(self, count=1, out_user_id=None, task_user_level=50,
                    labels=None):
        """Create task ID.

        Args:
            count (int, optional): The quantity of task ID.
            out_user_id (int, optional): Non-required, external user ID, used
                to distinguish users accessing third parties.
            task_user_level (int): Set the user's task level to either 50 or
                60, default is 50.
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
            data['labels'] = labels
        return self._connect.post(self._connect.url.createTask, data)

    def submit_task(self, task_id, asset_lsolation_model=None,
                    out_user_id=None):
        """Submit task.

        Args:
            task_id (int): Submit task ID.
            asset_lsolation_model (str): Asset isolation type, Optional value,
                default is null, optional value:'TASK_ID_MODEL' or 'OUT_USER_MODEL'.
            out_user_id (str): The asset isolates the user ID, Optional value,
                when asset_lsolation_model='OUT_USER_MODEL' ,'out_user_id' cant be empty.

        """
        data = {
            "taskId": task_id
        }
        if asset_lsolation_model:
            data["assetIsolationModel"] = asset_lsolation_model
        if out_user_id:
            data["outUserId"] = out_user_id.strip()

        return self._connect.post(self._connect.url.submitTask, data)

    def stop_task(self, task_param_list):
        """Stop the task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.stopTask,
                                  {self.TASK_PARAM: task_param_list})

    def start_task(self, task_param_list):
        """Start task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.startTask,
                                  {self.TASK_PARAM: task_param_list})

    def abort_task(self, task_param_list):
        """Give up the task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.abortTask,
                                  {self.TASK_PARAM: task_param_list})

    def delete_task(self, task_param_list):
        """Delete task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.deleteTask,
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
        return self._connect.post(self._connect.url.updateTaskUserLevel, data)

    def set_task_overtime_top(self, task_id_list, overtime):
        """Set the task timeout stop time.

        Args:
            task_id_list (list of int): Task list.
            overtime (int or float): Timeout time, unit: second.
            Example:
                {
                    "taskIds":[485],
                    "overTime":1800
                }
        """
        data = {
            'taskIds': task_id_list,
            'overTime': overtime
        }
        return self._connect.post(self._connect.url.setOverTimeStop, data)

    def full_speed(self, task_id_list):
        """Full to render.

        Args:
            task_id_list (list of int): Task list.
            Example:
                {
                    "taskIds":[485],
                }
        """
        data = {
            'taskIds': task_id_list,
        }
        return self._connect.post(self._connect.url, data)
