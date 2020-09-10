from enum import Enum


def assemble_api_url(domain, operators, protocol='https'):
    """Assemble the requests api url."""
    return '{}://{}{}'.format(protocol, domain, operators)


class ApiUrl(str, Enum):
    queryPlatforms = '/api/render/common/queryPlatforms'
    queryUserProfile = '/api/render/setUp/queryUserProfile'
    queryUserSetting = '/api/render/setUp/queryUserSetting'
    updateUserSetting = '/api/render/setUp/updateUserSetting'
    getBid = '/api/render/transfer/getBid'
    createTask = '/api/render/submit/createTask'
    task = '/api/render/submit/task'
    queryAnalyseErrorDetail = '/api/render/submit/queryAnalyseErrorDetail'
    getTaskList = '/api/render/handle/getTaskList'
    stopTask = '/api/rendering/task/renderingTask/stopTask'
    startTask = '/api/rendering/task/renderingTask/startTask'
    abandonTask = '/api/render/handle/abandonTask'
    deleteTask = '/api/render/handle/deleteTask'
    queryTaskFrames = '/api/render/handle/queryTaskFrames'
    queryAllFrameStats = '/api/render/handle/queryAllFrameStats'
    recommitTasks = '/api/render/handle/recommitTasks'
    recommitTaskFrames = '/api/render/handle/recommitTaskFrames'
    queryTaskInfo = '/api/render/handle/queryTaskInfo'
    add = '/api/render/project/add'
    delete = '/api/render/project/delete'
    getList = '/api/render/project/getList'
    querySoftwareList = '/api/render/plugin/querySoftwareList'
    querySoftwareDetail = '/api/render/plugin/querySoftwareDetail'
    addUserPluginConfig = '/api/render/plugin/addUserPluginConfig'
    editUserPluginConfig = '/api/render/plugin/editUserPluginConfig'
    deleteUserPluginConfig = '/api/render/plugin/deleteUserPluginConfig'
    setDefaultUserPluginConfig = '/api/render/plugin/setDefaultUserPluginConfig'
    getUserPluginConfig = '/api/render/plugin/getUserPluginConfig'
    updateTaskUserLevel = '/api/rendering/task/renderingTask/updateTaskUserLevel'
    getRaySyncUserKey = '/api/render/transfer/getRaySyncUserKey'
    getServerInfo = '/api/render/transfer/getServerInfo'
    loadTaskProcessImg = '/api/render/handle/loadTaskProcessImg'
    setTaskOverTimeStop = '/api/render/handle/setTaskOverTimeStop'
    loadingFrameThumbnail = '/api/render/handle/loadingFrameThumbnail'
    fullSpeedRendering = '/api/render/handle/fullSpeedRendering'
    taskJsonFile = '/api/render/submit/taskJsonFile'
    getConfig = '/api/render/transfer/getConfig'
    addTaskLabel = '/api/render/handle/addTaskLabel'
    deleteTaskLabel = '/api/render/handle/deleteTaskLabel'
