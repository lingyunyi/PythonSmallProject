from flask import Flask
from flask import render_template
import WebShell,time,random,Sqlmanager
from setting import Setting

app = Flask(__name__)
setting = Setting()

@app.route('/')
def indexShow():
    global setting
    return render_template('/index.html', DataDict=setting.Tem_Golbals_WebUrl_Dict,DataList=setting.Tem_Golbals_SQL_Table_Data_List)

@app.route("/login")
def login():
    global setting
    return render_template('/account.html')

@app.route("/admin/")
def admin():
    global setting
    return render_template('/admin/index.html', DataDict=setting.Tem_Golbals_WebUrl_Dict,DataList=setting.Tem_Golbals_SQL_Table_Data_List)

@app.route("/lingyunyi/<flag>")
def lingyunyi(flag):
    # 启动各种各样的定时功能
    if flag == "stop":
        setting.clearGolbalsData()
        setting.clearTemplateData()
        return render_template('完结的页面')
    elif flag == "start":
        # 内存字典的的刷新，其中包含status ADN ping值
        while True:
            # 开始获取数据并更新内存字典
            Sqlmanager.SqlManger(setting).search_table_all_data()
            # 将内存字典的数据转换并吸收数据
            WebShell.webShell(setting)
            # 到这里内存字典就已经有数据了
            # 我们将内存字典的数据，深拷贝到，临时内存字典中，防止第二次刷新数据时，网页出错
            setting.GolbalsData2TemplateData()
            print(setting.Tem_Golbals_WebUrl_Dict)
            time.sleep(random.randint(5,20)*60)
            # 在等待的时间完成之后，我们刷新一次内存字典，这时并不会影响使用临时字典的网站
            setting.clearGolbalsData()
    return True

if __name__ == '__main__':
    app.run(debug=True)
