rayvision_api
=============

[![](https://img.shields.io/badge/pypi%20package-0.4.4-green)](https://pypi.org/project/rayvision-api/)
[![](https://img.shields.io/badge/docs--%E4%B8%AD%E6%96%87%E7%AE%80%E4%BD%93-latest-green)](https://renderbus.readthedocs.io/zh/latest)
[![](https://img.shields.io/badge/docs--English-latest-green)](https://renderbus.readthedocs.io/en/latest)
[![](https://img.shields.io/badge/license-Apache%202-blue)](http://www.apache.org/licenses/LICENSE-2.0.txt)
![](https://img.shields.io/badge/python-2.7.10+%20%7C%203.6%20%7C%203.7-blue)
![](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)

A Python-based API for Using Renderbus cloud rendering service.

#### 1. 系统要求

​        rayvision_api 可在 Linux和 Windows 上运行。使用python2.7.10+或者python3.6+

#### 2.使用demo

```python
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
```

#### 3. 更多

详细的使用请参考[RenderBus SDK 显示说明书]( https://renderbus.readthedocs.io/zh/latest/index.html  "SDK详细说明书")