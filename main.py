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
    return render_template("from.html")

#初始加载数据库
@app.route('/jsondata', methods=['POST', 'GET'])
def info():
    sql = r"select * from grinder_data"
    txt = '初始化查询'
    return infodata(sql,txt)
#依照时间和磨床查找table数据
def infodata(sql):
    con = mysql.connect(user='root', password='Data123..', db="test")
    con.autocommit(True)
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    if data:
        # 元组非空
        datalist = list(data)
        print(datalist)
        for c in datalist:
            datalist[datalist.index(c)] = list(c)
        print(datalist)
        data = []
        a = 1
        for i in range(0, len(datalist)):
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
                 "c_date": (datalist[i][17]).strftime("%Y-%m-%d"),"c_frame_id": datalist[i][18],"c_roll_type": datalist[i][19],
                 "c_roll_position": datalist[i][20],"c_roll_material": datalist[i][21],"c_crown_symbol": datalist[i][22],
                 "c_roughness": datalist[i][23],"c_side_bearing": datalist[i][24],"c_drive_bearingd": datalist[i][25],
                 "c_pairing_roll": datalist[i][26],"c_top_diameter": datalist[i][27],"c_low_diameter": datalist[i][28]}
            data.append(d)
            print(d)

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
#一直辊号和

@app.route('/delete')
def delete():
    ID = request.args.get("ID")
    print(ID)
    sql = 'delete from grinder_data where ="%s"' %(ID)
    print(sql)
    # cur.execute(sql)
    return "ok"

@app.route('/add')
def add():
    name = request.args.get('name')
    age = request.args.get('age')
    sql = 'insert into userlist values("%s","%s")' %(name,age)
    print(sql)
    return "ok"

@app.route('/edit', methods=["GET","POST"])
def edit():
    data = json.loads(request.form.get('data'))
    print(data)
    c_id = data['c_id']                         #c_id               作为主键
    c_frame_id = Change.IFNone(data['c_frame_id'])             #c_frame_id         机架号
    c_roll_type = Change.IFNone(data['c_roll_type'])           #c_roll_type        轧辊类型
    c_roll_position = Change.IFNone(data['c_roll_position'])   #c_roll_position    轧辊位置
    c_roll_material = Change.IFNone(data['c_roll_material'])   #c_roll_material    轧辊材质
    c_crown_symbol = Change.IFNone(data['c_crown_symbol'])     #c_crown_symbol     凸度正负标记
    c_roughness = data['c_roughness']           #c_roughness        粗糙度
    c_side_bearing = data['c_side_bearing']     #c_side_bearing     操作侧轴承号
    c_drive_bearing = data['c_drive_bearing']   #c_drive_bearing    驱动侧轴程号
    c_pairing_roll = data['c_pairing_roll']     #c_pairing_roll     配对辊号
    c_top_diameter = data['c_top_diameter']     #c_top_diameter     锥形顶端直径
    c_low_diameter = data['c_low_diameter']     #c_low_diameter     锥形底端直径
    sqltxt = r"update grinder_data set c_frame_id = '%s', c_roll_type = '%s', c_roll_position = '%s', c_roll_material = '%s', c_crown_symbol = '%s', c_roughness = '%s', c_side_bearing = '%s', c_drive_bearing = '%s', c_pairing_roll = '%s', c_top_diameter = '%s', c_low_diameter = '%s' where c_id = '%s' LIMIT 1 ;" % (c_frame_id, c_roll_type, c_roll_position, c_roll_material,  c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter, c_id)
    print('更新操作SQL = '+sqltxt)
    try:
        con = mysql.connect(user='root', password='Data123..', db="test")
        con.autocommit(True)
        cur = con.cursor()
        cur.execute(sqltxt)
        cur.close()
        con.close()
        print('更新执行成功')
    except:
        print('更新执行失败')
        return data
    return data
# ajax数据处理
@app.route('/reload', methods=["GET","POST"])
def reload():
    print('执行成功')
    if request.method == 'POST':
        ROLL = request.form.get('ROLL')
        StartTime = request.form.get('StartTime')
        EndTime = request.form.get('EndTime')
        ROLLNM = request.form.get('ROLLNM')
    if request.method == 'GET':
        ROLL = request.args.get('ROLL')
        StartTime = request.args.get('StartTime')
        EndTime = request.args.get('EndTime')
        ROLLNM = request.args.get('ROLLNM')
        print(ROLL + StartTime + EndTime + ROLLNM)
    # print(ROLL+StartTime+EndTime)
    StartTime = Change(StartTime).ChangeTime()
    EndTime = Change(EndTime).ChangeTime()
    ROLL = Change(ROLL).GetROLL()
    # print("Search="+ROLLNM+type(ROLLNM))
    if (ROLLNM=='null'):
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_grinding_machine ='%s';"%(StartTime,EndTime,ROLL)
    else:
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_roll_number ='%s';"%(StartTime,EndTime,ROLLNM)
    print("reload查询"+sqltxt)
    return infodata(sqltxt)
    # print(infodata(sqltxt,txt))
    print('reload完成')

# refresh 更新数据表
@app.route('/reload2/<string:data>')
def reload2(data):
    print('1')
    print(data)




if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')