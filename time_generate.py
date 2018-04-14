"""
@author:yangliqiu
@theme:time generate
"""

# !/usr/bin/python
# __*__ coding: utf-8 __*__
import pymysql
import datetime


# 连接MySQL数据库
def connect_mysql():
    print("连接mysql数据库......")
    try:
        db = pymysql.connect(host="localhost", port=3306, user="root", passwd="1234", db="test", charset='utf8')
        print('连接成功')
    except Exception as e:
        print("连接失败", e)
    return db


# 数据插入MySQL数据库
def insert_mysql(db, time, year, quarter, month, day, weekday):
    cursor = db.cursor()
    sql = "insert into time_info(time_id,year,quarter,month,day,weekday) values('%s', '%s', '%d','%s','%s','%s')"
    data = (time, year, quarter, month, day, weekday)
    try:
        cursor.execute(sql % data)
        db.commit()
        print('插入成功')
    except Exception as e:
        print("插入失败", e)


# 星期转换函数
def weekday_transfor(weekday):
    if weekday == 0: weekday = "星期日"
    elif weekday == 1: weekday = "星期一"
    elif weekday == 2: weekday = "星期二"
    elif weekday == 3: weekday = "星期三"
    elif weekday == 4: weekday = "星期四"
    elif weekday == 5: weekday = "星期五"
    elif weekday == 6: weekday = "星期六"
    else:
        weekday = "error"
    return weekday


if __name__ == "__main__":
    db = connect_mysql()
    for i in range(2010, 2030):
        year = str(i)
        for j in range(1, 13):
            # 季度赋值
            if j < 4: quarter = 1
            elif 3 < j < 7: quarter = 2
            elif 6 < j < 10: quarter = 3
            elif 9 < j < 13: quarter = 4
            # 月份赋值
            if j < 10: month = '0' + str(j)
            else: month = str(j)
            for k in range(1, 32):
                if k < 10:
                    day = '0' + str(k)
                else:
                    day = str(k)
                time = year + month + day
                # 通过日期找出星期几
                try:
                    weekday = int(datetime.datetime(int(year), int(month), int(day)).strftime("%w"))
                except:
                    weekday = "error"
                weekday = weekday_transfor(weekday)
                insert_mysql(db, time, year, quarter, month, day, weekday)
    print('success')

