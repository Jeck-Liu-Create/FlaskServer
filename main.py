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
import threading
from utils import Change
from TCPclient import TCPclient

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
one=TCPclient()
clinet_thread = threading.Thread(target=one.tcp_client)
heardbeat_thread = threading.Thread(target=one.add_heartbeat)
clinet_thread.start()
heardbeat_thread.start()


@app.route('/')         #设置路由
def index():           # 设置路由对应的函数
    return render_template("from.html")

#初始加载数据库
@app.route('/jsondata', methods=['POST', 'GET'])
def info():
    sql = r"select * from grinder_data"
    return infodata(sql)
#依照时间和磨床查找table数据
def infodata(sql):
    con = mysql.connect(user='root', password='Data123..', db="test")
    con.autocommit(True)
    cur = con.cursor()
    try:
        cur.execute(sql)

    except Exception:
        con.rollback()
        print("搜索失败")
    finally:
        data = cur.fetchall()
        cur.close()
        con.close()
        if data:
            # 元组非空
            datalist = list(data)
            # print(datalist)
            for c in datalist:
                datalist[datalist.index(c)] = list(c)
            # print(datalist)
            data = []
            a = 0
            for i in range(0, len(datalist)):
                # print(len(datalist))
                # print(a)
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
                     "c_roughness": datalist[i][23],"c_side_bearing": datalist[i][24],"c_drive_bearing": datalist[i][25],
                     "c_pairing_roll": datalist[i][26],"c_top_diameter": datalist[i][27],"c_low_diameter": datalist[i][28], "number":a,
                     "c_grinding_amount": Change( datalist[i][7],data_to=datalist[i][6]).Amount(), "c_cause": datalist[i][29],
                     "c_result_detection": datalist[i][30], "c_crown_value": datalist[i][31]}
                data.append(d)
                # print(d)

            if request.method == 'POST':
                print('post')
            if request.method == 'GET':
                info = request.values
                limit = info.get('limit', 10)  # 每页显示的条数
                offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
                # print('get', limit)
                # print('get  offset', offset)
                # print(len(data))
                # print(data[int(offset):(int(offset) + int(limit))])
                # print(len(data[int(offset):(int(offset) + int(limit))]))
                # print(jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}))
                return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
                # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
                # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了
        else:
            data = {"data":'未搜索到数据'}
            print(data)
            return data

# 编辑保持数据
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
    c_cause = data['c_cause']                   #c_cause            磨削原因
    c_result_detection = data['c_result_detection']            #c_result_detection 探伤结果
    c_crown_value = data['c_crown_value']                      #c_crown_value      凸度值
    sqltxt = r"update grinder_data set c_frame_id = '%s', c_roll_type = '%s', c_roll_position = '%s', c_roll_material = '%s', c_crown_symbol = '%s', c_roughness = '%s', c_side_bearing = '%s', c_drive_bearing = '%s', c_pairing_roll = '%s', c_top_diameter = '%s', c_low_diameter = '%s', c_cause = '%s' ,c_result_detection = '%s', c_crown_value = '%s' where c_id = '%s'  LIMIT 1 ;" % (c_frame_id, c_roll_type, c_roll_position, c_roll_material,  c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter,  c_cause, c_result_detection ,c_crown_value ,c_id)
    print('更新操作SQL = '+sqltxt)
    restr = {"data": '修改成功',}
    json_restr = json.dumps(restr)
    redistr = {"data": '修改失败',}
    json_redistr = json.dumps(redistr)
    try:
        con = mysql.connect(user='root', password='Data123..', db="test")
        con.autocommit(True)
        cur = con.cursor()
        try:
            cur.execute(sqltxt)
            return json_restr
        except Exception:
            con.rollback()
            return json_redistr
        finally:
            cur.close()
            con.close()
            print('更新执行成功')
    except:
        print('更新执行失败')
        return json_redistr

