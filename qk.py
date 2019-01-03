import base64

import requests

session = requests.session()
session.get(
    url="http://csujwc.its.csu.edu.cn/jsxsd/"
)

id = input("请输入账号：\n")
id = bytes(id, encoding='utf-8')
pwd = input("输入密码：\n")
pwd = bytes(pwd, encoding='utf-8')
# 登录
session.post(
    url="http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk",
    data={
        'encoded': base64.b64encode(id) + b'%%%'+ base64.b64encode(pwd)
    }
)

# 这一步主要是更新服务端的session状态，伪造已经进入了选课系统，没有这步选课是没有响应的，jx0502zbid这个参数是访问权限，可以向高年级可以进入系统的学长学姐要
session.get(
    url="http://csujwc.its.csu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=36B0F6485A9446E3B5D9829DF9B81CE4"
)

# 这里放课程
courses = {
    '朋辈心理': "016483",
    '社会性别与婚姻家庭': "015389",
    '职业生涯规划': '016427'
}

while 1:
    for key in courses:
        res = session.post(
            url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=201820192" + courses[key]
        )
        print(res.text)

















# 可选的公选课的课程（json）
# sfct参数表示是否过滤冲突课程
# iDisplayLength": "9999999"  显示全部
# res = session.post(
#     url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=",
#     data={
#         "sEcho": "1",
#         "iColumns": "13",
#         "sColumns": "",
#         "iDisplayStart": "0",
#         "iDisplayLength": "9999",
#         "mDataProp_0": "kch",
#         "mDataProp_1": "kcmc",
#         "mDataProp_2": "ktmc",
#         "mDataProp_3": "xf",
#         "mDataProp_4": "skls",
#         "mDataProp_5": "sksj",
#         "mDataProp_6": "skdd",
#         "mDataProp_7": "xkrs",
#         "mDataProp_8": "syrs",
#         "mDataProp_9": "xxrs",
#         "mDataProp_10": "ctsm",
#         "mDataProp_11": "szkcflmc",
#         "mDataProp_12": "czOper"
#     },
#     headers={
#         'Referer':"http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk",
#         'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
#         'Host': "csujwc.its.csu.edu.cn",
#         'Origin': "http://csujwc.its.csu.edu.cn"
#     }
# )

# res = session.post(
#     url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=201820192016461"
# )


# 计划选修列表（json）
# sfct参数表示是否过滤冲突课程
# iDisplayLength": "9999999"  显示全部
# res = session.post(
#     url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/xsxkBxqjhxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=true",
#     data={
#         "sEcho": "1",
#         "iColumns": "13",
#         "sColumns": "",
#         "iDisplayStart": "0",
#         "iDisplayLength": "9999",
#         "mDataProp_0": "kch",
#         "mDataProp_1": "kcmc",
#         "mDataProp_2": "ktmc",
#         "mDataProp_3": "xf",
#         "mDataProp_4": "skls",
#         "mDataProp_5": "sksj",
#         "mDataProp_6": "skdd",
#         "mDataProp_7": "xkrs",
#         "mDataProp_8": "syrs",
#         "mDataProp_9": "xxrs",
#         "mDataProp_10": "ctsm",
#         "mDataProp_11": "xkbtf",
#         "mDataProp_12": "czOper"
#     },
#     headers={
#         'Referer':"http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk",
#         'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
#         'Host': "csujwc.its.csu.edu.cn",
#         'Origin': "http://csujwc.its.csu.edu.cn"
#     }
# )

# res = session.post(
#     url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=201820192016461"
# )
