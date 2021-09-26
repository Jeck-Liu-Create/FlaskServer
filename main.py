# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/20 9:55   LiuDongxing      1.0         None
'''
## 本系统基于Flask框架实现轧辊数据的查询与发送
#coding:utf8


from flask import Flask,request,render_template,jsonify
import pymysql as mysql
import json
import datetime
from utils import Change



con = mysql.connect(user='root',password='Data123..',db="test")
con.autocommit(True)
cur = con.cursor()

datalist = list()

#将数据库的datetime类型数据转化为string类型
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj,datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)

app = Flask(__name__)
@app.route('/')         #设置路由
def index():           # 设置路由对应的函数
    return render_template("indexold.html")

#初始加载数据库
@app.route('/jsondata', methods=['POST', 'GET'])
def info():
    sql = r"select * from grinder_data"
    txt = '初始化查询'
    return infodata(sql,txt)

def infodata(sql,txt:str):
    print(txt)
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    if data:
        print(data)
        # 元组非空
        print("1")
        print(type(data))
        print('2')
        datalist = list(data)
        print(datalist)
        print('3')
        for c in datalist:
            print('4')
            print(c)
            print(type(c))
            datalist[datalist.index(c)] = list(c)
        print('5')
        print(datalist)
        print('6')

        data = []
        a = 1
        for i in range(0, len(datalist)):
            print(i)
            # print(len(datalist))
            print(a)
            a += 1
            d = {"c_id": datalist[i][0], "c_roll_number": datalist[i][1], "c_program_number": datalist[i][2],
                 "c_operator": datalist[i][3], "c_shift": datalist[i][4], "c_curve": datalist[i][5],
                 "c_diameter": datalist[i][6], "c_diameter_before": datalist[i][7], "c_error": datalist[i][8],
                 "c_coaxiality": datalist[i][9], "c_cylindricity": datalist[i][10], "c_roundness": datalist[i][11],
                 "c_wheel_diameter": datalist[i][12], "c_actual_convexity": datalist[i][13],
                 "c_start_time": (datalist[i][14]).strftime("%Y-%m-%d %H:%M:%S"),
                 "c_end_time": (datalist[i][15]).strftime("%Y-%m-%d %H:%M:%S"), "c_grinding_machine": datalist[i][16],
                 "c_date": (datalist[i][17]).strftime("%Y-%m-%d")}
            data.append(d)
            # print(data)
            print('7')

        if request.method == 'POST':
            print('post')
        if request.method == 'GET':
            info = request.values
            limit = info.get('limit', 10)  # 每页显示的条数
            offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
            print('get', limit)
            print('get  offset', offset)
            print(len(data))
            print(data[int(offset):(int(offset) + int(limit))])
            print(len(data[int(offset):(int(offset) + int(limit))]))
            # print(jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}))
            return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
            # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
            # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了

    else:
        data = {"data":'未搜索到数据'}
        print(data)
        return data
    print('54145')


@app.route('/delete')
def delete():
    ID = request.args.get("ID")
    print(ID)
    sql = 'delete from grinder_data where ="%s"' %(ID)
    print(sql)
    cur.execute(sql)
    return "ok"

@app.route('/add')
def add():
    name = request.args.get('name')
    age = request.args.get('age')
    sql = 'insert into userlist values("%s","%s")' %(name,age)
    print(sql)
    cur.execute(sql)
    return "ok"

@app.route('/edit')
def edit():
    name = request.args.get('name')
    age = request.args.get('age')
    sql = 'update grinder_data set age=%s where name="%s"' %(age,name)
    print(sql)
    cur.execute(sql)
    return "ok"
# ajax数据处理
@app.route('/reload', methods=["GET","POST"])
def reload():
    print('执行成功')
    if request.method == 'POST':
        ROLL = request.form.get('ROLL')
        print(type(ROLL))
        StartTime = request.form.get('StartTime')
        print(type(StartTime))
        EndTime = request.form.get('EndTime')
        print(type(EndTime))
        print(ROLL+StartTime+EndTime)
    if request.method == 'GET':
        ROLL = request.args.get('ROLL')
        print(type(ROLL))
        StartTime = request.args.get('StartTime')
        print(type(StartTime))
        EndTime = request.args.get('EndTime')
        print(type(EndTime))
        print(ROLL + StartTime + EndTime)
    # print(ROLL+StartTime+EndTime)
    StartTime = Change(StartTime).ChangeTime()
    EndTime = Change(EndTime).ChangeTime()
    ROLL = Change(ROLL).GetROLL()
    sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_grinding_machine ='%s';"%(StartTime,EndTime,ROLL)
    txt = 'reload查询'
    print(sqltxt)
    return infodata(sqltxt,txt)
    # print(infodata(sqltxt,txt))
    print('reload完成')

# refresh 更新数据表
@app.route('/reload2/<string:data>')
def reload2(data):
    print('1')
    print(data)




if __name__ == "__main__":
    app.run(port=5000,host='10.18.23.104')