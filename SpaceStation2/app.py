from flask import Flask
from flask import render_template
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
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=SqlManger_Class_A,ImgData=ImgData)

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
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=SqlManger_Class_H,ImgData=ImgData)

if __name__ == '__main__':
    app.run(debug=True)
