.. note::
   为了更好的体验本API，请查看是否阅读的是最新版的文档。

初窥 rayvision_api
==================

**rayvision_api** 是基于Python制作用来调用Renderbus云渲染服务的，
- 当你需要从服务器上获取任务相关操作，如 **停止** ， **删除** ， **放弃** 任务等，或者
- 想获取用户的基本信息，你都可以在 `rayvision_api <https://pip.renderbus.com/simple/rayvision-api/>`_  中找到相关的操作方法。


API演示Demo
-----------

学习的最好方法就是参考例子，`rayvision_api <https://pip.renderbus.com/simple/rayvision-api/>`_  也不例外，我们也提供了下面的一个使用 **demo** 样例供您把玩学习::

   from rayvision_api import RayvisionAPI

   user_info = {
        "domain_name": "task.renderbus.com",
        "platform": "2",
        "access_id": "K2lbvJSlPScStv72niHGXZtbQYc5F6hkj",
        "access_key": "6b4b6eab841772113113b61c79db68d85",
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

Demo参数:
-----------

.. list-table:: user_info
   :widths: 15 10 50
   :header-rows: 1

   * - 参数名
     - 参数值
     - 描述
   * - domain_name
     - task.renderbus.com
     - 渲染接口URL
   * - platform
     - 2
     - 平台号ID值
   * - access_id
     - K2lbvJSlPScStv72niHGXZtbQYc5F6hkj
     - 用户开发者中心AccessID（非user_id）
   * - access_key
     - 6b4b6eab841772113113b61c79db68d85
     - 用户开发者中心AccessKey
   * - local_os
     - windows
     - 用户使用系统（window / linux）
   * - workspace
     - c:/workspace
     - 本地文档保存目录（下载目录可自行设置）


获取的结果
-------------

**user_profile** ::

   {'userId': 100150764, 'userName': 'ding625yutao', 'platform': 2, 'phone': '13684998977', 'email': '', 'company': '', 'companySite': '', 'name': '', 'job': '', 'communicationNumber': '', 'softType': 2001, 'softStatus': 1, 'businessType': 0, 'status': 1, 'infoStatus': 0, 'accountType': 1, 'userType': 1, 'mainUserId': 0, 'level': 49, 'pictureLever': 0, 'zone': 1, 'rmbbalance': -2.958, 'usdbalance': 0.0, 'rmbCumulative': 0.0, 'usdCumulative': 0.0, 'credit': 0.0, 'coupon': 0, 'description': '', 'country': '中国', 'city': '广东 中山', 'address': '', 'cpuPrice': 0.67, 'gpuPrice': 20.0, 'gpuSingleDiscount': 0.6, 'extraRamRate': 0.2, 'shareMainCapital': 0, 'subDeleteTask': 0, 'subDeleteCapital': 1, 'useMainBalance': 0, 'hideBalance': 0, 'hideJobCharge': 0, 'useLevelDirectory': 0, 'downloadDisable': 0, 'displaySubaccount': 0, 'subaccountLimits': 5, 'houdiniFlag': 1, 'c4dFlag': 1, 'blenderFlag': 1, 'keyshotFlag': 1, 'studentEndTime': None, 'commonCoupon': 0, 'qyCoupon': 0, 'commonCouponCount': 0, 'qyCouponCount': 0, 'exportFrameConsume': 0, 'availableCredit': -2.958, 'totalCredit': 0.0, 'inviterId': None, 'inviterName': None, 'enableNodeDetails': 0, 'taskNodeLimitPermission': 0}

**user_profile** ::

   {'infoStatus': None, 'accountType': None, 'shareMainCapital': 0, 'subDeleteTask': 0, 'useMainBalance': 0, 'taskOverTime': 12, 'taskOverTimeSec': 43200, 'singleNodeRenderFrames': None, 'maxIgnoreMapFlag': 1, 'autoCommit': None, 'separateAccountFlag': 0, 'mifileSwitchFlag': 0, 'assfileSwitchFlag': 0, 'manuallyStartAnalysisFlag': 0, 'downloadDisable': 0, 'ignoreMapFlag': 0, 'isVrayLicense': 0, 'justUploadConfigFlag': 0, 'justUploadCgFlag': 0, 'mandatoryAnalyseAllAgent': 0, 'downloadLimit': 0}

