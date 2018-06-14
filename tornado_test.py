# -*- coding: utf-8 -*-
#

from tornado.ioloop import IOLoop
from tornado import gen, web
from tornado_mysql import pools


connParam = {'host': 'rm-wz9v9e07mh753tk321o.mysql.rds.aliyuncs.com', 'port': 3306, 'user': 'diagnose_report',\
              'passwd': 'launch@1234', 'db': 'dmstest', "charset": "utf8"}


class GetUserHandler(web.RequestHandler):
    POOL = pools.Pool(connParam, max_idle_connections=1, max_recycle_sec=3)

    @gen.coroutine
    def get(self):
        city = self.get_argument('city')
        brand = self.get_argument('brand')
        city = "'" + city + "'"
        brand = "'%" + brand + "%'"
        # print('select * from technician_profile where city = %s and car_brand like %s order\
        #  by report_number desc limit 20' % (city, brand))
        cursor = yield self.POOL.execute('select technician_id, city, detailaddress from technician_profile where city = %s and car_brand like %s order\
        by report_number desc limit 20' % (city, brand))
        context = cursor.fetchall()
        context = context.__str__()
        # context = context.encode("utf-8")
        print(context)
        if cursor.rowcount > 0:
            self.write('<meta charset="utf-8">' + '"status": 0, "name":' + context)
        else:
            self.write({"status": 0, "name": ""})
        self.finish()


application = web.Application([(r"/city", GetUserHandler)], autoreload=True)
application.listen(8080)
IOLoop.current().start()

