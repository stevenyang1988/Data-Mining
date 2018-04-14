"""
@author:yangliqiu
@theme:address_info generate
"""

# !/usr/bin/python
# __*__ coding:utf8 __*__

import warnings
import urllib
from urllib import request
from bs4 import BeautifulSoup
import uuid
import pymysql
import pinyin

warnings.filterwarnings('ignore')
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.75 Safari/537.36'}
country = "中国"


# 数据插入MySQL数据库
def insert_mysql(address_id, province_name, city_name, city_pinyin):
    print("连接mysql数据库......")
    try:
        db = pymysql.connect(host="localhost", port=3306, user="root", passwd="1234", db="test", charset='utf8')
        print('连接成功')
    except Exception as e:
        print("连接失败", e)
    cursor = db.cursor()
    sql = "insert into address_info_pinyin(address_id,country,province,city,city_pinyin)\
          values('%s', '%s', '%s','%s', '%s')"
    data = (address_id, country, province_name, city_name, city_pinyin)
    try:
        cursor.execute(sql % data)
        db.commit()
        print('插入成功')
    except Exception as e:
        print("插入失败", e)
    # db.close()


if __name__ == "__main__":
    address_id = 0
    req = urllib.request.Request(url=url, headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('gb2312')
    soup = BeautifulSoup(html)
    lines = soup.find_all("tr", {"class": "provincetr"})
    for line in lines:
        provinces = line.find_all("a")
        for province in provinces:
            province_name = province.text
            # 爬取二级页面，地级市名称
            url_province = province.get('href')
            url1 = url + url_province
            req1 = urllib.request.Request(url=url1, headers=headers)
            response1 = request.urlopen(req1)
            html1 = response1.read().decode('gb2312')
            soup1 = BeautifulSoup(html1)
            lines1 = soup1.find_all("tr", {"class": "citytr"})
            for line1 in lines1:
                city_name = line1.find_all('td')[1].text
                if '省直辖县级行政区划' in city_name:
                    continue
                if city_name == '市辖区':
                    city_name = province_name
                city_pinyin = pinyin.get(city_name, format='strip', delimiter=" ").replace(' ', '')
                if "shi" in city_pinyin:
                    city_pinyin = city_pinyin.split('shi')[0].capitalize()
                address_id += 1
                address_id_format = "%03d" % address_id
                insert_mysql(address_id_format, province_name, city_name, city_pinyin)
                # print(address_id_format, province_name, city_name)

    print('success')


