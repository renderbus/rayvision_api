# -*- coding: utf-8 -*-
"""API query operation."""
import sys

from rayvision_api import constants


class QueryOperator(object):
    """API query operation."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.api.connect.Connect): The connect instance.

        """
        self._connect = connect

    def platforms(self):
        """Get platforms.

        Returns:
            list: Platforms info.
                e.g.:
                     [
                         {
                             "platform": 2,
                             "name": "query_platform_w2"
                         },
                     ]

        """
        zone = 1 if "renderbus" in self._connect.domain.lower() else 2
        return self._connect.post(self._connect.url.queryPlatforms,
                                  {'zone': zone})

    def error_detail(self, code=None, codes=None, language=0):
        r"""Get analysis error code.

        Args:
            code (string): Required value, error code.
                e.g.:
                    10010.
                    15000.
            codes (list for int): error codes
            language (int, optional): Not required, language,
                0: Chinese (default) 1: English.

        Returns:
            list: Detailed list of error messages.
                e.g.:
                     [
                         {
                            "id": 5,
                            "code": "15000",
                            "type": 1,
                            "languageFlag": 0,
                            "desDescriptionCn": "启动 3ds max 卡住或者失败",
                            "desSolutionCn": "1.检查启用对应版本的 3ds max
                                是否有特殊弹窗，有的话手动关闭；\n2.检查操作系
                                统是否设置了高级别的权限",
                            "solutionPath": "
                                http://note.youdao.com/noteshare?id=d8f1ea0c46dfb524af798f6b1d31cf6f",
                            "isRepair": 0,
                            "isDelete": 1,
                            "isOpen": 1,
                            "lastModifyAdmin": "",
                            "updateTime": 1534387709000
                         },
                     ]

        """
        data = {
            'language': language
        }
        if code:
            data['code'] = code
        if codes:
            data['codes'] = codes
        if not code and not codes:
            raise AssertionError("code and codes at least one")

        return self._connect.post(self._connect.url.queryAnalyseErrorDetail, data)

    def get_task_list(self, page_num=1, page_size=100, status_list=None,
                      search_keyword=None,
                      start_time=None, end_time=None):
        """Get task list.

        An old to the new row, the old one.

        Args:
            page_num (int): Required value, current page.
            page_size (int): Required value, numbers displayed per page.
            status_list (list<int>): status code list，query the status of the task in the list.
            search_keyword (string): Optional, scenario name or job ID.
            start_time (string): Optional, search limit for start time.
            end_time (string): Optional, search limit for end time.

        Returns:
            dict: Task info, please see the documentation for details.
                e.g.:
                    {
                        "pageCount": 32,
                        "pageNum": 1,
                        "total": 32,
                        "size": 1,
                        "items": [
                            {
                                "sceneName": "衣帽间.max",
                                "id": 18278,
                                "taskAlias": "P18278",
                                "taskStatus": 0,
                                "statusText": "render_task_status_0",
                                "preTaskStatus": 25,
                                "preStatusText": "render_task_status_25",
                                "totalFrames": 0,
                                "abortFrames": null,
                                "executingFrames": null,
                            },
                        ]
                    }

        """
        data = {
            'pageNum': page_num,
            'pageSize': page_size
        }
        if status_list:
            data['statusList'] = status_list
        if search_keyword:
            data['searchKeyword'] = search_keyword
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        return self._connect.post(self._connect.url.getTaskList, data)

    def task_frames(self, task_id, page_num=1, page_size=100,
                    search_keyword=None):
        """Get task rendering frame details.

        Args:
            task_id (int): The task ID number,
                which is the unique identifier of the task, required field.
            page_num (int): Current page number.
            page_size (int): Displayed data size per page.
            search_keyword (str, optional): Is a string, which is queried
                according to the name of a multi-frame name of a machine
                rendering, optional.

        Returns:
            dict: Frames info list, please see the documentation for details.
                e.g.:
                    {
                        "pageCount": 9,
                        "pageNum": 1,
                        "total": 17,
                        "size": 2,
                        "items": [
                            {
                                "id": 1546598,
                                "userId": null,
                                "framePrice": null,
                                "feeType": null,
                                "platform": null,
                                "frameIndex": "0-1",
                                "frameStatus": 4,
                                "feeAmount": 0.44,
                                "startTime": 1535960273000,
                                "endTime": 1535960762000,
                            },
                        ],
                    }

        """
        data = {
            'taskId': task_id,
            'pageNum': page_num,
            'pageSize': page_size
        }
        if search_keyword:
            data['searchKeyword'] = search_keyword
        return self._connect.post(self._connect.url.queryTaskFrames, data)

    def all_frame_status(self):
        """Get the overview of task rendering frame.

        Returns:
            dict: Frames status info.
                e.g.:
                    {
                        "executingFramesTotal": 1,
                        "doneFramesTotal": 308,
                        "failedFramesTotal": 2,
                        "waitingFramesTotal": 153,
                        "totalFrames": 577
                    }

        """
        return self._connect.post(self._connect.url.queryAllFrameStats,
                                  validator=False)

    def restart_failed_frames(self, task_param_list, status=None):
        """Replay failed frames for large tasks.

        Args:
            task_param_list (list of str): Task ID list.
            status (list for int): task status

        """
        data = {
            'taskIds': task_param_list
        }
        if status:
            data['status'] = status
        return self._connect.post(self._connect.url.recommitTasks, data)

    def restart_frame(self, task_id, select_all=1, ids_list=None, status=None):
        """Re-submit the specified frame.

        Args:
            task_id (int): Task ID number.
            ids_list (list, optional): Frame ID list, valid when select_all is
                0.
            select_all (int, optional): Whether to re-request all,
                1 represents the user select all operation,
                0 represents the user is not all selected,
                taskId is required when filling in 1, or ids is required when filling in 0 or not.
            status (list for int, optional): Specifies the state of the reframe.
        """
        if select_all == 1:
            if task_id:
                data = {
                    'taskId': task_id,
                    'selectAll': select_all
                }
            else:
                raise AttributeError("task_id is required when select_all is 1")
        else:
            if ids_list:
                data = {
                    'taskId': task_id,
                    'ids': ids_list,
                    'selectAll': select_all
                }
            else:
                raise AttributeError("ids is required when select_all is 0")

        if status:
            data['status'] = status

        return self._connect.post(self._connect.url.recommitTaskFrames, data)

    def task_info(self, task_ids_list):
        """Get task details.

        Args:
            task_ids_list (list of int): Shell task ID list.

        Returns:
            dict: Task details.
                e.g.:
                    {
                        "pageCount": 1,
                        "pageNum": 1,
                        "total": 1,
                        "size": 100,
                        "items": [
                            {
                                "sceneName": "3d66.com_593362_2018.max",
                                "id": 19084,
                                "taskAlias": "P19084",
                                "taskStatus": 0,
                                "statusText": "render_task_status_0",
                                "preTaskStatus": 25,
                                "preStatusText": "render_task_status_25",
                                "totalFrames": 0,
                                "abortFrames": null,
                                "executingFrames": null,
                                "doneFrames": null,
                                "failedFrames": 0,
                                "framesRange": "0",
                                "projectName": "",
                                "renderConsume": null,
                                "taskArrears": 0,
                                "submitDate": 1535958477000,
                                "startTime": null,
                                "completedDate": null,
                                "renderDuration": null,
                                "userName": "xiaoguotu_ljian",
                                "producer": null,
                                "taskLevel": 60,
                                "taskUserLevel": 0,
                                "taskLimit": null,
                                "taskOverTime": null,
                                "userId": 10001520,
                                "outputFileName": null,
                                "munuTaskId": "",
                                "layerParentId": 0,
                                "cgId": 2001,
                                "taskKeyValueVo": {
                                    "tiles": null,
                                    "allCamera": null,
                                    "renderableCamera": null
                                }
                            }
                        "userAccountConsume": null
                    }

        """
        data = {
            'taskIds': task_ids_list
        }
        return self._connect.post(self._connect.url.queryTaskInfo, data)

    def supported_software(self):
        """Get supported rendering software.

        Returns:
            dict: Software info.
                e.g.:
                    {
                        "isAutoCommit": 2,
                        "renderInfoList": [
                            {
                                "cgId": 2000,
                                "cgName": "Maya",
                                "cgType": "ma;mb",
                                "iconPath": "/img/softimage/maya.png",
                                "isNeedProjectPath": 3,
                                "isNeedAnalyse": 1,
                                "isSupportLinux": 1
                            }
                        ],
                        "defaultCgId": 2001
                    }

        """
        return self._connect.post(self._connect.url.querySoftwareList,
                                  validator=False)

    def supported_plugin(self, name):
        """Get supported rendering software plugins.

        Args:
            name (str): The name of the DCC.
                e.g.:
                    maya,
                    houdini

        Returns:
            dict: Plugin info.
                e.g.:
                    {
                        "cgPlugin": [
                            {
                                "cvId": 19,
                                "pluginName": "zblur",
                                "pluginVersions": [
                                    {
                                        "pluginId": 1652,
                                        "pluginName": "zblur",
                                        "pluginVersion": "zblur 2.02.019"
                                    }
                                ]
                            },
                        ],
                        "cgVersion": [
                            {
                                "id": 23,
                                "cgId": 2005,
                                "cgName": "CINEMA 4D",
                                "cgVersion": "R19"
                            }
                        ]
                    }

        """
        cg_id = constants.DCC_ID_MAPPINGS[name.strip()]
        platform = "windows" if sys.platform.startswith("win") else "linux"
        data = {'cgId': cg_id, 'osName': platform}
        return self._connect.post(self._connect.url.querySoftwareDetail, data)

    def get_transfer_server_msg(self):
        """Get the user rendering environment configuration.

        Returns:
            dict: Connect raysync information.
                Example:
                    {
                        'raysyncTransfer': {
                            'port': 2542,
                            'proxyIp': 'render.raysync.cn',
                            'proxyPort': 32011,
                            'serverIp': '127.0.0.1',
                            'serverPort': 2121,
                            'sslPort': 2543
                        }
                    }

        """
        zone = 1 if "renderbus" not in self._connect.domain else 2
        data = {
            "zone": zone
        }
        return self._connect.post(self._connect.url.getServerInfo, data)

    def get_raysync_user_key(self):
        """Get the user rendering environment configuration.

        Returns:
            dict: User login raysync information.
                Example:
                    {
                        'raySyncUserKey': '8ccb94d67c1e4c17fd0691c02ab7f753cea64e3d',
                        'userName': 'test',
                        'platform': 2,
                    }

        """
        return self._connect.post(self._connect.url.getRaySyncUserKey, validator=False)

    def get_task_processing_img(self, task_id, frame_type=None):
        """Get the task progress diagram,currently only Max software is supported.

        Args:
            task_id (int): Task id.
            frame_type (int): Apply colours to a drawing type, nonessential 2
                represents the photon frame, 5 gets the main picture progress,
                and returns the result dynamically according to the stage of
                the rendering task
            Example:
                {
                    "taskId":389406
                }

        Returns: Task progress diagram information
            dict:
                Example:
                    {
                        "block":16,
                        "currentTaskType":"Render",
                        "grabInfo":[
                            [
                                {
                                    "couponFee":"0.00",
                                    "frameIndex":"0",
                                    "renderInfo":"",
                                    "frameBlock":"1",
                                    "frameEst":"0",
                                    "grabUrl":"/mnt/output/d20/small_pic/10001500/10001834/389406/Render_2018110900083_0_frame_0[_]block_0[_]_STP00000_Renderbus_0000[-]tga.jpg",
                                    "feeAmount":"0.20",
                                    "frameUsed":"66",
                                    "frameStatus":"4",
                                    "framePercent":"100",
                                    "isMaxPrice":"0",
                                    "startTime":"2018-11-09 18:28:26",
                                    "endTime":"2018-11-09 18:29:32"
                                }
                            ]
                        ],
                        "height":1500,
                        "sceneName":"com_589250.max-Camera007",
                        "startTime":"2018-11-09 18:27:40",
                        "width":2000
                    }

        """
        data = {
            "taskId": task_id
        }
        if frame_type:
            data["frameType"] = frame_type
        return self._connect.post(self._connect.url.loadTaskProcessImg, data)

    def get_frame_thumbnall(self, frame_id, frame_status=4):
        """Load thumbnail.

        Args:
            frame_id (int): Frame id.
            frame_status (int): State of the frame, only complete with
                thumbnails.

        Returns:
            list: Thumbnail path.
                Example:
                    [
                        "small_pic\\100000\\100001\\138\\Render_264_renderbus_0008[-]jpg.jpg"
                    ]

        """
        data = {
            'id': frame_id,
            'frameStatus': frame_status
        }
        return self._connect.post(self._connect.url.loadingFrameThumbnail,
                                  data)

    def get_all_frames(self, task_id, start_page=1, end_page=2000, page_size=100):
        """Gets all frame details for the specified task.

        Args:
            task_id (int) : small task id
            start_page (int) : The start page that you want to query.
            end_page (int) : The end page that you want to query.

        Returns (dict): all frames detail info.

        """
        frames_detail = dict()
        for num in range(int(start_page), int(end_page)+1):
            task_frame = self.task_frames(task_id=int(task_id), page_num=num, page_size=page_size)
            if task_frame['items']:
                for per in task_frame['items']:
                    frame_index = per["frameIndex"]
                    frames_detail[frame_index] = per
            else:
                break
        return frames_detail

    def get_custome_frames(self, task_id, restartframes):
        """Retrieves the frame of the specified task according to the frame。

        Args:
            task_id (int) : small task id
            restartframes (list) : The frame number needs to be redrawn.
                Examples:
                     ["2-4[1]", "10"]

        """
        all_frames = self.get_all_frames(task_id)
        ids = [per["id"] for index, per in all_frames.items() if str(index) in restartframes]
        restart_frame = self.restart_frame(ids_list=ids, select_all=0, task_id=task_id)
        return restart_frame
