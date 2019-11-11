常量参数
-------------------------------

接口使用到的常量参数

.. automodule:: rayvision_api.constants
   :members:
   :undoc-members:
   :show-inheritance:

**所有的DCC软件的ID映射**::

   DCC_ID_MAPPINGS = {
    'maya': 2000,
    '3dsmax': 2001,
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
   }

- 请求头HEADERS::

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

.. warning::
   注意 ``CG_SETTING`` 软件名首字母大写。
**CG Settings**::

   CG_SETTING = {
    'Maya': '2000',
    'Houdini': '2004',
    'Katana': '2016',
    'Clarisse': '2013',
    '2000': 'Maya',
    '2004': 'Houdini',
    '2016': 'Katana',
    '2013': 'Clarisse',
   }

**task_info 默认参数**::

   TASK_INFO = {
    'task_info': {
        'input_cg_file': '',
        'is_picture': '0',
        'task_id': '',
        'frames_per_task': '1',
        'pre_frames': '000',
        'job_stop_time': '86400',
        'task_stop_time': '259200',
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

**可修改参数**::

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
    'ram'
   ]
