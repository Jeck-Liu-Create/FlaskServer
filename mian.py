# -*- encoding: utf-8 -*-
'''
@File    :   mian.py
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
    return render_template("index.html")

#初始加载数据库
@app.route('/jsondata', methods=['POST', 'GET'])
def infos():
    sql = "select * from grinder_data"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    print(type(data))
    datalist = list(data)
    for c in datalist:
        datalist[datalist.index(c)] = list(c)
        print
        c

    data = []
    for i in range(0, len(datalist)):
        d = {}
        d["c_id"] = datalist[i][0]
        d["c_roll_number"] = datalist[i][1]
        d["c_program_number"] = datalist[i][2]
        d["c_operator"] = datalist[i][3]
        d["c_shift"] = datalist[i][4]
        d["c_curve"] = datalist[i][5]
        d["c_diameter"] = datalist[i][6]
        d["c_diameter_before"] = datalist[i][7]
        d["c_error"] = datalist[i][8]
        d["c_coaxiality"] = datalist[i][9]
        d["c_cylindricity"] = datalist[i][10]
        d["c_roundness"] = datalist[i][11]
        d["c_wheel_diameter"] = datalist[i][12]
        d["c_actual_convexity"] = datalist[i][13]
        d["c_start_time"] = (datalist[i][14]).strftime("%Y-%m-%d %H:%M:%S")
        d["c_end_time"] = (datalist[i][15]).strftime("%Y-%m-%d %H:%M:%S")
        d["c_grinding_machine"] = datalist[i][16]
        d["c_date"] = (datalist[i][17]).strftime("%Y-%m-%d")
        data.append(d)
    print(data[1])
    print(type(data[1]))
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
        # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
        # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了

@app.route("/userlist")
def userlist():
    sql = "select * from grinder_data"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    print(type(data))
    datalist = list(data)
    for c in datalist:
        datalist[datalist.index(c)] = list(c)
        print
        c
    print(datalist)
    dump_data = json.dumps(data,cls=DateEncoder)
    print(type(dump_data))
    return dump_data

@app.route("/getfrom",methods = ["POST"])
def gettime():
    print ("成功获取时间")
    starttime = request.form.get('s_time')
    endtime = request.form.get('e_time')
    print("开始时间:"+starttime)
    print("结束时间:"+endtime)
    ROLL = request.form.get('ROLL')
    print(ROLL)
    return render_template('index.html')

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
    name = request.args.get('name');
    age = request.args.get('age')
    sql = 'update grinder_data set age=%s where name="%s"' %(age,name)
    print(sql)
    cur.execute(sql)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True,port=5000,host='127.0.0.1')