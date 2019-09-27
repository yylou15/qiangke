import requests,json,os,time,re,base64,sys
import platform as pf
try:
    import tkinter
    from tkinter import ttk
    guiFlag=True
except:
    print("导入tk库失败，图形预览不可用")
    guiFlag=False
getList_dt={
        "sEcho":"1",
        "iColumns":"13",
        "sColumns":"",
        "iDisplayLength":"9999",
        "iDisplayStart":"0",
        "mDataProp_0":"kch",
        "mDataProp_1":"kcmc",
        "mDataProp_2":"ktmc",
        "mDataProp_3":"xf",
        "mDataProp_4":"skls",
        "mDataProp_5":"sksj",
        "mDataProp_6":"skdd",
        "mDataProp_7":"xkrs",
        "mDataProp_8":"syrs",
        "mDataProp_9":"xxrs",
        "mDataProp_10":"ctsm",
        "mDataProp_11":"xkbtf",
        "mDataProp_12":"czOper"
    }
def resource_path(relative_path):
	if pf.system()=="Windows":
		p=sys.argv[0]
		p=p[:p.rfind('\\')+1]
		return p+relative_path
	elif pf.system()=="Linux":
		relative_path=relative_path.replace("\\","/")
		return sys.path[0]+relative_path
	else:
		relative_path=relative_path.replace("\\","/")
		return sys.path[0]+relative_path

def refreshSession():
    global ses
    ses = requests.session()
    ses.headers={
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Origin":"http://jwctest.its.csu.edu.cn",
        "Host":"jwctest.its.csu.edu.cn",
        "Proxy-Connection":"keep-alive",
        "Referer":"http://jwctest.its.csu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
    }
    ses.get(
        url="http://csujwc.its.csu.edu.cn/jsxsd/"
    ) # 拿JSESSIONID和BIGipServerpool_jwctest
refreshSession()

def reAuth():
    ses.post(url="http://csujwc.its.csu.edu.cn/jsxsd/xk/LoginToXk",data=AuthData)

try: # 懒人认证功能
    authFile=open(resource_path("auth.log"),"r")
    conf1=input("使用上次的身份验证？[Use previous authenticate?](Y/n)")
    if conf1!="n" and conf1!="N" and conf1!="no" and conf1!="No" and conf1!="NO" and conf1!="oN":
        a=authFile.readlines()
        AuthData={"encoded":bytes(a[0],"utf-8")+b'%%%'+bytes(a[1],"utf-8")}
        reAuth()
    else:
        raise NameError("Manual Auth")
    authFile.close()
except Exception as e:
    print(e)
    id = input("请输入账号：\n")
    id = bytes(id, encoding='utf-8')
    pwd = input("输入密码：\n")
    pwd = bytes(pwd, encoding='utf-8')
    # 登录
    AuthData={'encoded': base64.b64encode(id) + b'%%%' + base64.b64encode(pwd)}
    reAuth()
    with open(resource_path("auth.log"),"w") as f:
        f.write(str(base64.b64encode(id),"utf-8") + "\n" + str(base64.b64encode(pwd),"utf-8"))

Courses=[]
def refreshCourses():
    global Courses
    Courses=[]
    #ses.headers["Referer"]="http://jwctest.its.csu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk"
    getList_res=ses.post(getList_lnk,data=getList_dt)
    #print(getList_res.text)
    print("=====================")
    getList_json=json.loads(getList_res.text)
    try:
        with open(resource_path("courses.bak"),"w") as fbak:
            pass
        for i in getList_json["aaData"]:
            Courses.append({
                "Lesson_Name":i["ktmc"],
                "Lesson_Type":i["kcmc"],
                "Teachers":i["skls"],
                "Study_Score":i["xf"],
                "Time":i["sksj"],
                "Place":i["skdd"],
                "Remain":i["syrs"],
                "Max":i["xxrs"],
                "Subsidy":i["xkbtf"],# 补贴分
                "Request_ID":i["jx0404id"]
            })
            print(json.dumps(Courses[-1])+"\n")
            with open(resource_path("courses.bak"),"a") as fbak:
                fbak.write(json.dumps(Courses[-1])+"\n")
        print("Done!Results are in courses.bak")
    except Exception as e:
        print(e)
        print("refresh Courses failed!")

def fixCookie():
    retryTime=0
    while 1:
        res = ses.get("http://csujwc.its.csu.edu.cn/jsxsd/xsxk/xklc_list")
        URLs = re.findall(r'<a\shref="(.*?)"\starget="blank">进入选课</a>', res.text)
        if len(URLs)>1:
            for i in range(len(URLs)):
                print(i,URLs[i])
            try:
                ress=ses.get("http://csujwc.its.csu.edu.cn"+URLs[int(input("进入哪个选课页？输入序号。[Use which select page?Enter the num_tag]:"))])
                break
            except Exception as e:
                print(e)
        elif len(URLs)==1:
            ress=ses.get("http://csujwc.its.csu.edu.cn"+URLs[0])
            break
        else:
            print("等待选课系统开放中...已经尝试%d次"%retryTime)
            time.sleep(5)
            retryTime+=1

    getFakeList_lnk="http://jwctest.its.csu.edu.cn"+re.findall('''<a href="(.*?)" target="mainFrame">本学期计划选课</a>.*?''',ress.text)[0]
    tempR=ses.get(getFakeList_lnk).text
    global getList_lnk
    getList_lnk="http://jwctest.its.csu.edu.cn"+re.findall('''"sAjaxSource":"(.*?)"\\+param,.*?''',tempR)[0]+"?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false"

    # kcxx 课程信息
    # skls 上课老师
    # skxq 上课星期
    # skjc 上课节次
    # sfym 是否已满
    # sfct 是否冲突

