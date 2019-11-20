from flask import Flask
from flask import render_template,request,session,redirect
import mainFunction
import pickle
import random
import os
from datetime import timedelta
import hashlib


app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=1) #设置session的保存时间。

@app.route('/')
def indexShow():
    '''
        初始化首页
    :return:
    '''
    return dynamic(Account="")

@app.route("/user/register",methods=['POST', 'GET'])
def register():
    '''
        用户注册后的请求页面
    :return:
    '''
    return render_template("/payment.html")

@app.route("/user/login/",methods=['POST', 'GET'])
def login():
    '''
        用户注册的请求与session赋值页面
    :return:
    '''
    session['account'] = None
    print("Access_method",request.method)
    if request.method == "GET":
        return render_template("/login.html")
    if request.method == 'POST':
        print(request.form)
        fileRead = open('TemplateData.txt', 'rb')
        # 打开序列化过后的文件，进行反序列化处理
        golbalData = pickle.load(fileRead)
        users = golbalData["Users"]
        fileRead.close()
        # 这时已经获得所有账号的加密数据，开始进行判断.
        # 需要对传入数据进行md5加密计算
        m = hashlib.md5()
        passwd = request.form.get('password')
        passwd = passwd.encode(encoding='utf-8')
        m.update(passwd)
        passwd_md5 = m.hexdigest()
        # MD5取值完成
        # 循环抽取账号密码进行匹配
        for i in users:
            print(i)
            if request.form.get('account') == i[1] and passwd_md5 == i[2]:
                session['account'] = request.form.get('account')
                print("欢迎登入",session.get('account'))
                break
        # 如果已经登入成功，直接跳转到个人版资源网站
        if session['account'] != None:
            return redirect("/{}".format(session.get('account')))
        #  登入失败则直接跳转到首页
        return redirect("/")
    # 异常则回转登入页面
    return render_template("/login.html")

@app.route("/<string:Account>")
def dynamic(Account):
    '''
        动态，根据用户是否登入，来自动进入个人版。
    :param Account:
    :return:
    '''
    # 打开序列化过后的文件，进行反序列化处理
    fileRead = open('TemplateData.txt', 'rb')
    # 打开序列化过后的文件，进行反序列化处理
    golbalData = pickle.load(fileRead)
    # 获取 全局类 大字典文件。哔哩哔哩字典
    imgData = golbalData["BiliBili"]
    # # 将哔哩哔哩的内容随机取值
    # randomKey = random.choice(list(imgData.keys()))
    # # 将所有哔哩哔哩的内容取值
    # randomValue = imgData[randomKey]
    # ImgData = []
    # # 将按照对应关系进行处理
    # ImgData.append([randomKey,randomValue])
    # # 将SQLmanager的数据进行一下分类
    SqlManger_dynamic_Class = []
    all_Class_Set = set()
    # 循环全部SQLmanager列表获取数据
    for i in golbalData["SqlManger"]:
        all_Class_Set.add(i[2])
    # 开始动态判断
    if Account == "" or Account not in all_Class_Set or session.get("account") == None:
        if Account == "biantai":
            Account = "H"
        else:
            Account = "A"
        SqlManger_dynamic_Class = [ i for i in golbalData["SqlManger"] if i[2] == Account]
    #   当输入的参数不等于空且有值时且等于数据库的时
    elif Account != "" and Account in all_Class_Set:
        # 这里得做账号是否登入判断
        print("当前登入的账号是",session.get("account"))
        # 就算登入了但是想偷看其他人的资源库，也是禁止的，个人只能访问个人的资源库
        if session.get("account") != Account:
            return redirect("/")
        SqlManger_dynamic_Class = [ i for i in golbalData["SqlManger"] if i[2] == Account]
    # 尝试获取首页内容，如果不行，直接赋值为空
    try:
        fileRead_IndexContent = open('IndexContent.txt', 'rb')
        IndexContentDICT = pickle.load(fileRead_IndexContent)
        IndexContent = IndexContentDICT['IndexContent']
    except:
        IndexContent = "暂无公告喵喵喵~~~"
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=SqlManger_dynamic_Class,ImgData=imgData,IndexContent=IndexContent)

@app.route("/post/",methods=['POST', 'GET'])
def IndexPost():
    '''
        公告请求页面。
    :return:
    '''
    # 现在的FLASK根据表单的name获取，而不是表单的ID
    print("Access_method",request.method)
    if request.method == "GET":
        return render_template("/admin/index.html")
    if request.method == 'POST':
        print(request.form)
        if request.form.get('Account') == "lingyunyi" and request.form.get('IndexContent') != "":
            IndexContentDICT = {}
            IndexContentDICT['IndexContent'] = request.form.get('IndexContent')
            print("IndexContentDICT['IndexContent']",request.form.get('IndexContent'))
            # 序列化到全局变量文件中
            fileOpen = open('IndexContent.txt', 'wb')
            pickle.dump(IndexContentDICT, fileOpen)
            fileOpen.close()
    return render_template("/admin/index.html")

@app.route("/payment/")
def payment():
    '''
        静态打赏页面
    :return:
    '''
    return render_template("/payment.html")

@app.route("/admin/")
def admin():
    '''
        用户登入管理界面
    :return:
    '''
#     首先判断是否已经登入个人账号
    if session.get("account") == None:
        # 条状到登入页面
        return redirect("/user/login")
#   如果已经登入，直接进入个人版管理页面


if __name__ == '__main__':
    app.run(debug=True)
