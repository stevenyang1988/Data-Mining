from launch.gaode_api import SiJiAddress
import csv
from collections import defaultdict

# 创建字典
province_report_num = defaultdict(int)
city_report_num = defaultdict(int)
# 创建csv文件，并写入列名
# with open("data.csv","w",newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['province', 'city', 'lon_lan', 'number'])


# 字典转换为csv文件函数
def dict2csv(dict, file):
    with open(file, 'w',  newline='') as f:
        w = csv.writer(f)
        # write each key/value pair on a separate row
        w.writerows(dict.items())


if __name__ == "__main__":
    # 读取源表数据
    with open("f:\\data\\report_201802_preprocessing.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for record in reader:
            if reader.line_num == 1:
                continue
            # 读取经纬度，并转换成地址
            location = record[0]
            addr_json = SiJiAddress(location)
            # 如果是直辖市，则city字段填直辖市名
            if not addr_json['city']:
                addr_json['city'] = addr_json['province']
            if len(addr_json) < 1:
                continue
            # 将每个省份、地级市的报告统计出来
            with open("f:\\data\\address_info.csv", "r", newline='', encoding='utf-8') as csvfile:
                reader1 = csv.reader(csvfile)
                # 计算每个地级市的诊断报告数量
                for record1 in reader1:
                    if reader1.line_num == 1:
                        continue
                    if record1[3] == addr_json['city']:
                        city_report_num[addr_json['city']] += int(record[1])
                # 计算每个省的诊断报告数量
                for record1 in reader1:
                    if reader1.line_num == 1:
                        continue
                    if record1[2] == addr_json['province']:
                        province_report_num[addr_json['province']] += int(record[1])
                        break

            # with open("data.csv", "a", newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerow([addr_json['province'], addr_json['city'], record[0], record[1]])
    # 将数据存入csv文件
    dict2csv(city_report_num, "city_success1.csv")
    dict2csv(province_report_num, "province_success1.csv")
print("转换完成")
