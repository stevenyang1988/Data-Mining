"""@Author: yangliqiu
   @theme:  解析出每条诊断报告的地理位置，同时将诊断报告名称转化为拼音，
            最终将诊断报告的id号、地理位置（城市）、诊断报告拼音、故障码列表存入csv文件
"""

from odps import ODPS
from launch.gaode_api import SiJiAddress
import pinyin
import csv
import pandas as pd
import datetime
from multiprocessing import Pool
import time
import json

# 读取产品设备号和地理位置表，方便后续解析地理位置
data = pd.read_csv('C:\\Users\\steven\\Desktop\\data\\address_product_series.csv', encoding="gbk", low_memory=False)
data1 = data.drop_duplicates("product_series")
data2 = data1.set_index(['product_series'])
# 读取maxcompute中的diagnose_report表
odps = ODPS('LTAIkLO9entocXgc', 'mCr2aK02tf510aqwAoZRI0QjpTRdTA', 'Launch_DW',
            endpoint='http://service.odps.aliyun.com/api')
t = odps.get_table('diagnose_report')


def work(start_date):
    name = start_date + '.' + 'csv'
    # 打开csv文件，并写入列名
    with open(name, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'address', 'theme_pinyin', 'fault_list'])
    start_time = datetime.datetime.strptime(start_date, '%Y%m%d')
    for k in range(50):
        now_time = start_time + datetime.timedelta(days=k)
        now_time = now_time.strftime("%Y%m%d")
        partition = 'pt' + '=' + now_time
        with t.open_reader(partition=partition) as reader:
            for record in reader:
                # 解析出故障码到列表fault_list1
                fault_codes = record['fault_codes']
                fault_list1 = []
                if fault_codes:
                    json_fault = json.loads(fault_codes)
                    try:
                        syss_list = json_fault['syss']
                        for syss in syss_list:
                            fault_list = syss['faults']
                            for fault in fault_list:
                                fault_list1.append(fault['code'])
                    except:
                        pass
                # 若有经纬度数据，则通过经纬度解析地址
                if record['technician_lon'] and record['technician_lat']:
                    try:
                        address = SiJiAddress(str(record['technician_lon']) + ',' + str(record['technician_lat']))['city']
                        address = address.split('市')[0]
                        address = pinyin.get(address, format='strip', delimiter=" ").replace(' ', '').capitalize()
                    # 若经纬度没有解析出地址，则则通过设备号解析出地理位置
                    except:
                        try:
                            address = data2.loc[int(record['pro_serial_no'])]['city_name']
                        except:
                            address = ''
                # 若无经纬度数据，则通过设备号解析出地理位置
                else:
                    try:
                        address = data2.loc[int(record['pro_serial_no'])]['city_name']
                    except:
                        address = ''
                # 将报告主题转化为拼音
                try:
                    theme = record['theme'].split('诊断报告')[0]
                    theme_pinyin = pinyin.get(theme, format='strip', delimiter=" ")
                    theme_pinyin = ''.join(e for e in theme_pinyin if e.isalnum())
                except:
                    theme_pinyin = ''
                # 将数据写入csv文件
                try:
                    with open(name, "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([record['id'], address, theme_pinyin, fault_list1])
                except:
                    continue


if __name__ == "__main__":
    start = time.clock()
    p = Pool(22)
    for i in range(22):
        now_time = datetime.datetime.strptime('20150501', '%Y%m%d')
        now_time = now_time + datetime.timedelta(days=50 * i)
        now_time = now_time.strftime("%Y%m%d")
        p.apply_async(work, args=(now_time,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    end = time.clock()
    print(end - start)


