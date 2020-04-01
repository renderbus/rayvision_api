"""The constants of the rayvision_api."""

# The name of the package.
PACKAGE_NAME = 'rayvision_api'

# The all DCC software ID mappings, we can easily get the corresponding
# ``cgId`` from the alias.
DCC_ID_MAPPINGS = {
    'maya': 2000,
    '3ds Max': 2001,
    'lightwave': 2002,
    'arnold': 2003,
    'houdini': 2004,
    'cinema4d': 2005,
    'softimage': 2006,
    'blender': 2007,
    'vr_standalone': 2008,
    'mr_standalone': 2009,
    'sketchup': 2010,
    'vue': 2011,
    'keyshot': 2012,
    'clarisse': 2013,
    'octane_render': 2014,
    'katana': 2016,
}

# The headers of rayvision api.
HEADERS = {
    'accessId': '',
    'channel': '4',
    'platform': '',
    'UTCTimestamp': '',
    'nonce': '',
    'signature': '',
    'version': '1.0.0',
    'Content-Type': 'application/json'
}

# The operators of the rayvision_api.
QUERY_PLATFORMS = '/api/render/common/queryPlatforms'
QUERY_USER_PROFILE = '/api/render/user/queryUserProfile'
QUERY_USER_SETTINGS = '/api/render/user/queryUserSetting'
UPDATE_USER_SETTINGS = '/api/render/user/updateUserSetting'
GET_TRANSFER_BID = '/api/render/task/getTransferBid'
CREATE_TASK = '/api/render/task/createTask'
SUBMIT_TASK = '/api/render/task/submitTask'
QUERY_ERROR_DETAIL = '/api/render/common/queryErrorDetail'
GET_TASK_LIST = '/api/render/task/getTaskList'
STOP_TASK = '/api/render/task/stopTask'
START_TASK = '/api/render/task/startTask'
ABORT_TASK = '/api/render/task/abortTask'
DELETE_TASK = '/api/render/task/deleteTask'
QUERY_TASK_FRAMES = '/api/render/task/queryTaskFrames'
QUERY_ALL_FRAME_STATUS = '/api/render/task/queryAllFrameStats'
RESTART_FAILED_FRAMES = '/api/render/task/restartFailedFrames'
RESTART_FRAME = '/api/render/task/restartFrame'
QUERY_TASK_INFO = '/api/render/task/queryTaskInfo'
ADD_LABEL = '/api/render/common/addLabel'
DELETE_LABEL = '/api/render/common/deleteLabel'
GET_LABEL_LIST = '/api/render/common/getLabelList'
QUERY_SUPPORTED_SOFTWARE = '/api/render/common/querySupportedSoftware'
QUERY_SUPPORTED_PLUGIN = '/api/render/common/querySupportedPlugin'
ADD_RENDER_ENV = '/api/render/common/addRenderEnv'
UPDATE_RENDER_ENV = '/api/render/common/updateRenderEnv'
DELETE_RENDER_ENV = '/api/render/common/deleteRenderEnv'
SET_DEFAULT_RENDER_ENV = '/api/render/common/setDefaultRenderEnv'
GET_RENDER_ENV = '/api/render/common/getRenderEnv'
UPDATE_TASK_USER_LEVEL = '/api/rendering/task/renderingTask/updateTaskUserLevel'
GET_RAYSYNC_USERKEY = '/api/render/user/getRaySyncUserKey'
GET_TRANSFER_SERVER_MSG = '/api/render/task/getTransferServerMsg'
LOAD_TASK_PROCESSING = '/api/render/task/loadTaskProcessImg'
SET_OVER_TIME_STOP = '/api/render/task/setOverTimeStop'
LOADING_FRAME_THUMBNAIL = '/api/render/task/loadingFrameThumbnail'
FULL_SPEED = '/api/render/task/fullSpeed'

CG_SETTING = {
    'Maya': '2000',
    'Houdini': '2004',
    'Katana': '2016',
    'Clarisse': '2013',
    'Blender': '2007',
    '3ds Max': '2001',
    '2000': 'Maya',
    '2004': 'Houdini',
    '2016': 'Katana',
    '2013': 'Clarisse',
    '2007': 'Blender',
    '2001': '3ds Max'
}

TASK_INFO = {
    'task_info': {
        'enable_layered': '0',
        'input_cg_file': '',
        'is_picture': '0',
        'task_id': '',
        'frames_per_task': '1',
        'pre_frames': '000',
        'job_stop_time': '259200',
        'task_stop_time': '0',
        'time_out': '43200',
        'stop_after_test': '2',
        'project_name': '',
        'project_id': '',
        'channel': '4',
        'cg_id': '',
        'platform': '',
        'tiles_type': 'block',
        'tiles': '1',
        'is_layer_rendering': '1',
        'is_distribute_render': '0',
        'distribute_render_node': '3',
        'input_project_path': '',
        'render_layer_type': '0',
        'user_id': '',
        'os_name': '1',
        'ram': '64'
    },
    'software_config': {},
    'scene_info': {},
    'scene_info_render': {}
}

MODIFIABLE_PARAM = [
    'pre_frames',
    'input_cg_file',
    'frames_per_task',
    'test_frames',
    'job_stop_time',
    'task_stop_time',
    'time_out',
    'stop_after_test',
    'tiles_type',
    'tiles',
    'is_layer_rendering',
    'is_distribute_render',
    'distribute_render_node',
    'input_project_path',
    'render_layer_type',
    'os_name',
    'ram',
    'enable_layered',
]


KEYS = ["layers", "scene_info_render", "task_info", "scene_info", "software_config"]
