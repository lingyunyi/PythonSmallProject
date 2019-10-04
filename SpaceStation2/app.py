from flask import Flask
from flask import render_template
import mainFunction
import pickle
import random

app = Flask(__name__)


@app.route('/')
def indexShow():
    fileRead = open('TemplateData.txt', 'rb')
    golbalData = pickle.load(fileRead)
    imgData = golbalData["BiliBili"]
    randomKey = random.choice(list(imgData.keys()))
    randomValue = imgData[randomKey]
    ImgData = []
    ImgData.append([randomKey,randomValue])
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=golbalData["SqlManger"],ImgData=ImgData)

@app.route("/login")
def login():
    fileRead = open('TemplateData.txt', 'rb')
    golbalData = pickle.load(fileRead)
    return render_template('/index.html', DataDict=golbalData["WebShell"],DataList=golbalData["SqlManger"])

@app.route("/admin/")
def admin():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("开始执行..")
    print("开始执行...")
    print("开始执行.........")
    mainFunction.IntervalProduction()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    fileRead = open('TemplateData.txt', 'rb')
    golbalData = pickle.load(fileRead)
    return render_template('/admin/index.html', DataDict=golbalData["WebShell"],DataList=golbalData["SqlManger"])

if __name__ == '__main__':
    app.run(debug=True)
