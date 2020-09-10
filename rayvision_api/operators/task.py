"""Interface to operate on the task."""

from rayvision_api.exception import RayvisionError


class TaskOperator(object):
    """API task related operations."""

    TASK_PARAM = "taskIds"

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect
        self._has_submit = False
        self._task_id = None

    def create_task(self,
                    count=1,
                    task_user_level=50,
                    out_user_id=None,
                    labels=None,
                    clone_original_id=None,
                    artist=None):
        """Create a task ID.

        Args:
            count (int, optional): The quantity of task ID.
            task_user_level (int): Set the user's task level to either 50 or
                60, default is 50.
            out_user_id (int, optional): Non-required, external user ID, used
                to distinguish users accessing third parties.
            labels (list or tuple, optional): Custom task labels.
            clone_original_id (int, optional): Clone the original task ID.
            artist (str, optional): producer.

        Returns:
            dict: The information of the task.
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
        if clone_original_id:
            data['cloneOriginalId'] = int(clone_original_id)
        if artist:
            data['artist'] = artist
        return self._connect.post(self._connect.url.createTask, data)

    def _generate_task_id(self):
        """Get task id.

        Example::

            task_id_info = {
                    "taskIdList": [1658434],
                    "aliasTaskIdList": [2W1658434],
                    "userId": 100093088
                }

        Returns:
            int: The ID number of the task.

        """
        if not self._has_submit and self._task_id:
            return self._task_id
        task_id_info = self.create_task(count=1, out_user_id=None)
        task_id_list = task_id_info.get("taskIdList")
        if not task_id_list:
            raise RayvisionError(1000000, 'Failed to create task number!')
        self._task_id = task_id_list[0]
        self._has_submit = False
        return self._task_id

    @property
    def task_id(self):
        """int: The ID number of the render task.

        Notes:
            As long as we do not initialize the class again or submit the task
            successfully, we can always continue to get the task id from the
            class instance.

        """
        return self._generate_task_id()

    def submit_task(self, task_id,
                    producer=None,
                    only_id=False):
        """Submit a task to rayvision render farm.

        Args:
            task_id (int): Submit task ID.
            producer (str, optional): Producer.

        """
        data = {
            "taskId": task_id,
        }
        if producer:
            data["producer"] = producer

        task_info = self._connect.post(self._connect.url.task, data)
        if only_id:
            return task_id
        self._has_submit = True
        return task_info

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
        return self._connect.post(self._connect.url.abandonTask,
                                  {self.TASK_PARAM: task_param_list})

    def delete_task(self, task_param_list):
        """Delete task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.deleteTask,
                                  {self.TASK_PARAM: task_param_list})

    def update_priority(self, task_id, priority):
        """Update the render priority for the task by given task id.

        Args:
            task_id (int): The ID number of the render task.
            priority (int): The priority for the current render task.

        """
        data = {
            'taskId': task_id,
            'taskUserLevel': priority,
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
        return self._connect.post(self._connect.url.setTaskOverTimeStop, data)

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
        return self._connect.post(self._connect.url.fullSpeedRendering, data)
