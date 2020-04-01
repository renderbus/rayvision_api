#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rayvision_api import RayvisionAPI

render_para = {
    "domain": "task.renderbus.com",  # 用戶不需要修改
    "platform": "2",
    "access_id": "xxxxx",  # 用户自行修改(必填)
    "access_key": "xxxxx",  # 用户自行修改(必填)
}

api = RayvisionAPI(access_id=render_para['access_id'],
                   access_key=render_para['access_key'],
                   domain=render_para['domain'],
                   platform=render_para['platform'])


print("======= 获取平台列表 =============")
platform = api.query.platforms()
print(platform)
#
# print("======= 获取用户详情 =============")
# user_profile = api.user.query_user_profile()
# print(user_profile)
#
# print("======= 获取用户设置 =============")
# user_setting = api.user.query_user_setting()
# print(user_setting)
#
# print("======= 更新用户设置 =============")
# update_user_setting = api.user.update_user_settings(task_over_time=43200)
# print(update_user_setting)
#
# print("======= 获取用户传输BID =============")
# user_transfer_bid = api.user.get_transfer_bid()
# print(user_transfer_bid)
#
# print("======= 创建任务号 =============")
# create_task_id = api.task.create_task(count=1, task_user_level=50, labels=["label_test1"])
# print(create_task_id)

# print("======= 提交任务 =============")
# task_id = create_task_id["taskIdList"][0]
# submit_task = api.task.submit_task(task_id=task_id)
# print(submit_task)

# print("======= 获取分析错误码 =============")
# error_detail = api.query.error_detail(code="601")
# print(error_detail)
#
# print("======= 获取任务列表 =============")
# task_list = api.query.get_task_list(page_num=1, page_size=1)
# print(task_list)
#
# print("======= 停止任务 =============")
# stop_task = api.task.stop_task(task_param_list=[14362099])
# print(stop_task)

# print("======= 开始任务 =============")
# start_task = api.task.start_task(task_param_list=[13798105])
# print(start_task)

# print("======= 放弃任务 =============")
# abort_task = api.task.abort_task(task_param_list=[13798105])
# print(abort_task)

# print("======= 删除任务 =============")
# delete_task = api.task.delete_task(task_param_list=[13798105])
# print(delete_task)

# print("======= 获取任务渲染帧详情 =============")
# task_frame = api.query.task_frames(task_id=13652193, page_num=1, page_size=1)
# print(task_frame)
#
# print("======= 获取任务总渲染帧概况 =============")
# all_frame_status = api.query.all_frame_status()
# print(all_frame_status)

# print("======= 重提失败帧 =============")
# # restart_failed_frames = api.query.restart_failed_frames(task_param_list=[13788981])
# # print(restart_failed_frames)

# print("======= 重提任务指定帧 =============")
# restart_frame = api.query.restart_frame(task_id=14362099, select_all=1)
# print(restart_frame)

# print("======= 获取任务详情 =============")
# task_info = api.query.task_info(task_ids_list=[13652193])
# print(task_info)
#
# print("======= 添加自定义标签 =============")
# add_label_name = api.tag.add_label(new_name="test_tag4", status=0)
# print(add_label_name)

# print("======= 删除自定义标签 =============")
# delete_label_name = api.tag.delete_label(del_name="test_tag2")
# print(delete_label_name)

# print("======= 获取自定义标签 =============")
# label_list = api.tag.get_label_list()
# print(label_list)

# print("======= 获取支持的渲染软件 =============")
# support_software = api.query.supported_software()
# print(support_software)

# print("======= 获取支持的渲染软件插件 =============")
# support_software_plugin = api.query.supported_plugin(name='maya')
# print(support_software_plugin)

# print("======= 新增用户渲染环境配置 =============")
# env = {
#     "cgId": 2000,
#     "cgName": "Maya",
#     "cgVersion": "2020",
#     "renderLayerType": 0,
#     "editName": "testRenderEnv2",
#     "renderSystem": "0",
#     "pluginIds": [1166]
# }
# add_user_env = api.env.add_render_env(render_env=env)
# print(add_user_env)


# print("======= 修改用户渲染环境配置 =============")
# update_env = {
#     "cgId": 2000,
#     "cgName": "Maya",
#     "cgVersion": "2020",
#     "renderLayerType": 0,
#     "editName": "testRenderEnv",
#     "renderSystem": "0",
#     "pluginIds": []
# }
# update_user_env = api.env.update_render_env(render_env=update_env)
# print(update_user_env)

# print("======= 删除用户渲染环境配置 =============")
# delete_user_env = api.env.delete_render_env(edit_name="testRenderEnv")
# print(delete_user_env)

# print("======= 设置默认渲染环境配置 =============")
# set_default_user_env = api.env.set_default_render_env(edit_name="testRenderEnv")
# print(set_default_user_env)

# print("======= 获取用户渲染环境配置 =============")
# user_render_config = api.env.get_render_env(name='houdini')
# print(user_render_config)


# print("======= 任务进度图 =============")
# task_processing_img = api.query.get_task_processing_img(task_id=14470635, frame_type=2)
# print(task_processing_img)

# print("======= 设置任务超时停止时间 =============")
# set_task_overtime = api.task.set_task_overtime_top(task_id_list=[13790691], overtime=60)
# print(set_task_overtime)


# print("======= 加载缩略图 =============")
# frame_thumbnall = api.query.get_frame_thumbnall(frame_id=230772361)
# print(frame_thumbnall)

# print("======= 获取镭速传输信息 =============")
# transfer_server_msg = api.query.get_transfer_server_msg()
# print(transfer_server_msg)

# print("======= 获取镭速验证key =============")
# raysync_user_key = api.query.get_raysync_user_key()
# print(raysync_user_key)


# print("======= 全速渲染 =============")
# full_speed_render = api.task.full_speed(task_id_list=[13652193])
# print(full_speed_render)