# 更新table_ajax 数据处理
@app.route('/reload', methods=["GET","POST"])
def reload():
    global StartTime, EndTime, ROLL, ROLLNM
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
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_grinding_machine ='%s' ORDER BY c_id desc;"%(StartTime,EndTime,ROLL)
    else:
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_roll_number ='%s' ORDER BY c_id desc;"%(StartTime,EndTime,ROLLNM)
    print("reload查询"+sqltxt)
    return infodata(sqltxt)
    # print(infodata(sqltxt,txt))

# send 发送数据到Level2系统
@app.route('/send', methods=["GET","POST"])
def send():
    data = json.loads(request.form.get('data'))
    # print(data)
    senddata = data['c_id']
    senddata = senddata.zfill(9)
    databytes = bytes(50)
    print(senddata)
    datadatabytesbarr = bytearray(databytes)
    senddata = senddata.encode("utf-8")
    datadatabytesbarr[0:len(senddata) ] = senddata
    databytes = bytes(datadatabytesbarr)
    one.queue_wirte(databytes)
    redata = {"data": '发送成功'}
    return  redata

@app.route('/from.html') #页面链接该路由名称
def f_infor():
    return render_template('from.html')

@app.route('/index.html') #页面链接该路由名称
def f_infor_index():
    return render_template('index.html')

@app.route('/uproll.html') #页面链接该路由名称
def f_infor_uproll():
    return render_template('uproll.html')

@app.route('/supplement.html') #页面链接该路由名称
def f_infor_supplement():
    return render_template('supplement.html')

@app.route('/send_record.html') #页面链接该路由名称
def f_infor_send_record():
    return render_template('send_record.html')

#依照时间和磨床查找table数据
def infodata_index(sql):
    con = mysql.connect(user='root', password='Data123..', db="serverxp")
    con.autocommit(True)
    cur = con.cursor()
    try:
        cur.execute(sql)

    except Exception:
        con.rollback()
        print("搜索失败")
    finally:
        data = cur.fetchall()
        cur.close()
        con.close()
        if data:
            # 元组非空
            datalist = list(data)
            # print(datalist)
            for c in datalist:
                datalist[datalist.index(c)] = list(c)
            # print(datalist)
            data = []
            a = 0
            for i in range(0, len(datalist)):
                # print(len(datalist))
                # print(a)
                a += 1
                d = {"c_frame_id": datalist[i][0], "c_roll_type": datalist[i][1], "c_roll_number": datalist[i][2],
                     "c_down_time": (datalist[i][3].strftime("%Y-%m-%d %H:%M:%S")), "c_down_cless": datalist[i][4], "c_down_set": datalist[i][5],
                     "c_running_time": datalist[i][6], "c_rolling_length": datalist[i][7], "c_rolling_weight": datalist[i][8],
                     "c_product_remark": datalist[i][9], "c_change_reason": datalist[i][10], "c_accident_coil_No ": datalist[i][11],
                     "id": datalist[i][12]}
                data.append(d)
                # print(d)

            if request.method == 'POST':
                print('post')
            if request.method == 'GET':
                info = request.values
                limit = info.get('limit', 10)  # 每页显示的条数
                offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
                # print('get', limit)
                # print('get  offset', offset)
                # print(len(data))
                # print(data[int(offset):(int(offset) + int(limit))])
                # print(len(data[int(offset):(int(offset) + int(limit))]))
                # print(jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}))
                return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
                # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
                # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了
        else:
            data = {"data":'未搜索到数据'}
            print(data)
            return data

