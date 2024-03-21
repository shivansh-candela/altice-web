from statistics import mode
from django.db import models
from jsonfield import JSONField
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask,ClockedSchedule
from pytest_web_ui.settings import BASE_DIR1
from .enums import TimeInterval, SetupStatus
import json as jsn
from django.conf import settings
from datetime import datetime
from django import forms
import os
import uuid
import string
import re
# Create your models here.
class Tester(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    chart=models.JSONField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "        Tester"
    
    def __str__(self):
        return self.name
        
class AccessPoint(models.Model):
    model = models.CharField(max_length=20,null=False,help_text="Enter DUT Model name: [Example: Netgear AP]",verbose_name="DUT Model")
    mode = models.CharField(max_length=20,null=False,help_text="Enter Wi-Fi Standards [Example : wifi6,wifi5,wifi4]",verbose_name="Wi-Fi Standards")
    serial = models.CharField(max_length=50,help_text="Enter DUT Serial Number [Example: 1234567890]",verbose_name="DUT Serial number")
    jumphost = models.CharField(max_length=20,null=False,default="true",help_text="Always true",verbose_name="Jumphost")
    ip = models.GenericIPAddressField(protocol='IPv4',unique=True,null=False,help_text="Enter Lanforge IP Address [Example: 192.168.200.10]",verbose_name="Lanforge IP")
    username = models.CharField(max_length=20,null=False,help_text="Enter Lanforge Username [Example: lanforge]",verbose_name="Lanforge Username")
    password = models.CharField(max_length=20,null=False,help_text="Enter Lanforge Password [Example: lanforge]",verbose_name="Lanforge Password")
    port = models.CharField(max_length=20,null=False,help_text="Enter Lanforge SSH Port number [Example: 22]",verbose_name="Lanforge SSH port number")
    jumphost_tty = models.CharField(max_length=20,null=False,help_text="Enter the serial connection tty [Example: /dev/ttyUSB0]",verbose_name="Serial Connection tty")
    version = models.CharField(max_length=20,default='',blank=True,help_text="Enter DUT Firmware version [Example : next-latest] ",verbose_name="Firmware Version")
    ap_username = models.CharField(max_length=20,null=False,help_text="Enter AP Username",verbose_name="AP Username",default="admin")
    ap_password = models.CharField(max_length=20,null=False,help_text="Enter Access Point Password [Example: AP Password] ",verbose_name="AP Password",default="DustBunnyRoundup9#")
    ap_prompt = models.CharField(max_length=20,null=False,help_text="Enter the tty location [Example: root@GEN8]",verbose_name="AP Prompt",default="root@GEN8")
    image = models.ImageField(upload_to = 'images',null=True,blank=True,help_text="Choose the image of the AP[Example : .img .png, .jpg, .jpeg file]",verbose_name="DUT Image")
    attached = models.BooleanField(default=False,help_text="Attached: Enable(The AP is attached to a Testbed")
    use_ssh = models.BooleanField(default=True,help_text="Attached: Enable By default")
    class Meta:
        verbose_name_plural = "       Accesspoint"
    def __str__(self):
        return self.model

class TrafficGenerator(models.Model):
    name = models.CharField(max_length=100,null=False,help_text="Enter Traffic Generator Name [ Example – LANforge]",verbose_name="Traffic Generator Name")
    ip = models.GenericIPAddressField(protocol='IPv4',unique=True,null=False,help_text="Enter Traffic Generator IP Address [Example : 192.168.200.100]",verbose_name="Traffic Generator IP")
    port = models.CharField(max_length=100,null=False,help_text="Enter HTTP Port Number [Example : 8080]",verbose_name="HTTP Port")
    ssh_port = models.CharField(max_length=100,null=False,help_text="Enter SSH Port Number [Example : 22]",verbose_name="SSH Port")
    twog_radio = models.CharField(max_length=100,null=False,help_text="Enter 2.4GHz Radio interface name [Example : 1.1.wiphy0,1.1.wiphy1] (Seperate Multiple Radios With Comma)",verbose_name="2.4GHz Radio")
    fiveg_radio = models.CharField(max_length=100,null=False,help_text="Enter 5GHz Radio interface name [Example : 1.1.wiphy0,1.1.wiphy1] (Seperate Multiple Radios With Comma)",verbose_name="5GHz Radio")
    ax_radio = models.CharField(max_length=100,blank=True,default='',help_text="Enter Ax Radio interface name [Example : 1.1.wiphy0,1.1.wiphy2] (Seperate multiple radios with comma)",verbose_name="Ax Radio")
    upstream = models.CharField(max_length=100,null=False,help_text="Enter the port which is used to run traffic [Example : 1.1.eth1]",verbose_name="WAN Upstream Port")
    lan_upstream = models.CharField(max_length=100,blank=True,default='',help_text="Enter the port which is used to run traffic [Example : 1.1.eth1]",verbose_name="LAN Upstream Port")
    upstream_subnet = models.CharField(default="",editable=False,max_length=100,help_text="Enter Upstream Subnet address [Example : 192.168.200.100.1/24]")
    uplink = models.CharField(default="",editable=False,max_length=100,help_text="Enter uplink port [Example : eth1]")
    twog_station_name = models.CharField(max_length=100,null=False,help_text="Enter 2.4Ghz station name [Example : sta0]",verbose_name="2.4GHz Station Name")
    fiveg_station_name = models.CharField(max_length=100,null=False,help_text="Enter 5Ghz station name [Example : sta1]",verbose_name="5GHz Station Name")
    ax_station_name = models.CharField(max_length=100,default='',blank=True,help_text="Enter Ax station name [Example : ax]",)
    attenuation_connected_serial = models.CharField(max_length=100,blank=True,default='',help_text="Enter Connected Attenuator [Example : 3258,3456] (Seperate Multiple Attenuation Values With Comma)",verbose_name="Connected Serial Atenuator")
    attenuation_selected_serial = models.CharField(max_length=100,blank=True,default='',help_text="Enter Selected Attenuator [Example : 3258,3456] (Seperate Multiple Attenuation Values With Comma)",verbose_name="Selected Serial Attenuator")
    attached = models.BooleanField(default=False,help_text="Attached: Enable(The Traffic Generator is attached to a Testbed")
    


    image = models.ImageField(upload_to = 'images',null=True,blank=True)


    class Meta:
        verbose_name_plural = "      Traffic Generators"
    
    def __str__(self):
        return self.name

class Testbed(models.Model):
    base_directory=settings.BASE_DIR
    testbedname = models.CharField(unique=True,max_length=50,null=False,help_text=" ")
    accesspoint = models.ForeignKey(AccessPoint,on_delete=models.CASCADE,null=False)
    trafficgenerator = models.ForeignKey(TrafficGenerator,on_delete=models.CASCADE,null=False)
    status = models.BooleanField(default=True,help_text="Reservation Status: Enable(Unreserved Testbed)")
    availability = models.BooleanField(default=True,help_text="To disable the testbed the testbed status to be enabled by default.")

    def __str__(self):
        return self.testbedname
    class Meta:
            verbose_name_plural = "     Testbed"
    def delete(self, *args, **kwargs):
        accesspoint_primary_key_data = AccessPoint.objects.filter(pk=self.accesspoint_id)
        trafficgenerator_primary_key_data = TrafficGenerator.objects.filter(pk=self.trafficgenerator_id)
        accesspoint_primary_key_data.update(attached=False)
        trafficgenerator_primary_key_data.update(attached=False)
        TestScheduler.objects.filter(testbed=self.testbedname).update(status='Aborted')
        TestScheduler.objects.filter(testbed=self.testbedname).update(completed=True)
        base_directory=settings.BASE_DIR
        f=open(base_directory+'/static/admin/data_files/testbeds.json','r+')
        testbeds = jsn.load(f)
        testbed_names = testbeds['testbed names']
        testbed_names.remove(self.testbedname)
        testbeds['testbed names'] = testbed_names
        f.close()
        f=open(base_directory+'/static/admin/data_files/testbeds.json','w+')
        f.write(jsn.dumps(testbeds,indent=4))
        f.close()
        # jsn.dump(testbeds,f,indent=4)
        super().delete(*args, **kwargs)
        base_directory=settings.BASE_DIR1
        config_file_dir=base_directory+"/wlan-testing/tests/lab_info.json"
        f=open(config_file_dir,'r+')
        data=jsn.load(f)
        f.close()
        del data['CONFIGURATION'][self.testbedname]
        with open(config_file_dir, 'w') as f:
            jsn.dump(data, f, indent=4)
            f.close()
    def save(self, *args, **kwargs):
        AccessPoint.objects.filter(pk=self.accesspoint_id).update(attached=True)
        TrafficGenerator.objects.filter(pk=self.trafficgenerator_id).update(attached=True)
        base_directory=settings.BASE_DIR
        f=open(base_directory+'/static/admin/data_files/testbeds.json','r+')
        testbeds = jsn.load(f)
        if('testbed names' in testbeds.keys()):
            testbed_names = testbeds['testbed names']
            if(self.testbedname not in testbed_names):
                testbed_names.append(self.testbedname)
            testbeds['testbed names'] = testbed_names
        else:
            testbeds['testbed names'] = [self.testbedname,]
        f.seek(0)
        jsn.dump(testbeds,f,indent=4)
        super().save(*args, **kwargs)
        testbed_data = list(Testbed.objects.values())
        final = []
        list1 = dict()
        for tb in testbed_data:
            accesspoint_primary_key_data = AccessPoint.objects.filter(
                pk=tb.get('accesspoint_id'))  # getting the pk of AP
            lanforge_primary_key_data = TrafficGenerator.objects.filter(
                pk=tb.get('trafficgenerator_id'))  # getting the pk of LF
            accesspoint_primary_key_data_list = list(accesspoint_primary_key_data.values())[0]  # gettign the list of AP
            lanforge_primary_key_data_list = list(lanforge_primary_key_data.values())  # getting the list
            tb['accesspoint_id'] = accesspoint_primary_key_data_list
        # print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",lanforge_data)
            tb['trafficgenerator_id'] = lanforge_primary_key_data_list
            # print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",lanforge_data)
            final.append(tb)
        # print("kjfsdnfkjnfkjne",final)
            # print("\n\n\n",final)
            #list1 = dict()
            for f in final:         
                context = {
                    f.get('testbedname'): {
                        'controller': {
                            # API base url for the controller
                            'url': 'asd',
                            'username': "asdsa",
                            'password': 'dasd',
                        },
                        'access_point': [
                            f.get('accesspoint_id')
                        ],

                        'traffic_generator': {
                            'name': f.get('trafficgenerator_id')[0]['name'],
                            'details': {
                                # f.get('trafficgenerator_id')[0],
                                'ip': f.get('trafficgenerator_id')[0]['ip'],
                                'port': f.get('trafficgenerator_id')[0]['port'],
                                'ssh_port': f.get('trafficgenerator_id')[0]['ssh_port'],
                                '2.4G-Radio': f.get('trafficgenerator_id')[0]['twog_radio'].strip("\\\"").split(','),
                                '5G-Radio': f.get('trafficgenerator_id')[0]['fiveg_radio'].strip("\\\"").split(','),
                                'AX-Radio': [ i.lstrip(' ') for i in f.get('trafficgenerator_id')[0]['ax_radio'].strip("\\\"").split(',') if f.get('trafficgenerator_id')[0]['ax_radio']!="" or f.get('trafficgenerator_id')[0]['ax_radio']!=None ],
                                'upstream': f.get('trafficgenerator_id')[0]['upstream'],
                                'lan-upstream': f.get('trafficgenerator_id')[0]['lan_upstream'],
                                'upstream_subnet': f.get('trafficgenerator_id')[0]['upstream_subnet'],
                                'uplink': f.get('trafficgenerator_id')[0]['uplink'],
                                '2.4G-Station-Name': f.get('trafficgenerator_id')[0]['twog_station_name'],
                                '5G-Station-Name': f.get('trafficgenerator_id')[0]['fiveg_station_name'],
                                'AX-Station-Name': f.get('trafficgenerator_id')[0]['ax_station_name'],
                                'attenuation_connected_serial' : [ i.lstrip(' ') for i in f.get('trafficgenerator_id')[0]['attenuation_connected_serial'].strip("\\\"").split(',') if f.get('trafficgenerator_id')[0]['attenuation_connected_serial']!="" or f.get('trafficgenerator_id')[0]['attenuation_connected_serial']!=None ],
                                'attenuation_selected_serial' :  [ i.lstrip(' ') for i in f.get('trafficgenerator_id')[0]['attenuation_selected_serial'].strip("\\\"").split(',') if f.get('trafficgenerator_id')[0]['attenuation_selected_serial']!="" or f.get('trafficgenerator_id')[0]['attenuation_selected_serial']!=None ],
                            }
                        }
                    }
                }
                # if(context[f.get('testbedname')]['access_point'][0]['serial']=="\"\""):
                context[f.get('testbedname')]['access_point'][0]['serial']=""
                if(context[f.get('testbedname')]['traffic_generator']['details']['upstream_subnet']=="\"\""):
                    context[f.get('testbedname')]['traffic_generator']['details']['upstream_subnet']=""
                if(context[f.get('testbedname')]['traffic_generator']['details']['uplink']=="\"\""):
                    context[f.get('testbedname')]['traffic_generator']['details']['uplink']=""
                if(context[f.get('testbedname')]['traffic_generator']['details']['attenuation_connected_serial'][0]==""):
                    context[f.get('testbedname')]['traffic_generator']['details']['attenuation_connected_serial'] = ""
                if(context[f.get('testbedname')]['traffic_generator']['details']['attenuation_selected_serial'][0]==""):
                    context[f.get('testbedname')]['traffic_generator']['details']['attenuation_selected_serial'] = ""
                list1.update(context)
            config = {
                'CONFIGURATION': list1,
                "PERFECTO_DETAILS" : 
                {
                    "securityToken":"eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3NzkzZGM0Ni1jZmU4LTQ4ODMtYjhiOS02ZWFlZGU2OTc2MDkifQ.eyJpYXQiOjE2MzI4Mzc2NDEsImp0aSI6IjAwZGRiYWY5LWQwYjMtNDRjNS1hYjVlLTkyNzFlNzc5ZGUzNiIsImlzcyI6Imh0dHBzOi8vYXV0aDIucGVyZmVjdG9tb2JpbGUuY29tL2F1dGgvcmVhbG1zL3RpcC1wZXJmZWN0b21vYmlsZS1jb20iLCJhdWQiOiJodHRwczovL2F1dGgyLnBlcmZlY3RvbW9iaWxlLmNvbS9hdXRoL3JlYWxtcy90aXAtcGVyZmVjdG9tb2JpbGUtY29tIiwic3ViIjoiODNkNjUxMWQtNTBmZS00ZWM5LThkNzAtYTA0ZjBkNTdiZDUyIiwidHlwIjoiT2ZmbGluZSIsImF6cCI6Im9mZmxpbmUtdG9rZW4tZ2VuZXJhdG9yIiwibm9uY2UiOiI2ZjE1YzYxNy01YTU5LTQyOWEtODc2Yi1jOTQxMTQ1ZDFkZTIiLCJzZXNzaW9uX3N0YXRlIjoiYmRjZTFmYTMtMjlkYi00MmFmLWI5YWMtYjZjZmJkMDEyOTFhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBvZmZsaW5lX2FjY2VzcyBlbWFpbCJ9.5R85_1R38ZFXv_wIjjCIsj8NJm1p66dCsLJI5DBEmks",
                    "projectName": "TIP-PyTest-Execution",
                    "projectVersion": "1.0",
                    "reportTags": "TestTag",
                    "perfectoURL":"tip",
                    "iPhone-11": {
                        "model-iOS": "iPhone-11",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-11",
                        "jobNumber": 38
                    },
                    "iPhone-12": {
                        "model-iOS": "iPhone-12",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-12",
                        "jobNumber": 38
                    },
                    "iPhone-7": {
                        "model-iOS": "iPhone-7",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-7",
                        "jobNumber": 38
                    },
                    "iPhone-XR": {
                        "model-iOS": "iPhone-XR",
                        "bundleId-iOS": "com.apple.Preferences",
                        "platformName-iOS": "iOS",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Ping": "com.deftapps.ping",
                        "browserType-iOS": "Safari",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "platformName-android": "Android",
                        "appPackage-android": "com.android.settings",
                        "jobName": "Interop-iphone-XR",
                        "jobNumber": 38
                    },
                    "Galaxy S20": {
                        "platformName-android": "Android",
                        "model-android": "Galaxy S20",
                        "appPackage-android": "com.android.settings",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "jobName": "Interop-Galaxy-S20",
                        "jobNumber": 38
                    },
                    "Galaxy S10.*": {
                        "platformName-android": "Android",
                        "model-android": "Galaxy S10.*",
                        "appPackage-android": "com.android.settings",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "jobName": "Interop-Galaxy-S10",
                        "jobNumber": 38
                    },
                    "Galaxy S9": {
                        "platformName-android": "Android",
                        "model-android": "Galaxy S9",
                        "appPackage-android": "com.android.settings",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "jobName": "Interop-Galaxy-S9",
                        "jobNumber": 38
                    },
                    "Pixel 4": {
                        "platformName-android": "Android",
                        "model-android": "Pixel 4",
                        "appPackage-android": "com.android.settings",
                        "bundleId-iOS-Settings": "com.apple.Preferences",
                        "bundleId-iOS-Safari": "com.apple.mobilesafari",
                        "jobName": "Interop-pixel-4",
                        "jobNumber": 38
                    }
                },
                'RADIUS_SERVER_DATA': {
                    'ip': '10.10.1.221',
                    "port": 1812,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "RADIUS_ACCOUNTING_DATA": {
                    "ip": "10.10.1.221",
                    "port": 1813,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "DYNAMIC_VLAN_RADIUS_SERVER_DATA": {
                    "ip": "3.20.165.131",
                    "port": 1812,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "DYNAMIC_VLAN_RADIUS_ACCOUNTING_DATA": {
                    "ip": "3.20.165.131",
                    "port": 1813,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "RATE_LIMITING_RADIUS_SERVER_DATA": {
                    "ip": "18.189.85.200",
                    "port": 1812,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "RATE_LIMITING_RADIUS_ACCOUNTING_DATA": {
                    "ip": "18.189.85.200",
                    "port": 1813,
                    "secret": "testing123",
                    "user": "user",
                    "password": "password",
                    "pk_password": "whatever"
                },

                "PASSPOINT_RADIUS_SERVER_DATA": {
                    "ip": "52.234.179.191",
                    "port": 11812,
                    "secret": "yeababy20!",
                    "user": "nolaradius",
                    "password": "nolastart",
                    "pk_password": "whatever"
                },

                "PASSPOINT_RADIUS_ACCOUNTING_SERVER_DATA": {
                    "ip": "52.234.179.191",
                    "port": 11813,
                    "secret": "yeababy20!"
                },

                "PASSPOINT_PROVIDER_INFO": {
                    "mcc": None,
                    "mnc": None,
                    "network": None,
                    "nai_realms": {
                        "domain": "oss.ameriband.com",
                        "encoding": 0,
                        "eap_map": {"EAP-TTLS with username/password": ["Credential Type:username/password",
                                                                        "Non-EAP Inner Authentication Type:MSCHAPV2"]}
                    },
                    "osu_nai_standalone": "anonymous@ameriband.com",
                    "osu_nai_shared": "anonymous@ameriband.com",
                    "roaming_oi": []
                },

                "PASSPOINT_OPERATOR_INFO": {
                    "osen": "Disabled",
                    "domain_name_list": ["telecominfraproject.atlassian.net"],
                    "operator_names": [
                            {"locale": "eng", "name": "Default friendly passpoint_operator name"},
                            {"locale": "fra", "name": "Nom de lopérateur convivial par défaut"}
                    ]
                },

                "PASSPOINT_VENUE_INFO": {
                    "venue_type": {"group": "Business", "type": "Police Station"},
                    "venue_names": [
                        {"locale": "eng", "name": "Example passpoint_venue",
                        "url": "http://www.example.com/info-eng"},
                        {"locale": "fra", "name": "Exemple de lieu",
                        "url": "http://www.example.com/info-fra"}
                    ]
                },

                "PASSPOINT_PROFILE_INFO": {
                    "profile_download_url_ios": "https://onboard.almondlabs.net/ttls/AmeriBand-Profile.mobileconfig",
                    "profile_download_url_android": "https://onboard.almondlabs.net/ttls/androidconfig.cfg",
                    "profile_name_on_device": "AmeriBand",
                    "radius_configuration": {
                        "user_defined_nas_id": "FB001AP001",
                        "operator_id": "AmeribandTIP",
                        "radius_acounting_service_interval": 60
                    },
                    "interworking_hs2dot0": "Enabled",
                    "hessid": None,
                    "access_network": {
                        "Access Network Type": "Free Public Network",
                        "Authentication Type": "Acceptance of Terms & Conditions",
                        "Emergency Services Reachable": "Enabled",
                        "Unauthenticated Emergency Service": "Disabled"
                    },
                    "ip_connectivity": {
                        "Internet Connectivity": "Enabled",
                        "IP Address Type": "Public IPv4 Address Available",
                        "Connection Capability": [{"status": "open", "protocol": "TCP", "port": 8888}],
                        "ANQP Domain ID": 1234,
                        "GAS Address 3 Behaviour": "P2P Spec Workaround From Request",
                        "Disable DGAF": False
                    }
                },
                "open_flow":{},
                "influx_params" : {},
                "AP_CLI": {
                    "wireless_ssid_details_2g": "/wireless/basic/show --wifi-index=0",
                    "wireless_ssid_details_5g": "/wireless/basic/show --wifi-index=1",
                    "wireless_ssid_client_connectivity_2g": "/wireless/basic/config --wifi-index=0 --wifi-ssid=client_connectivity_altice",
                    "wireless_ssid_client_connectivity_5g": "/wireless/basic/config --wifi-index=1 --wifi-ssid=client_connectivity_altice",
                    "wireless_sec_show_2g": "/wireless/security/show --wifi-index=0",
                    "wireless_sec_show_5g": "/wireless/security/show --wifi-index=1",
                    "wireless_ssid_open_config_2g": "/wireless/security/config --wifi-index=0 --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=None",
                    "wireless_ssid_open_config_5g": "/wireless/security/config --wifi-index=1 --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=None",
                    "wireless_ssid_wpa2_personal_config_2g": "/wireless/security/config --wifi-index=0 --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=WPA2-Personal --wifi-wl-wpa-passphrase=something",
                    "wireless_ssid_wpa2_personal_config_5g": "/wireless/security/config --wifi-index=1 --wifi-sec-choose-interface=0 --wifi-wl-auth-mode=WPA2-Personal --wifi-wl-wpa-passphrase=something"
                }
            }
            # print("\n\n\n\n",context)
            # print("\n\n\n\n",config)
        base_directory=settings.BASE_DIR1
        config_file_dir=base_directory+"/wlan-testing/tests/lab_info.json"
        # config_file_dir_2 = "/home/akhilesh/Desktop/ctpriv-scripts/altice/wlan-testing/tests/lab_info.json"
        with open(config_file_dir, 'w') as f:
            jsn.dump(config, f, indent=4)
            f.close()
        # with open(config_file_dir_2, 'w') as f:
        #     jsn.dump(config, f, indent=4)
        #     f.close()

class TBForm(forms.ModelForm):
    class Meta:
        model = Testbed
        fields = '__all__'
    def clean(self):
        cleaned_data=self.cleaned_data
        pattern = r'^[' + string.punctuation + ']+'
        if re.search(pattern, cleaned_data.get('testbedname')) is not None:
            raise forms.ValidationError("Testbed name can not be started with a special character")
        if(cleaned_data.get('status')==False and cleaned_data.get('availability')==False):
            raise forms.ValidationError("Testbed is reserved. Cannot disable it.")

class TestScheduler(models.Model):
    tester=models.ForeignKey(Tester,on_delete=models.CASCADE)
    tester_name=models.CharField(max_length=100,null=True,blank=False)
    name=models.CharField(max_length=50,default="abcd")
    task=models.CharField(max_length=50,default="resources.tasks.collect_marker_task")
    #pytest_m = models.CharField(max_length=500,default="pytest -m")
    testplan = models.CharField(max_length=500,null=True,blank=False)
    accesspoint = models.CharField(max_length=500,null=True,blank=False)
    accesspoint_mode = models.CharField(max_length=500,null=True,blank=False)
    accesspoint_serial = models.CharField(max_length=500,null=True,blank=False)
    trafficgenerator = models.CharField(max_length=500,null=True,blank=False)
    #testbed_n = models.CharField(max_length=500,default="--testbed =")
    testbed = models.CharField(max_length=500,null=True,blank=False)
    starttime = models.CharField(unique=True,max_length=50,null=True)
    estimated_time = models.CharField(max_length=50,null=True,blank=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=100,default="Pending")
    firmware_name = models.CharField(max_length=50,null=True)
    created_at_dt=datetime.now().month
    created_at_dt=str(created_at_dt)
    # created_at_dt=datetime.strptime(str(created_at_dt), "%m")
    # created_at_dt=created_at_dt.strftime("%B").lower()
    sprint="RC-"+created_at_dt
    created_at = models.CharField(max_length=200,default=sprint)
    celery_task_id = models.CharField(max_length=200,default=0)
    total_passed = models.IntegerField(default=0)
    total_failed = models.IntegerField(default=0)
    total_error = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0)
    total_testcases = models.CharField(max_length=200,default=0)
    remarks = models.CharField(max_length=200,default="No Remarks")
    evaluator = models.CharField(max_length=200,default="None")

    def __str__(self):
        return self.tester.name+"_"+self.starttime+"_"+self.testbed


class Testplan(models.Model):
    testplan_name=models.CharField(unique=True,max_length=50,null=True,blank=False)
    testplan_marker=models.CharField(unique=True,max_length=500,null=True,blank=True)
    tester_id=models.CharField(unique=False,max_length=50,null=True,blank=True,default="admin")
    features=models.CharField(max_length=500,null=True,blank=True)
    band=models.CharField(max_length=50,null=True,blank=True)
    security=models.CharField(max_length=50,null=True,blank=True)
    channels=models.CharField(max_length=50,null=True,blank=True)
    bandwidth=models.CharField(max_length=50,null=True,blank=True)
    protocol=models.CharField(max_length=50,null=True,blank=True)
    sub_feature=models.CharField(max_length=50,null=True,blank=True)
    time=models.CharField(max_length=50,null=True,blank=True)
    unique_features = models.CharField(max_length=500,null=True,blank=True)
    unique_band = models.CharField(max_length=500,null=True,blank=True)
    unique_security = models.CharField(max_length=500,null=True,blank=True)
    unique_channels = models.CharField(max_length=500,null=True,blank=True)
    unique_bandwidth = models.CharField(max_length=500,null=True,blank=True)
    unique_protocol = models.CharField(max_length=500,null=True,blank=True)
    testcases = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    data=JSONField(null=True,blank=True)
    Total_Testcases=models.CharField(max_length=50,null=True,blank=True)
    Estimated_Time=models.CharField(max_length=50,null=True,blank=True)
    class Meta:
        verbose_name_plural = " Testplan"
    def __str__(self):
        return self.testplan_name
class FirmwareImage(models.Model):
    firmware_name=models.CharField(unique=True,max_length=50,null=True,blank=False,help_text="Enter the Firmware version of the DUT [Example : V1.0.0.100]",verbose_name="Firmware Version")
    class Meta:
        verbose_name_plural = "    Firmware Image"
    def __str__(self):
        return self.firmware_name

class ReleaseCycle(models.Model):
    release_cycle_name=models.CharField(unique=True,max_length=50,null=True,blank=False)
    start_date=models.DateTimeField(unique=True,max_length=50,null=True,blank=False)
    end_date=models.DateTimeField(unique=True,max_length=50,null=True,blank=False)
    relid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        verbose_name_plural = "   Release Cycle"
    def __str__(self):
        return self.release_cycle_name+"                    FROM                           -"+str(self.start_date.date())+"-TO-"+str(self.end_date.date())

class RCForm(forms.ModelForm):
    class Meta:
        model = ReleaseCycle
        fields = '__all__'
    def clean(self):
        cleaned_data = self.cleaned_data

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if cleaned_data.get('release_cycle_name') == "RC-00":
            raise forms.ValidationError("\"RC-00\" is already used as default release cycle")
    
        

        if(ReleaseCycle.objects.filter(relid=self.instance.pk).first() is None):
            if start_date is not None and end_date is not None:
                startbetween = ReleaseCycle.objects.filter(start_date__lte=start_date, end_date__gte=start_date)
                endbetween = ReleaseCycle.objects.filter(start_date__lte=end_date, end_date__gte=end_date)

                overlap = ReleaseCycle.objects.filter(start_date__gte=start_date,end_date__lte=end_date)
            
                if startbetween or endbetween or overlap:
                    raise forms.ValidationError("Release cycle overlaps with other release cycle")
                
            try: 
                datetime.strptime(str(start_date.time()),"%H:%M:%S")
                datetime.strptime(str(end_date.time()),"%H:%M:%S")
            except:
                raise forms.ValidationError("Date format should be YYY-MM-DD and Time format should be HH:MM:SS")
                

        else:
            ob=ReleaseCycle.objects.filter(relid=self.instance.pk).first()
            ReleaseCycle.objects.filter(relid=self.instance.pk).delete()
            
            if start_date is not None and end_date is not None:
                startbetween = ReleaseCycle.objects.filter(start_date__lte=start_date, end_date__gte=start_date)
                endbetween = ReleaseCycle.objects.filter(start_date__lte=end_date, end_date__gte=end_date)

                overlap = ReleaseCycle.objects.filter(start_date__gte=start_date,end_date__lte=end_date)
            
                if startbetween or endbetween or overlap:
                    ob.save() 
                    raise forms.ValidationError("Release cycle overlaps with other release cycle")
                
            try: 
                datetime.strptime(str(start_date.time()),"%H:%M:%S")
                datetime.strptime(str(end_date.time()),"%H:%M:%S")
            except:
                ob.save()
                raise forms.ValidationError("Date format should be YYY-MM-DD and Time format should be HH:MM:SS")

        if(start_date > end_date):
            raise forms.ValidationError("Release Cycle start date should be preceeding the End Date")
        return cleaned_data

class Feature(models.Model):
    feature_label=models.CharField(unique=True,max_length=50,null=True,blank=False)
    feature_name=models.CharField(unique=True,max_length=50,null=True,blank=False)
    
    def __str__(self):
        return self.feature_label