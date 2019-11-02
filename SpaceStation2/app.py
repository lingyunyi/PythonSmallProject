from flask import Flask
from flask import render_template,request
import mainFunction
import pickle
import random

app = Flask(__name__)


@app.route('/')
def indexShow():
    # 打开序列化过后的文件，进行反序列化处理
    fileRead = open('TemplateData.txt', 'rb')
    # 打开序列化过后的文件，进行反序列化处理
    golbalData = pickle.load(fileRead)
    # 获取 全局类 大字典文件。哔哩哔哩字典
    imgData = golbalData["BiliBili"]
    # 将哔哩哔哩的内容随机取值
    randomKey = random.choice(list(imgData.keys()))
    # 将所有哔哩哔哩的内容取值
    randomValue = imgData[randomKey]
    ImgData = []
    # 将按照对应关系进行处理
    ImgData.append([randomKey,randomValue])
    # 将SQLmanager的数据进行一下分类
    SqlManger_Class_A = []
    # 循环全部SQLmanager列表获取数据
    for i in golbalData["SqlManger"]:
        # 判断是否等于A类
        if i[2] == "A":
            SqlManger_Class_A.append(i)
    # 尝试获取首页内容，如果不行，直接赋值为空
    try:
        IndexContent = golbalData["IndexContent"]
    except:
        IndexContent = "暂无公告......"
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=SqlManger_Class_A,ImgData=ImgData,IndexContent=IndexContent)

@app.route("/biantai/")
def biantai():
    # 打开序列化过后的文件，进行反序列化处理
    fileRead = open('TemplateData.txt', 'rb')
    # 打开序列化过后的文件，进行反序列化处理
    golbalData = pickle.load(fileRead)
    # 获取 全局类 大字典文件。哔哩哔哩字典
    imgData = golbalData["BiliBili"]
    # 将哔哩哔哩的内容随机取值
    randomKey = random.choice(list(imgData.keys()))
    # 将所有哔哩哔哩的内容取值
    randomValue = imgData[randomKey]
    ImgData = []
    # 将按照对应关系进行处理
    ImgData.append([randomKey,randomValue])
    # 将SQLmanager的数据进行一下分类
    SqlManger_Class_H = []
    # 循环全部SQLmanager列表获取数据
    for i in golbalData["SqlManger"]:
        # 判断是否等于A类
        if i[2] == "H":
            SqlManger_Class_H.append(i)
    # 尝试获取首页内容，如果不行，直接赋值为空
    try:
        IndexContent = golbalData["IndexContent"]
    except:
        IndexContent = "暂无公告......"
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=SqlManger_Class_H,ImgData=ImgData,IndexContent=IndexContent)

@app.route("/admin/",methods=['POST', 'GET'])
def IndexPost():
    # 现在的FLASK根据表单的name获取，而不是表单的ID
    print("Access_method",request.method)
    if request.method == "GET":
        return render_template("/admin/index.html")
    if request.method == 'POST':
        print(request.form)
        if request.form.get('Account') == "lingyunyi":
            # 打开序列化过后的文件，进行反序列化处理
            fileRead = open('TemplateData.txt', 'rb')
            # 打开序列化过后的文件，进行反序列化处理
            golbalData = pickle.load(fileRead)
            fileRead.close()
            # 给全局变量再次赋值
            golbalData['IndexContent'] = request.form.get('IndexContent')
            print("golbalData['IndexContent']",request.form.get('IndexContent'))
            # 序列化到全局变量文件中
            fileOpen = open('TemplateData.txt', 'wb')
            pickle.dump(golbalData, fileOpen)
            fileOpen.close()
        return render_template("/admin/index.html")

@app.route("/payment/")
def payment():
    return render_template("payment.html")

if __name__ == '__main__':
    app.run(debug=True)