try: # 查询可选课程列表
    with open(resource_path("courses.bak"),"r") as f:
        conf1=input("使用上次的选课查询结果？[Use previous query result?](Y/n)")
        if conf1!="n" and conf1!="N" and conf1!="no" and conf1!="No" and conf1!="NO" and conf1!="oN":
            for i in f.readlines():
                Courses.append(json.loads(i))
            
        else:
            raise NameError("Redo query")
except Exception as e:
    print(e)
     # 获取选课查询链接
    fixCookie()
    

    
    refreshCourses()

selectCode=0
print("表格数据建立完成")
print("伪交互模块启动，输入help或者h查看帮助")
while 1:
    cmd=input(">>>")
    if cmd=="h" or cmd=="help":
        print("简写\t命令\t说明")
        print("h\thelp\t打印此帮助信息")
        print("e\teval\t进入eval命令执行模式，调试用")
        print("s\tselect\t输入欲选课的下标序号（在新的一行里）")
        print("rec\trefreshcourses\t重新获取可选课列表")
        print("rea\trefreshauth\t重新登录")
        print("res\trefreshsession\t重新获取会话，用后自动重新登录（慎用）")
        print("sh\tshow\t命令行展示可选课列表，请确保命令框够大")
        print("stk\tshowintkinter\t用tk库展示可选课列表")
        print("d\tdo\t开始抢课，使用前请先用s设置目的课")
        print("q\tquit\t退出")
    elif cmd=="e" or cmd=="eval":
        print("eval模式已启动，输入q回到上级")
        try:
            while 1:
                evalcmd=input(">>>")
                if evalcmd=="q":
                    break
                else:
                    print(eval(evalcmd))
        except KeyboardInterrupt:
            print("键盘打断，回到上级")
    elif cmd=="s" or cmd=="select":
        try:
            selectCode=int(Courses[int(input("下标序号（从零开始的，并不是行号）:"))]["Request_ID"])
            print(selectCode)
        except Exception as e:
            print(e)
            print("更新选课代码失败")
    elif cmd=="rec" or cmd=="refreshcourses":
        fixCookie()
        refreshCourses()
    elif cmd=="rea" or cmd=="refreshauth":
        reAuth()
    elif cmd=="res" or cmd=="refreshsession":
        refreshSession()
        reAuth()
    elif cmd=="sh" or cmd=="show":
        print("下标\t课名\t类型\t教师\t学分\t时间\t地点\t剩余人数\t人数上限\t补贴分\t请求ID")
        for i in range(len(Courses)):
            print(i,Courses[i]["Lesson_Name"],Courses[i]["Lesson_Type"],Courses[i]["Teachers"],Courses[i]["Study_Score"],Courses[i]["Time"],Courses[i]["Place"],Courses[i]["Remain"],Courses[i]["Max"],Courses[i]["Subsidy"],Courses[i]["Request_ID"],sep="\t")
    elif cmd=="stk" or cmd=="showintkinter":
        rt=tkinter.Tk()
        rt.title("Courses Graphic View")
        rt.geometry("1700x900")
        tree_view=ttk.Treeview(rt)
        tree_view["columns"]=["i","n","c","t","s","ti","p","r","m","su","rid"]
        tree_view.pack(expand=1,fill="both")
        tree_view.column("i",width=30)
        tree_view.column("n",width=150)
        tree_view.column("c",width=150)
        tree_view.column("t",width=90)
        tree_view.column("s",width=30)
        tree_view.column("ti",width=400)
        tree_view.column("p",width=150)
        tree_view.column("r",width=50)
        tree_view.column("m",width=50)
        tree_view.column("su",width=30)
        tree_view.column("rid",width=150)
        tree_view.heading("i",text="下标")
        tree_view.heading("n",text="课名")
        tree_view.heading("c",text="类型")
        tree_view.heading("t",text="教师")
        tree_view.heading("s",text="学分")
        tree_view.heading("ti",text="时间")
        tree_view.heading("p",text="地点")
        tree_view.heading("r",text="剩余人数")
        tree_view.heading("m",text="人数上限")
        tree_view.heading("su",text="补贴分")
        tree_view.heading("rid",text="请求id")
        for i in range(len(Courses)):
            tree_view.insert("",i,values=(i,Courses[i]["Lesson_Name"],Courses[i]["Lesson_Type"],Courses[i]["Teachers"],Courses[i]["Study_Score"],Courses[i]["Time"],Courses[i]["Place"],Courses[i]["Remain"],Courses[i]["Max"],Courses[i]["Subsidy"],Courses[i]["Request_ID"]))
        rt.mainloop()
    elif cmd=="d" or cmd=="do":
        if selectCode==0:
            print("请先运行s以确认选课！")
            continue
        lnk = "http://jwctest.its.csu.edu.cn/jsxsd/xsxkkc/bxqjhxkOper?jx0404id=%d&xkzy=&trjf=" % selectCode
        try:
            try:
                do_result=ses.get(lnk,timeout=2)
                print(lnk)
                print(do_result)
                print(do_result.headers)
                print(do_result.text)
                
                        
            except Exception as e:
                print(e)
                print("错误断点1")
                
            try:
                do_json=json.loads(do_result.text)
                while do_json["success"]!=True:
                    try:
                        do_result=ses.get(lnk,timeout=1)
                        do_json=json.loads(do_result.text)
                        print(do_json)
                    except Exception as ex:
                        print(ex)
                        print("于while内部错误")
                print("抢课成功，命令回显:",do_json)
            except Exception as e:
                print(e)
                print("错误断点2,建议运行rec")
        except KeyboardInterrupt:
            print("通过键盘打断,抢课终止")
    elif cmd=="q" or cmd=="quit":
        break
    else:
        print("无法理解的命令:",cmd)

