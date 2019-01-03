import re

import requests
import base64

session = requests.session()

session.get("http://csujwc.its.csu.edu.cn/jsxsd/")
# id = input("请输入账号：\n")
id = "3901170504"
id = bytes(id, encoding='utf-8')
# pwd = input("输入密码：\n")
pwd = "lou1453687"
pwd = bytes(pwd, encoding='utf-8')
# 登录
session.post(
    url="http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk",
    data={
        'encoded': base64.b64encode(id) + b'%%%'+ base64.b64encode(pwd)
    }
)
res = session.get("http://csujwc.its.csu.edu.cn/jsxsd/xspj/xspj_list.do?pj0502id=73A6E84BBD1A47DCA824BB16AE9440A3&xnxq01id=2018-2019-1")

links = re.finditer(r"/jsxsd/xspj/xspj_edit\.do\?xnxq01id=.*?&pj01id=.*?&pj0502id=.*?&jx02id=.*?&jx0404id=.*?&xsflid=&zpf=.*?&jg0101id=\w+",res.text)
                     # "/jsxsd/xspj/xspj_edit.do?xnxq01id=(.*)&pj01id=(.*)&pj0502id=(.*)&jx02id=(.*)&jx0404id=(.*)&xsflid=&zpf=(.*)&jg0101id=(.*)"
for link in links:
    res = session.get(
        url="http://csujwc.its.csu.edu.cn/" + link.group(),
        headers={
            'Referer': "http://csujwc.its.csu.edu.cn/jsxsd/xspj/xspj_list.do?pj0502id=73A6E84BBD1A47DCA824BB16AE9440A3&xnxq01id=2018-2019-1",
            'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'Upgrade-Insecure-Requests': '1',
            "Host": "csujwc.its.csu.edu.cn",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml + xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7"

    }
                      )
    print(res.text)

# print(res.text)


