# -*- encoding: utf-8 -*-
'''
@File    :   utils.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/25 9:26   LiuDongxing      1.0         None
'''

# import lib
class Change:
    # 将ajax返回的时间类型数据转化为datetime类型字符串
    def __init__(self,data,data_to=None):
        self.data = data
        self.data_to =data_to
    def ChangeTime(self):
        str = self.data.replace('T',' ')
        print(str)
        return  str
    # 将时间数据转日期数据
    def ChangeDate(self):
        datestr = (self.ChangeTime())[0:10]
        return datestr

    # 将返回的磨床编号下拉框中的数据转为字符串
    def GetROLL(self):
        str = self.data[5:-1]
        print(str)
        return str
    def IFNone(self):
        str = ''
        if self is None:
            return str
        else:
            return self
    def Amount(self):
        if self.data is None:
            return None
        else:
            return float('%.5f' % (float(self.data) - float(self.data_to)))


if  __name__ == '__main__':
    ch = Change('0号磨床(HIECISE-MK84160)').GetROLL()
