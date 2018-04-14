from urllib import request
import json


# 输入高德经纬度，获得详细的四级地址
def SiJiAddress(location):
    # 构造uri地址
    key = '5358d1aa58f3dc1ff8e2bfe17121038d'
    url = 'http://restapi.amap.com/v3/geocode/regeo?'
    uri = url + '&key=' + key + '&location=' + location + '&output=json'
    # 请求得到一个json格式的地址
    req = request.urlopen(uri)
    res = req.read().decode()
    answer = json.loads(res)

    SiJiAddress = {}

    if answer['status'] == '1':
        addresscomponent = answer['regeocode']['addressComponent']
        country = "中国"
        SiJiAddress['country'] = country
        country = addresscomponent['country']
        if len(addresscomponent['province']) > 0:
            province = addresscomponent['province']
            SiJiAddress['province'] = province
        else:
            province = ''
            SiJiAddress['province'] = province

        if len(addresscomponent['city']) > 0:
            city = addresscomponent['city']
            SiJiAddress['city'] = city
        else:
            city = ''
            SiJiAddress['city'] = city

        if len(addresscomponent['district']) > 0:
            district = addresscomponent['district']
            SiJiAddress['district'] = district
        else:
            district = ''
            SiJiAddress['district'] = district

        if len(answer['regeocode']['formatted_address']) > 0:
            detailaddress = answer['regeocode']['formatted_address']
            SiJiAddress['detailaddress'] = detailaddress
        else:
            detailaddress = ''
            SiJiAddress['detailaddress'] = detailaddress

    return SiJiAddress


if __name__ == "__main__":
    print(SiJiAddress("120.37189999999998,36.098600000000005"))

