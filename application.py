# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.gen
import nmap
import os

hosts = os.environ.get("HOSTS", "192.168.1.0/24")


settings = {"debug": True}

class OnlineHostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        nm = nmap.PortScanner()
        result = nm.scan(hosts=hosts, arguments="-sP")
        scan = result.get("scan", {})
        ip_list = scan.keys()
        d = {
            "code": "200",
            "response": ip_list,
            "success": True,
        }
        self.write(d)


class OfflineHostHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        nm = nmap.PortScanner()
        all_ip = nm.scan(hosts=hosts, arguments='-sL')
        all_scan = all_ip.get("scan", {})
        all_ip_list = all_scan.keys()

        online = nm.scan(hosts=hosts, arguments="-sP")
        online_scan = online.get("scan", {})
        online_ip_list = online_scan.keys()

        offline_ip_list =  list(set(all_ip_list).difference(set(online_ip_list)))

        d = {
            "code": "200",
            "response": offline_ip_list,
            "success": True,
        }
        self.write(d)

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/v1/online", OnlineHostHandler),
        (r"/v1/offline", OfflineHostHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
