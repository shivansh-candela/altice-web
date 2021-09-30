#!/usr/bin/env python3
from LANforge.lfcli_base import LFCliBase
import port_utils
from port_utils import PortUtils
from pprint import pprint
import pprint
import time

class HTTPProfile(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port, local_realm, debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_url = "http://%s:%s" % (lfclient_host, lfclient_port)
        self.debug = debug_
        self.requests_per_ten = 600
        self.local_realm = local_realm
        self.created_cx = {}
        self.created_endp = []
        self.ip_map = {}
        self.direction = "dl"
        self.dest = "/dev/null"
        self.port_util = PortUtils(self.local_realm)
        self.max_speed = 0 #infinity
        self.quiesce_after = 0 #infinity

    def check_errors(self, debug=False):
        fields_list = ["!conn", "acc.+denied", "bad-proto", "bad-url", "other-err", "total-err", "rslv-p", "rslv-h",
                       "timeout", "nf+(4xx)", "http-r", "http-p", "http-t", "login-denied"]
        endp_list = self.json_get("layer4/list?fields=%s" % ','.join(fields_list))
        debug_info = {}
        if endp_list is not None and endp_list['endpoint'] is not None:
            endp_list = endp_list['endpoint']
            expected_passes = len(endp_list)
            passes = len(endp_list)
            for item in range(len(endp_list)):
                for name, info in endp_list[item].items():
                    for field in fields_list:
                        if info[field.replace("+", " ")] > 0:
                            passes -= 1
                            debug_info[name] = {field: info[field.replace("+", " ")]}
            if debug:
                print(debug_info)
            if passes == expected_passes:
                return True
            else:
                print(list(debug_info), " Endps in this list showed errors getting to its URL")  # %s") % self.url)
                return False

    def start_cx(self):
        print("Starting CXs...")
        for cx_name in self.created_cx.keys():
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": self.created_cx[cx_name],
                "cx_state": "RUNNING"
            }, debug_=self.debug)
            print(".", end='')
        print("")

    def stop_cx(self):
        print("Stopping CXs...")
        for cx_name in self.created_cx.keys():
            self.json_post("/cli-json/set_cx_state", {
                "test_mgr": "default_tm",
                "cx_name": self.created_cx[cx_name],
                "cx_state": "STOPPED"
            }, debug_=self.debug)
            print(".", end='')
        print("")

    def cleanup(self):
        print("Cleaning up cxs and endpoints")
        if len(self.created_cx) != 0:
            for cx_name in self.created_cx.keys():
                req_url = "cli-json/rm_cx"
                data = {
                    "test_mgr": "default_tm",
                    "cx_name": self.created_cx[cx_name]
                }
                self.json_post(req_url, data)
                # pprint(data)
                req_url = "cli-json/rm_endp"
                data = {
                    "endp_name": cx_name
                }
                self.json_post(req_url, data)
                # pprint(data)

    def map_sta_ips(self, sta_list=[]):
        for sta_eid in sta_list:
            eid = self.local_realm.name_to_eid(sta_eid)
            sta_list = self.json_get("/port/%s/%s/%s?fields=alias,ip" %
                                     (eid[0], eid[1], eid[2]))
            if sta_list['interface'] is not None:
                self.ip_map[sta_list['interface']['alias']] = sta_list['interface']['ip']

    def create(self, ports=[], sleep_time=.5, debug_=False, suppress_related_commands_=None, http=False, ftp=False,
               https=False, user=None, passwd=None, source=None, ftp_ip=None, upload_name=None, http_ip=None, https_ip=None):
        cx_post_data = []
        self.map_sta_ips(ports)
        print("Create CXs...")

        for i in range(len(list(self.ip_map))):
            url = None
            if i != len(list(self.ip_map)) - 1:
                port_name = list(self.ip_map)[i]
                ip_addr = self.ip_map[list(self.ip_map)[i + 1]]
            else:
                port_name = list(self.ip_map)[i]
                ip_addr = self.ip_map[list(self.ip_map)[0]]

            if (ip_addr is None) or (ip_addr == ""):
                raise ValueError("HTTPProfile::create encountered blank ip/hostname")

            shelf = self.local_realm.name_to_eid(port_name)[0]
            resource = self.local_realm.name_to_eid(port_name)[1]
            name = self.local_realm.name_to_eid(port_name)[2]

            if upload_name != None:
                name = upload_name

            if http:
                if http_ip is not None:
                    self.port_util.set_http(port_name=name, resource=resource, on=True)
                    url = "%s http://%s %s" % (self.direction, http_ip, self.dest)
                else:
                    self.port_util.set_http(port_name=name, resource=resource, on=True)
                    url = "%s http://%s/ %s" % (self.direction, ip_addr, self.dest)
            if https:
                if https_ip is not None:
                    self.port_util.set_http(port_name=name, resource=resource, on=True)
                    url = "%s https://%s %s" % (self.direction, https_ip, self.dest)
                else:
                    self.port_util.set_http(port_name=name, resource=resource, on=True)
                    url = "%s https://%s/ %s" % (self.direction, ip_addr, self.dest)

            if ftp:
                self.port_util.set_ftp(port_name=name, resource=resource, on=True)
                if user is not None and passwd is not None and source is not None:
                    if ftp_ip is not None:
                        ip_addr=ftp_ip
                    url = "%s ftp://%s:%s@%s%s %s" % (self.direction, user, passwd, ip_addr, source, self.dest)
                    print("###### url:{}".format(url))
                else:
                    raise ValueError("user: %s, passwd: %s, and source: %s must all be set" % (user, passwd, source))
            if not http and not ftp and not https:
                raise ValueError("Please specify ftp and/or http")

            if (url is None) or (url == ""):
                raise ValueError("HTTPProfile::create: url unset")

            if upload_name ==None:
                endp_data = {
                    "alias": name + "_l4",
                    "shelf": shelf,
                    "resource": resource,
                    "port": name,
                    "type": "l4_generic",
                    "timeout": 10,
                    "url_rate": self.requests_per_ten,
                    "url": url,
                    "proxy_auth_type": 0x200,
                    "max_speed": self.max_speed,
                    "quiesce_after": self.quiesce_after}
            else:
                endp_data = {
                    "alias": name + "_l4",
                    "shelf": shelf,
                    "resource": resource,
                    "port": ports[0],
                    "type": "l4_generic",
                    "timeout": 10,
                    "url_rate": self.requests_per_ten,
                    "url": url,
                    "ssl_cert_fname": "ca-bundle.crt",
                    "proxy_port": 0,
                    "max_speed": self.max_speed,
                    "proxy_auth_type": 0x200,
                    "quiesce_after": self.quiesce_after
                }
            url = "cli-json/add_l4_endp"
            self.local_realm.json_post(url, endp_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands_)
            time.sleep(sleep_time)

            endp_data = {
                "alias": "CX_" + name + "_l4",
                "test_mgr": "default_tm",
                "tx_endp": name + "_l4",
                "rx_endp": "NA"
            }
            cx_post_data.append(endp_data)
            self.created_cx[name + "_l4"] = "CX_" + name + "_l4"

        for cx_data in cx_post_data:
            url = "/cli-json/add_cx"
            self.local_realm.json_post(url, cx_data, debug_=debug_,
                                       suppress_related_commands_=suppress_related_commands_)
            time.sleep(sleep_time)
