import base64
import re
import time

import requests

def qk():
    cnt = cnt1 = 1
    try:
        while 1:
            for key in courses['jhxk']:
                time.sleep(0.5)
                res = session.get(
                    url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=201820192" + courses['jhxk'][key]
                    # 这个是本学期计划选课
                )
                print(res.text + "第" + str(cnt) + "次尝试" + key)
                cnt += 1

            for key in courses['ggxk']:
                time.sleep(0.5)
                res = session.get(
                    url="http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=201820192" + courses['ggxk'][key]
                    # 这个是本学期计划选课
                )
                print(res.text + "第" + str(cnt) + "次尝试" + key)
                cnt1 += 1
    except:
        print("连接断开，正在尝试重新连接......")
        qk()



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
        'encoded': base64.b64encode(id) + b'%%%' + base64.b64encode(pwd)
    }
)

while 1:
    time.sleep(1)
    res = session.get(
        url="http://csujwc.its.csu.edu.cn/jsxsd/xsxk/xklc_list"
    )
    xkxtUrl = re.search(r'<a\shref="(.*?)"\starget="blank">进入选课</a>', res.text)
    if xkxtUrl:
        xkxtUrl = xkxtUrl.group(1)
        break
    else:
        print("等待选课系统开放中......")

session.get(
    url="http://csujwc.its.csu.edu.cn" + xkxtUrl
)

# 这里放课程
courses = {
    'jhxk': {
        # 包括体育、专业选修
        '体育舞蹈1': "015991",
        '体育保健': "016033",
        '体育舞蹈2': "015988",
        '体育舞蹈3': "015989",
    },
    'ggxk': {
        # 公选课
        # '博弈论解说': "015339",
    }
}
qk()











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
