# --*-- coding: utf-8 --*--
"""
@author: yangliqiu
@theme: resolve address of technician
"""
from odps import ODPS
from launch.gaode_api import SiJiAddress
import random
import csv
import pandas as pd

# read table product_lat_lon from aliyun maxcompute table
odps = ODPS('LTAIkLO9entocXgc', 'mCr2aK02tf510aqwAoZRI0QjpTRdTA', 'Launch_DW',
            endpoint='http://service.odps.aliyun.com/api')
t = odps.get_table('technician_profile3')
# read the csv file "address_product_series.csv", and define the index column of "product_series"
data = pd.read_csv('address_product_series.csv', encoding="gbk", low_memory=False)
data1 = data.drop_duplicates("product_series")
data2 = data1.set_index(['product_series'])
# read the csv file "address_info_pinyin.csv", and define the index column of "city_pinyin"
data3 = pd.read_csv('address_info_pinyin.csv', encoding="utf-8", low_memory=False)
data4 = data3.set_index(['city_pinyin'])

telephone_data1 = pd.read_csv('technician_apply_detail.csv', encoding="utf-8", low_memory=False)
telephone_data2 = telephone_data1.rename(columns={"1748967": 'technician_id', 'kioopppp': 'name', '0': 'telephone'})
telephone_data3 = telephone_data2.set_index(["technician_id"])
telephone_data4 = telephone_data3.drop_duplicates(["technician_id","name"])

telephone_data5 = pd.read_csv('tb_user.csv', encoding="utf-8", low_memory=False)
telephone_data6 = telephone_data5.set_index(["user_id"])


j = 0
# create the csv file, and write the column name
with open("technician_profile.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['technician_id', 'product_info', 'car_brand', 'report_number', 'first_time', 'last_time',
                     'car_codes', 'recent_one_year', 'recent_half_year', 'recent_three_month', "recent_one_month",
                     "non_working_day", 'car_brand', 'code_number', 'province', 'city', 'detailaddress',
                     'lon_lat_select', " name", 'telephone', 'email'])
# loop read the data of maxcompute table "product_lat_lon", and resolve to address
with t.open_reader() as reader:
    count = reader.count
    for record in reader[1: count]:
        technician_id = int(record[0])
        email = ""
        name = ""
        telephone = ""
        lon_lat_list = []
        city = ""
        province = ""
        detailaddress = ""
        lon_lat_select = ""

        try:
            name = telephone_data4.loc[technician_id]['name']
            telephone = telephone_data4.loc[technician_id]['telephone']
        except:
            pass
        if not name:
            try:
                name = telephone_data6.loc[technician_id]["user_name"]
                telephone = telephone_data6.loc[technician_id]["mobile"]
                email = telephone_data6.loc[technician_id]["email"]
            except:
                pass

        # if there is longitude and latitude, use the "SiJiAddress" API to resolve address
        if record[6] and record[6] != "0.0,0.0":
            lat_lon = record[6].split(">")
            if "0.0,0.0" in lat_lon:
                lat_lon.remove("0.0,0.0")
            for i in range(len(lat_lon)):
                lat = lat_lon[i].split(",")[0]
                lon = lat_lon[i].split(",")[1]
                try:
                    if float(lat) == 0.0 or float(lon) == 0.0:
                        continue
                    if len(lat) < 5 or len(lon) < 5:
                        continue
                except:
                    continue
                lon_lat = lon + "," + lat
                lon_lat_list.append(lon_lat)
            if lon_lat_list:
                # random choice a longitude and latitude
                i = random.choice(range(len(lon_lat_list)))
                lon_lat_select = lon_lat_list[i]
                # use the SiJiAddress API interface
                addr_json = SiJiAddress(lon_lat_select)
                # if the city is Municipality, then write the name of "province"
                if len(addr_json) < 1:
                    continue
                try:
                    if not addr_json['city']:
                        addr_json['city'] = addr_json['province']
                    city = addr_json['city']
                    province = addr_json['province']
                    detailaddress = addr_json['detailaddress']
                except:
                    continue
        # if there is not longitude and latitude, use the file "address_product_series.csv" to map the address
        else:
            try:
                product_series = record[1]
                if product_series:
                    if "," in product_series:
                        product_series = product_series.split(",")[0]
                    city_pinyin = data2.loc[int(product_series)]['city_name']
            except:
                city_pinyin = ''
            if city_pinyin:
                try:
                    city = data4.loc[city_pinyin]['city']
                except:
                    city = ''
                try:
                    province = data4.loc[city_pinyin]['province']
                except:
                    province = ''
            # ignore when city_pinyin map two city
            if type(city) != str:
                city = ""
                province = ""
        # write to csv file
        with open("technician_profile.csv", "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([record[0], record[1], record[2], record[3], record[4], record[5], record[7], record[8],
                             record[9], record[10], record[11], record[12], record[13], record[14], province, city,
                             detailaddress, lon_lat_select, name, telephone, email])
        j += 1
        print(record[0], j, name)




