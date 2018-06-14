import csv
from collections import defaultdict
import re
from odps import ODPS


technician_id_code_num = defaultdict(lambda: defaultdict(int))
# read table diagnose_report from aliyun maxcompute
odps = ODPS('LTAIkLO9entocXgc', 'mCr2aK02tf510aqwAoZRI0QjpTRdTA', 'Launch_DW',
            endpoint='http://service.odps.aliyun.com/api')
t = odps.get_table('recommender_address_clean')
partition = 'address' + '=' + 'Shenzhen' + ',' + "pinyin_theme" + "=" + 'liuzhouwuling'
with t.open_reader(partition=partition) as reader:
    count = reader.count
    print(count)
    for record in reader[0: count]:
        address = record[1]
        fault_code_list = record[3].replace('[','').replace(']','').split(",")
        for fault_code in fault_code_list:
            fault_code = fault_code.replace('"','').replace("'",'').strip()
            if not fault_code:
                continue
            technician_id_code_num[fault_code][address] += 1
    # print(technician_id_code_num)

fault_code_num = technician_id_code_num.keys()
print(len(fault_code_num))
k = 0
for code in fault_code_num:
    k += 1
    for j in range(1):
        max_num = 0
        for i in technician_id_code_num[code].items():
            a = i[1]
            if a > max_num:
                max_num = a
                id = i[0]

        del technician_id_code_num[code][id]
    print(k, code, max_num, id)


