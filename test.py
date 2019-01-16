# encoding:utf-8
import datetime, time
from lxml import etree
import requests
import json
from decimal import Decimal
import re

s = '2018-09-29 00:00:00'
Unixtime = time.mktime(time.strptime(s, '%Y-%m-%d %H:%M:%S'))
dt = datetime.datetime.fromtimestamp(Unixtime)
print(type(dt))
print(dt)
Time = "Sep-10-2018 02:26:03 AM"
ds = time.strptime(Time, '%b-%d-%Y %I:%M:%S AM')
ds_s = time.strftime('%Y-%m-%d %H:%M:%S', ds)
ftime = datetime.datetime.strptime(Time, '%b-%d-%Y %I:%M:%S AM')
if Time.find('PM') > -1:
    ftime = ftime + datetime.timedelta(hours=12)
print(ftime)
print(type(ftime))
s_list = ["/address/0xb96eb33e4a1a9ea3b8581abc8185f9597e45e8aa"]

purse_address = s_list[0][9:]
print(purse_address)

# url = 'https://www.hbg.com/-/x/general/exchange_rate/list?r=8o8s0b3eau3pm3wua66c1sjor'
# url_1 = 'https://www.hbg.com/-/x/general/index/constituent_symbol/detail?r=d451aj8o56xet3ksg5mmzehfr'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);'
# }
# result = requests.get(url, headers=headers)
# result = json.loads(result.content.decode())
# result_1 = requests.get(url_1, headers=headers)
# result_1 = json.loads(result_1.content.decode())
# rate = (result['data'][11]['rate'] - 0.1) * result_1['data']['symbols'][2]['close']
# rate = '%0.2f' % rate

# print(rate)
# s_str = "5.000 Ether"
# s_str = s_str[:-6]
# s_str = float(s_str)
# if s_str >= 5:
#     print(type(s_str))
s_float = 3.15676666
s_float_son = 3.5489953
bonus = '%0.3f' % s_float
print(str(s_float)[:-1])

print(10 / 3)

f_str = str(s_float)      # f_str = '{}'.format(f_str) 也可以转换为字符串
a, b, c = f_str.partition('.')
c = (c+"0"*3)[:3]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
s_float = ".".join([a, c])

print(s_float)
print(s_float_son)

s_str = '2.66633'
s_str = float(s_str)

url = 'https://www.mytoken.io/currency/49654'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);'
}

# result = requests.get(url, headers=headers)
# print(result.content.decode())

# encoding:utf-8
import json
from lxml import etree
import requests
import pymysql, datetime


def obtain_rate():
    url = 'https://www.mytoken.io/currency/49654'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);'
    }
    result = requests.get(url, headers=headers)
    html = etree.HTML(result.content.decode())
    node_information = html.xpath('//div[@class="price"]/text()')
    a, b, c = str(node_information[0]).partition(',')
    rate = a + c
    f = open('constants.py', 'w')
    f.write('rate=%s' % rate)


decimal = 5.66
str_decimal = '%.3f' % decimal
print(str_decimal)


num_list = [1, 5, 3, 4, 2, 6, 7]

num_list.reverse()
print(num_list)

import time
import datetime
import calendar

aDatetime = datetime.datetime(1970, 1, 1, 0, 0, 1)
aTimestamp = 1

# 获取时区时差
print("time.timezone: ", time.timezone)

# 根据自定义时间，获取显示时间（datetime）。
print("datetime: ", aDatetime)
print("timetuple: ", aDatetime.timetuple())
print("time.strptime: ", time.strptime("1970-1-1 0:1:1", "%Y-%m-%d %H:%M:%S"))

# 根据时间戳（timestamp），获取UTC显示时间（datetime）。即：时间戳（timestamp） 转换-> 显示时间（datetime）。
print("time.gmtime: timestamp(%s)->datetime(%s)" % (aTimestamp, time.gmtime(aTimestamp)))
print("datetime.datetime.utcfromtimestamp: timestamp(%s)->datetime(%s)" % (aTimestamp, datetime.datetime.utcfromtimestamp(aTimestamp)))

# 根据显示时间（datetime），获取UTC时间戳（timestamp）。即：显示时间（datetime） 转换-> 时间戳（timestamp）。
print("calendar.timegm: datetime(%s)->timestamp(%s)" % (aDatetime.timetuple(), calendar.timegm(aDatetime.timetuple())))
dt = time.gmtime(aTimestamp - time.timezone)  # time.mktime转换时间是带时区的，所以需要减掉时区时差
print("time.mktime: datetime(%s)->timestamp(%s)" % (dt, time.mktime(dt)))
