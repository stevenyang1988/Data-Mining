"""
@Author:yangliqiu
@Theme:通过调用api接口把ip地址转化为地理位置，定位到市
"""

import chardet
import pinyin
import csv
from pygeoip import GeoIP
import geoip2.database
from launch.gaode_api import SiJiAddress

# 创建csv文件，并写入列名
with open("C:\\Users\\steven\\Desktop\\data\\address_product_series.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['product_series', 'lat', 'lon', 'city_name'])


# ip转换地址函数1
def ip_transform1(ip):
    reader = geoip2.database.Reader('f:\\data\\GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        if response:
            # country_name = response.country.names['zh-CN']
            # city_name = response.city.names
            lon = response.location.longitude
            lat = response.location.latitude
        else:
            # country_name = ''
            # city_name = ''
            lat = ''
            lon = ''
    except Exception as e:
        print('error:', e)
        lat = ''
        lon = ''
    finally:
        reader.close()
    return lat, lon


# ip转换地址函数2
def ip_transform2(ip):
    gi = GeoIP("f:\\data\\GeoLiteCity.dat")
    gir = gi.record_by_addr(ip)
    try:
        country_name = gir['country_name']
        city_name = gir['city']
        lat = gir['latitude']
        lon = gir['longitude']
    except Exception as e:
        print(e)
        country_name = ''
        city_name = ''
        lat = ''
        lon = ''
    return lat, lon, city_name, country_name


if __name__ == "__main__":
    with open("f:\\data\\ip_product_serial.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for record in reader:
            if reader.line_num == 1:
                continue
            ip = record[1]
            try:
                lat, lon, city_name, country_name = ip_transform2(ip)
            except:
                lat = None
            # 去除经度为空的数据
            if not lat:
                continue
            # 去除不是中国的数据
            if not country_name == 'China':
                continue
            # 将数据写入csv文件
            with open("C:\\Users\\steven\\Desktop\\data\\address_product_series.csv", "a", newline='') as file:
                writer = csv.writer(file)
                try:
                    if not city_name:
                        city_name = SiJiAddress(str(lon) + "," + str(lat))['city']
                        city_name = pinyin.get(city_name, format='strip', delimiter=" ").replace(' ', '').split('shi')[0].capitalize()
                    writer.writerow([int(float(record[2])), lat, lon, city_name])
                except:
                    city_name = SiJiAddress(str(lon) + "," + str(lat))['city']
                    city_name = pinyin.get(city_name, format='strip', delimiter=" ").replace(' ', '').split('shi')[0].capitalize()
                    writer.writerow([int(float(record[2])), lat, lon, city_name])
    print('success')

