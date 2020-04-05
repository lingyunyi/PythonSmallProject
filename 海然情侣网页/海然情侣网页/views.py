from django.http import request
from django.shortcuts import redirect,render,HttpResponse
from .Tools.mysql_manager import SqlManger

import datetime,os,time,random



def index(request):
    '''
        首页
    '''
    # 首页目前没有内容直接跳转至日志页面
    return redirect('/diary/')



def diary(request):
    '''
        日志页面
    '''
    '''
           纪念日页面
       '''
    sqltool = SqlManger()
    # 获取当前时间
    now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    # 如果请求为GET请求
    if request.method == "GET":
        # 执行SQL语句
        sql = '''SELECT * from diary limit 0,18'''
        results = sqltool.search(sql)
        bigdata2,imglist,randomcolor = commond(results)
    # 如果请求为POST请求
    elif request.method == "POST":

        # 获取POST请求数据
        post_data = request.POST
        # 构造SQL语句
        content = post_data['content']
        # 注入过滤
        content = str(content).replace("'", "").replace('\\', "").replace('"', "").strip(" ").replace("select","").replace("insert", "")
        if content == "":
            # 输入为空直接跳转，可做后续操作
            return redirect('/diary')
        # 注入过滤
        sql = '''insert into diary(content,create_day) values ('%s','%s')''' % (content, now)
        sqltool.insert(sql)
        return redirect('/diary/')
    return render(request, r"diary.html", {"bigdata": bigdata2, "imglist": imglist,"color":randomcolor})


def diary_del(request):
    if request.method == "GET":
        nid = request.GET["nid"]
        nid = str(nid).replace("'", "").replace('\\', "").replace('"', "").strip(" ").replace("select","").replace("insert", "")
        if nid == "":
            # 输入为空直接跳转，可做后续操作
            return redirect('/diary/')
        sqltool = SqlManger()
        sql = '''delete from diary where id = '%s'     '''%nid
        sqltool.insert(sql)
    return redirect('/diary/')


def memorial_day(request):
    '''
        纪念日页面
    '''
    sqltool = SqlManger()
    # 获取当前时间
    now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    # 如果请求为GET请求
    if request.method == "GET":
        # 执行SQL语句
        sql = '''SELECT * from memorial limit 0,18'''
        results = sqltool.search(sql)
        bigdata2,imglist,randomcolor = commond(results)
    # 如果请求为POST请求

    elif request.method == "POST":

        # 获取POST请求数据
        post_data = request.POST
        # 构造SQL语句
        content = post_data['content']
        # 注入过滤
        content = str(content).replace("'", "").replace('\\', "").replace('"', "").strip(" ").replace("select","").replace("insert", "")
        if content == "":
            # 输入为空直接跳转，可做后续操作
            return redirect('/diary')
        # 注入过滤
        if request.POST["year"] != "" and request.POST["month"] != "" and request.POST["day"] != "":
            year = request.POST["year"]
            month = request.POST["month"]
            day = request.POST["day"]
            now = "%s-%s-%s"%(year,month,day)
        sql = '''insert into memorial(content,create_day) values ('%s','%s')'''%(content,now)
        sqltool.insert(sql)
        return redirect('/memorial_day/')

    # 获取年月日
    year = []
    month = []
    day = []
    y_m_d = now.split("-")
    for i in range(int(y_m_d[0])-30,int(y_m_d[0])+1):
        year.append(i)
    for i in range(0,int(y_m_d[1])):
        month.append(i)
    for i in range(0,int(y_m_d[2])):
        month.append(i)
    year.reverse()
    month.reverse()
    day.reverse()

    return render(request, r"memorial_day.html",{"bigdata":bigdata2,"imglist":imglist,"color":randomcolor,
                                                 "year":year,"month":month,"day":month,
                                                 })


def memorial_day_del(request):
    if request.method == "GET":
        nid = request.GET["nid"]
        nid = str(nid).replace("'", "").replace('\\', "").replace('"', "").strip(" ").replace("select","").replace("insert", "")
        if nid == "":
            # 输入为空直接跳转，可做后续操作
            return redirect('/memorial_day/')
        sqltool = SqlManger()
        sql = '''delete from memorial where id = '%s'     '''%nid
        sqltool.insert(sql)
    return redirect('/memorial_day/')


def commond(results):
    '''

    '''
    now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    bigdata = list(results)
    bigdata.reverse()
    bigdata2 = []
    for i in bigdata:
        if i[3] != "":
            d1 = datetime.datetime.strptime(i[3], "%Y-%m-%d")
            d2 = datetime.datetime.strptime(now, "%Y-%m-%d")
            span = (d2 - d1).days
            print(span)
            ii = list(i)
            ii.insert(0,span)
            ii.append(random.choice(["success","info","warning","danger"]))
            bigdata2.append(ii)
    #         进行二维数据排列
    bigdata3 = sorted(bigdata2, key = lambda x:x[0])
    print("数据时",bigdata3)
    # 获取所有需要滚动的图片
    files = os.listdir("./static/images/switch_img")
    imglist = []
    for i in files:
        imglist.append("/static/images/switch_img/{}".format(i))
    print(imglist)
    randomcolor = random.choice(["success","info","warning","danger"])
    return bigdata3,imglist,randomcolor