# -*- coding: utf-8 -*-
"""API query operation."""

from rayvision_api import constants


class Query(object):
    """API query operation."""

    def __init__(self, connect):
        """Initialize instance."""
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
        zone = 1 if 'renderbus' in self._connect.domain.lower() else 2
        return self._connect.post(constants.QUERY_PLATFORMS, {'zone': zone})

    def error_detail(self, code, language='0'):
        r"""Get analysis error code.

        Args:
            code (str): Required value, error code.
                e.g.:
                    "10010".
                    "15000".
            language (str, optional): Not required, language,
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
            'code': code,
            'language': language
        }
        details = self._connect.post(constants.QUERY_ERROR_DETAIL, data)
        if details:
            return details
        return None

    def get_task_list(self, page_num=1, page_size=2):
        """Get task list.

        An old to the new row, the old one.

        Args:
            page_num (int): Required value, current page.
            page_size (int): Required value, numbers displayed per page.

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
        return self._connect.post(constants.GET_TASK_LIST, data)

    def task_frames(self, task_id, page_num, page_size,
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
        return self._connect.post(constants.QUERY_TASK_FRAMES, data)

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
        return self._connect.post(constants.QUERY_ALL_FRAME_STATUS)

    def restart_failed_frames(self, task_param_list):
        """Re-submit the failed frame.

        Args:
            task_param_list (list of str): Task ID list.

        """
        data = {
            'taskParam': task_param_list
        }
        self._connect.post(constants.RESTART_FAILED_FRAMES, data)

    def restart_frame(self, task_id, select_all, ids_list=None):
        """Re-submit the specified frame.

        Args:
            task_id (int): Task ID number.
            ids_list (list, optional): Frame ID list, valid when select_all is
                0.
            select_all (int): Whether to re-request all,
                1 all re-raised, 0 specified frame re-request.

        """
        ids_list = ids_list or []
        data = {
            'taskId': task_id,
            'ids': ids_list,
            'selectAll': select_all
        }
        self._connect.post(constants.RESTART_FRAME, data)

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
        return self._connect.post(constants.QUERY_TASK_INFO, data)

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
        return self._connect.post(constants.QUERY_SUPPORTED_SOFTWARE)

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
        cg_id = constants.DCC_ID_MAPPINGS[name]
        data = {'cgId': cg_id}
        return self._connect.post(constants.QUERY_SUPPORTED_PLUGIN, data)
