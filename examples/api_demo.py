#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rayvision_api import RayvisionAPI

user_info = {
    "domain_name": "task.renderbus.com",
    "platform": "2",
    "access_id": "xxxx",
    "access_key": "xxxx",
    "local_os": 'windows',
    "workspace": "c:/workspace",
}

api = RayvisionAPI(access_id=user_info['access_id'],
                   access_key=user_info['access_key'],
                   domain=user_info['domain_name'],
                   platform=user_info['platform'])

print("======= user profile=============")
user_profile = api.user.query_user_profile()
print(user_profile)

print("======= user setting=============")
user_setting = api.user.query_user_setting()
print(user_setting)