# 更新table_ajax 数据处理
@app.route('/reload_index', methods=["GET","POST"])
def reload_index():
    global StartTime, EndTime, ROLL, ROLLNM, Roll_Type, Franm_Id, sqltxt
    print('执行成功')
    if request.method == 'POST':
        Franm_Id = request.form.get('Franm_Id')
        Roll_Type = request.form.get('Roll_Type')
        StartTime = request.form.get('StartTime')
        EndTime = request.form.get('EndTime')
        ROLLNM = request.form.get('ROLLNM')
    if request.method == 'GET':
        Franm_Id = request.args.get('Franm_Id')
        Roll_Type = request.args.get('Roll_Type')
        StartTime = request.args.get('StartTime')
        EndTime = request.args.get('EndTime')
        ROLLNM = request.args.get('ROLLNM')
        print(Franm_Id + Roll_Type + StartTime + EndTime + ROLLNM)

    StartTime = Change(StartTime).ChangeTime()
    EndTime = Change(EndTime).ChangeTime()

    if (ROLLNM=='null'):
        if (Roll_Type =='' and Franm_Id ==''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' ORDER BY id desc;"%(StartTime, EndTime)
        elif( Roll_Type =='' and Franm_Id != ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 机架号 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Franm_Id)
        elif( Roll_Type !='' and Franm_Id == ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 轧辊类型 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Roll_Type)
        elif( Roll_Type !='' and Franm_Id != ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 轧辊类型 = '%s' and 机架号 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Roll_Type, Franm_Id)
    else:
        if (Roll_Type == '' and Franm_Id == ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 轧辊号 = '%s'ORDER BY id desc;" % (StartTime, EndTime, ROLLNM)
        elif (Roll_Type == '' and Franm_Id != ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 机架号 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Franm_Id, ROLLNM)
        elif (Roll_Type != '' and Franm_Id == ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 轧辊类型 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Roll_Type, ROLLNM)
        elif (Roll_Type != '' and Franm_Id != ''):
            sqltxt = r"select * from offrollmsg where 卸辊时间 >= '%s' and 卸辊时间 <= '%s' and 轧辊类型 = '%s' and 机架号 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Roll_Type, Franm_Id, ROLLNM)
    print("reload查询"+sqltxt)
    return infodata_index(sqltxt)
    # print(infodata(sqltxt,txt))

#依照时间和磨床查找table数据
def infodata_uproll(sql):
    con = mysql.connect(user='root', password='Data123..', db="serverxp")
    con.autocommit(True)
    cur = con.cursor()
    try:
        cur.execute(sql)

    except Exception:
        con.rollback()
        print("搜索失败")
    finally:
        data = cur.fetchall()
        cur.close()
        con.close()
        if data:
            # 元组非空
            datalist = list(data)
            # print(datalist)
            for c in datalist:
                datalist[datalist.index(c)] = list(c)
            # print(datalist)
            data = []
            a = 0
            for i in range(0, len(datalist)):
                # print(len(datalist))
                # print(a)
                a += 1
                d = {"c_frame_id": datalist[i][0], "c_roll_type": datalist[i][1], "c_roll_number": datalist[i][2],
                     "c_down_time": (datalist[i][3].strftime("%Y-%m-%d %H:%M:%S")), "c_down_cless": datalist[i][4], "c_down_set": datalist[i][5],
                     "id": datalist[i][6]}
                data.append(d)
                # print(d)

            if request.method == 'POST':
                print('post')
            if request.method == 'GET':
                info = request.values
                limit = info.get('limit', 10)  # 每页显示的条数
                offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
                # print('get', limit)
                # print('get  offset', offset)
                # print(len(data))
                # print(data[int(offset):(int(offset) + int(limit))])
                # print(len(data[int(offset):(int(offset) + int(limit))]))
                # print(jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}))
                return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
                # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
                # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了
        else:
            data = {"data":'未搜索到数据'}
            print(data)
            return data

# 更新table_ajax 数据处理
@app.route('/reload_uproll', methods=["GET","POST"])
def reload_uproll():
    global StartTime, EndTime, ROLL, ROLLNM, Roll_Type, Franm_Id, sqltxt
    print('执行成功')
    if request.method == 'POST':
        Franm_Id = request.form.get('Franm_Id')
        Roll_Type = request.form.get('Roll_Type')
        StartTime = request.form.get('StartTime')
        EndTime = request.form.get('EndTime')
        ROLLNM = request.form.get('ROLLNM')
    if request.method == 'GET':
        Franm_Id = request.args.get('Franm_Id')
        Roll_Type = request.args.get('Roll_Type')
        StartTime = request.args.get('StartTime')
        EndTime = request.args.get('EndTime')
        ROLLNM = request.args.get('ROLLNM')
        print(Franm_Id + Roll_Type + StartTime + EndTime + ROLLNM)

    StartTime = Change(StartTime).ChangeTime()
    EndTime = Change(EndTime).ChangeTime()

    if (ROLLNM=='null'):
        if (Roll_Type =='' and Franm_Id ==''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' ORDER BY id desc;"%(StartTime, EndTime)
        elif( Roll_Type =='' and Franm_Id != ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 机架号 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Franm_Id)
        elif( Roll_Type !='' and Franm_Id == ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 轧辊类型 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Roll_Type)
        elif( Roll_Type !='' and Franm_Id != ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 轧辊类型 = '%s' and 机架号 = '%s' ORDER BY id desc;"%(StartTime, EndTime, Roll_Type, Franm_Id)
    else:
        if (Roll_Type == '' and Franm_Id == ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 轧辊号 = '%s'ORDER BY id desc;" % (StartTime, EndTime, ROLLNM)
        elif (Roll_Type == '' and Franm_Id != ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 机架号 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Franm_Id, ROLLNM)
        elif (Roll_Type != '' and Franm_Id == ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 轧辊类型 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Roll_Type, ROLLNM)
        elif (Roll_Type != '' and Franm_Id != ''):
            sqltxt = r"select * from uprollmsg where 装辊时间 >= '%s' and 装辊时间 <= '%s' and 轧辊类型 = '%s' and 机架号 = '%s' and 轧辊号 = '%s' ORDER BY id desc;" % (StartTime, EndTime, Roll_Type, Franm_Id, ROLLNM)
    print("reload查询"+sqltxt)
    return infodata_uproll(sqltxt)
    # print(infodata(sqltxt,txt))

# 补录数据
@app.route('/edit_add', methods=["GET","POST"])
def edit_add():
    global model_id , model_insert , id_data
    data = json.loads(request.form.get('data'))
    print(data)
    c_start_time = Change(data['c_start_time'] ).ChangeTime()           #c_start_time       开始时间
    c_end_time = Change(data['c_end_time'] ).ChangeTime()               #c_start_time       开始时间
    c_diameter_before = data['c_diameter_before']              #c_diameter_before           轧辊磨前直径
    c_diameter = data['c_diameter']             #c_diameter         轧辊磨后直径
    c_date = Change(data['c_end_time']).ChangeDate()                    #c_date             结束日期
    c_grinding_machine =Change(data['c_grinding_machine']).GetROLL()    #c_grinding_machine 磨床
    c_roll_number = data['c_roll_number']       #c_roll_number      轧辊编号
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
    c_cause = data['c_cause']                   #c_cause            磨削原因
    c_result_detection = data['c_result_detection']            #c_result_detection 探伤结果
    c_crown_value = data['c_crown_value']                      #c_crown_value      凸度值
    # sqltxt = r"update grinder_data set c_frame_id = '%s', c_roll_type = '%s', c_roll_position = '%s', c_roll_material = '%s', c_crown_symbol = '%s', c_roughness = '%s', c_side_bearing = '%s', c_drive_bearing = '%s', c_pairing_roll = '%s', c_top_diameter = '%s', c_low_diameter = '%s', c_cause = '%s' ,c_result_detection = '%s', c_crown_value = '%s' where c_id = '%s'  LIMIT 1 ;" % (c_frame_id, c_roll_type, c_roll_position, c_roll_material,  c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter,  c_cause, c_result_detection ,c_crown_value )

    sqltxt = r"insert into grinder_data (c_diameter_before, c_date, c_roll_number,c_start_time, c_end_time, c_diameter, c_grinding_machine, c_frame_id, c_roll_type, c_roll_position, c_roll_material, c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter, c_cause, c_result_detection, c_crown_value) "
    sqltxt = sqltxt + r"values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (c_diameter_before, c_date, c_roll_number,c_start_time, c_end_time, c_diameter ,c_grinding_machine, c_frame_id, c_roll_type, c_roll_position, c_roll_material, c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter, c_cause, c_result_detection, c_crown_value)

    sqltxtid = r"select c_id from grinder_data where c_diameter_before = '%s' and c_date = '%s' and c_roll_number = '%s' and c_start_time = '%s' and c_end_time = '%s' and c_diameter = '%s' and c_grinding_machine = '%s' and c_frame_id = '%s' and c_roll_type = '%s' and c_roll_position = '%s' and c_roll_material = '%s' and c_crown_symbol = '%s' and c_roughness = '%s' and c_side_bearing = '%s' and c_drive_bearing = '%s' and c_pairing_roll = '%s' and c_top_diameter = '%s' and c_low_diameter = '%s' and c_cause = '%s' and c_result_detection = '%s' and c_crown_value = '%s' LIMIT 1 ;" % (c_diameter_before,c_date,c_roll_number, c_start_time, c_end_time, c_diameter ,c_grinding_machine, c_frame_id, c_roll_type, c_roll_position, c_roll_material, c_crown_symbol, c_roughness, c_side_bearing, c_drive_bearing, c_pairing_roll, c_top_diameter, c_low_diameter, c_cause, c_result_detection, c_crown_value)

    print('插入SQL = '+sqltxt)

    model_insert = True
    model_id = True
    try:
        con = mysql.connect(user='root', password='Data123..', db="test")
        con.autocommit(True)
        cur = con.cursor()
        try:
            cur.execute(sqltxt)
            print('插入执行成功')
        except Exception:
            con.rollback()
            model_insert = False
        finally:
            cur.close()
            con.close()
    except:
        print('插入执行失败')

    # 确定补录数据的id
    try:
        con = mysql.connect(user='root', password='Data123..', db="test")
        con.autocommit(True)
        cur = con.cursor()
        try:
            cur.execute(sqltxtid)
            print('id搜索执行成功')
            id_data = cur.fetchall()
        except Exception:
            con.rollback()
            model_id = False
        finally:
            cur.close()
            con.close()
    except:
        print('插入执行失败')

    if model_insert:
        print('补录成功')
        if model_id:
            print('c_id搜索执行成功')
            if id_data:
                print("全部成功")
                datalist = list(id_data)
                for c in datalist:
                    datalist[datalist.index(c)] = list(c)
                print(datalist)
                returndata = {"data": '补录成功',"c_id":datalist[0][0]}
                json_returndata = json.dumps(returndata)
                return json_returndata
            else:
                print("c_id搜索为空")
                returndata = {"data": '补录失败', "c_id": ''}
                json_returndata = json.dumps(returndata)
                return json_returndata
        else:
            print("搜索语句执行失败")
            returndata = {"data": '补录失败', "c_id": ''}
            json_returndata = json.dumps(returndata)
            return json_returndata
    else:
        print('补录执行失败')
        returndata = {"data": '补录失败', "c_id": ''}
        json_returndata = json.dumps(returndata)
        return json_returndata

# 补录数据搜索
@app.route('/reload_add', methods=["GET","POST"])
def reload_add():
    global StartTime, EndTime, ROLL, ROLLNM
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
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_grinding_machine ='%s' and c_shift is null ORDER BY c_id desc;"%(StartTime,EndTime,ROLL)
    else:
        sqltxt = r"select * from grinder_data where c_start_time >= '%s' and c_end_time <= '%s' and c_roll_number ='%s' and c_shift is null ORDER BY c_id desc;"%(StartTime,EndTime,ROLLNM)
    print("reload查询"+sqltxt)
    return infodata(sqltxt)
    # print(infodata(sqltxt,txt))

# 补录数据删除
@app.route('/delete_id', methods=["GET","POST"])
def delete_id():
    global model_delete
    data = json.loads(request.form.get('data'))
    c_id = data['c_id']
    print(c_id)
    sqltxt = r"DELETE FROM grinder_data WHERE c_id = '%s'" % c_id

    restr = {"data": '删除成功', }
    json_restr = json.dumps(restr)
    redistr = {"data": '删除失败', }
    json_redistr = json.dumps(redistr)

    model_delete = True

    try:
        con = mysql.connect(user='root', password='Data123..', db="test")
        con.autocommit(True)
        cur = con.cursor()
        try:
            cur.execute(sqltxt)
            print('删除执行成功')
        except Exception:
            con.rollback()
            model_delete = False
        finally:
            cur.close()
            con.close()
    except:
        print('删除执行失败')

    if model_delete:
        return json_restr
    else:
        return json_redistr

#依照发送时间和磨床查找table数据
def info_send_data(sql):
    con = mysql.connect(user='root', password='Data123..', db="test")
    con.autocommit(True)
    cur = con.cursor()
    try:
        cur.execute(sql)

    except Exception:
        con.rollback()
        print("搜索失败")
    finally:
        data = cur.fetchall()
        cur.close()
        con.close()
        if data:
            # 元组非空
            datalist = list(data)
            for c in datalist:
                datalist[datalist.index(c)] = list(c)
            data = []
            a = 0
            for i in range(0, len(datalist)):
                a += 1
                d = {"id": datalist[i][0],"send_time": (datalist[i][1]).strftime("%Y-%m-%d %H:%M:%S"),"c_id": datalist[i][2], "c_roll_number": datalist[i][3], "c_program_number": datalist[i][4],
                     "c_operator": datalist[i][5], "c_shift": datalist[i][6], "c_curve": datalist[i][7],
                     "c_diameter": datalist[i][8], "c_diameter_before": datalist[i][9], "c_error": datalist[i][10],
                     "c_coaxiality": datalist[i][11], "c_cylindricity": datalist[i][12], "c_roundness": datalist[i][13],
                     "c_wheel_diameter": datalist[i][14], "c_actual_convexity": datalist[i][15],
                     "c_start_time": (datalist[i][16]).strftime("%Y-%m-%d %H:%M:%S"),
                     "c_end_time": (datalist[i][17]).strftime("%Y-%m-%d %H:%M:%S"), "c_grinding_machine": datalist[i][18],
                     "c_date": (datalist[i][19]).strftime("%Y-%m-%d"),"c_frame_id": datalist[i][20],"c_roll_type": datalist[i][21],
                     "c_roll_position": datalist[i][22],"c_roll_material": datalist[i][23],"c_crown_symbol": datalist[i][24],
                     "c_roughness": datalist[i][25],"c_side_bearing": datalist[i][26],"c_drive_bearing": datalist[i][27],
                     "c_pairing_roll": datalist[i][28],"c_top_diameter": datalist[i][29],"c_low_diameter": datalist[i][30], "number":a,
                     "c_grinding_amount": Change( datalist[i][9],data_to=datalist[i][8]).Amount(), "c_cause": datalist[i][31],
                     "c_result_detection": datalist[i][32], "c_crown_value": datalist[i][33]}
                data.append(d)

            # if request.method == 'POST':
            #     print('post')
            if request.method == 'GET':
                info = request.values
                limit = info.get('limit', 10)  # 每页显示的条数
                offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
                # print('get', limit)
                # print('get  offset', offset)
                # print(len(data))
                # print(data[int(offset):(int(offset) + int(limit))])
                # print(len(data[int(offset):(int(offset) + int(limit))]))
                return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
        else:
            data = {"data":'未搜索到数据'}
            print(data)
            return data

@app.route('/reload_send_data', methods=["GET","POST"])
def reload_send_data():
    global StartTime, EndTime, ROLL, ROLLNM
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
        sqltxt = r"select * from send_succeed where send_time >= '%s' and send_time <= '%s' and c_grinding_machine ='%s' ORDER BY c_id desc;"%(StartTime,EndTime,ROLL)
    else:
        sqltxt = r"select * from send_succeed where send_time >= '%s' and send_time <= '%s' and c_roll_number ='%s' ORDER BY c_id desc;"%(StartTime,EndTime,ROLLNM)
    print("reload查询"+sqltxt)
    return info_send_data(sqltxt)

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')