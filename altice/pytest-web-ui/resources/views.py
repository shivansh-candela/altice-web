from asyncio import subprocess
from cgitb import enable
from datetime import date, datetime
import email
from email.mime import base
from enum import unique
import imp
from math import fabs
from multiprocessing import context
from os import access
from django.shortcuts import render, HttpResponse
import random
from django.urls import conf
from .models import *
#from django.core.mail import send_mail .
#from .utils import *
from django.http import JsonResponse
import json as jsn
import asyncio
# for filexec
from subprocess import run, PIPE, Popen
# import requests
import sys
from resources.tasks import *
import datetime
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.conf import settings
from celery import current_task
from django.contrib import messages #import messages
from collections import OrderedDict
from celery import Celery
from celery.app.control import Control
from shutil import rmtree
app = Celery('pytest_web_ui')
task_control = Control(app=app)

# import swal from sweetalert
# filexece ends
# Create your views here.

accesspoint_all = AccessPoint.objects.all()
lanforge_all = TrafficGenerator.objects.all()
testbed_all = Testbed.objects.all()
testplan_all = Testplan.objects.all()
feature_all=Feature.objects.all()
testscheduler_all=TestScheduler.objects.all()
firmware_all=FirmwareImage.objects.all()
lock=False
def home(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            accesspoint_all = AccessPoint.objects.all()
            lanforge_all = TrafficGenerator.objects.all()
            testbed_all = Testbed.objects.all()
            testplan_all = Testplan.objects.all()
            return render(request, "resources/dashboard/index.html", {'tester_email_id': tester_email_id})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

def statistics(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            return render(request, "resources/dashboard/statistics.html", {'tester_email_id': tester_email_id})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})


def login(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            accesspoint_all = AccessPoint.objects.all()
            lanforge_all = TrafficGenerator.objects.all()
            testbed_all = Testbed.objects.filter(availability=True)
            testplan_all = Testplan.objects.all()
            return render(request, "resources/view_all.html", {'tester_email_id': tester_email_id, 'accesspoint_all': accesspoint_all, 'lanforge_all': lanforge_all, 'testbed_all': testbed_all, 'testplan_all': testplan_all})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        try:

            if request.POST:
                tester_email_id = Tester.objects.get(email=request.POST['email'])
                if(tester_email_id.status):
                    if tester_email_id.password == request.POST['password']:
                        request.session['email'] = tester_email_id.email
                        accesspoint_all = AccessPoint.objects.all()
                        lanforge_all = TrafficGenerator.objects.all()
                        testbed_all = Testbed.objects.filter(availability=True)
                        testplan_all = Testplan.objects.all()
                        return render(request, "resources/view_all.html", {'tester_email_id': tester_email_id, 'accesspoint_all': accesspoint_all, 'lanforge_all': lanforge_all, 'testbed_all': testbed_all, 'testplan_all': testplan_all})
                    else:
                        msg="Invalid Credentials"
                        return render(request, "resources/login.html",{'msg':msg})
                msg=tester_email_id.name + " is blocked by admin."
                try:
                    del request.session['email']
                except: 
                    pass
                return render(request, "resources/login.html",{'msg' :msg})
            return render(request, "resources/login.html")
        except:
            msg="Invalid Credentials"
            return render(request, "resources/login.html",{'msg':msg})


def collect_only(request):
     if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        base_directory=settings.BASE_DIR
        base_directory1=settings.BASE_DIR1
        if request.method == 'POST':
            testplan_string=request.POST['testplan_new']
            # print(testplan_string)

            #allure_dir=base_directory+"/results/"+testplan_name
            argument1 = "pytest -m" + " " + '\"'+ testplan_string + '\"' + " "+"--collect-only  -q | tail -1 | cut  -d ' ' -f 1"
            pytest_dir=base_directory1+"/wlan-testing/tests"
            # print("///////////////////////////////////",pytest_dir)
            # print("/////////////////////////////////",argument1)
            sp=Popen(argument1, cwd=pytest_dir,shell=True,stdin=PIPE, stdout=PIPE,stderr=PIPE)
            (out,err) = sp.communicate()
            stt=out.decode("utf-8")
            context = {
                'stt': stt,
            }
            #new_testplan=Testplan(testplan_name=testplan_name,testplan_marker=testplan_string)
            #new_testplan.save()
            return JsonResponse({'context':context})
# def register(request):
#     try:
#         if request.POST:
#             firstname = request.POST['firstname']
#             email = request.POST['email']
#             contact = request.POST['contact']
#             li = ["65","55","98","74","62","32","54"]
#             ch = random.choice(li)
#             password = firstname[1:]+contact[3:6]+email[3:6]+ch
#             print("--------------->password",password)

#             tester_email_id = User.objects.create(email=email,password=password)
#             eid = Employee.objects.create(user_id=tester_email_id,firstname=firstname,contact=contact)

#             subject = "Welcome to Candela Technologies"

#             sendmail(subject,'maintemplate',email,{'firstname':firstname,'password':password})
#             return render(request,"resources/login.html")
#         else:

#             return render(request,"resources/register.html")
#     except:
#         e_msg="Something Went Wrong"
#         return render(request,"resources/register.html",{'e_msg':e_msg})

def logout(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            del request.session['email']
            return render(request, "resources/login.html")
        else:
            del request.session['email']
            msg=tester_email_id.name + " is blocked by admin."
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})


def view_all(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            accesspoint_all = AccessPoint.objects.all()
            lanforge_all = TrafficGenerator.objects.all()
            testbed_all = Testbed.objects.filter(availability=True)
            testplan_all = Testplan.objects.all()
            return render(request, "resources/view_all.html", {'tester_email_id':tester_email_id,'accesspoint_all': accesspoint_all, 'lanforge_all': lanforge_all, 'testbed_all': testbed_all, 'testplan_all': testplan_all})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

def accesspoint_details(request, pk):
    accesspoint_id = AccessPoint.objects.get(id=pk)
    tester_email_id = Tester.objects.get(email=request.session['email'])
    return render(request, "resources/accesspoint_details.html", {'tester_email_id': tester_email_id, 'accesspoint_id': accesspoint_id, 'accesspoint_all': accesspoint_all})


def lanforge_details(request, pk):
    lanforge_id = TrafficGenerator.objects.get(id=pk)
    tester_email_id = Tester.objects.get(email=request.session['email'])
    return render(request, "resources/lanforge_details.html", {'tester_email_id': tester_email_id, 'lamforge_id': lanforge_id, 'lanforge_all': lanforge_all})


def testbed_details(request, pk):
    testbed_id = Testbed.objects.get(pk=pk)
    tester_email_id = Tester.objects.get(email=request.session['email'])
    return render(request, "resources/testbed_details.html", {'tester_email_id': tester_email_id, 'testbed_id': testbed_id})

def json(request):
    base_directory=settings.BASE_DIR
    with open(base_directory+'/'+'data_with_testcases.json', 'r+') as f:
        data = jsn.load(f)
        data = data['alldata']
        f.close()                                                                                                                                             
    return JsonResponse(data, safe=False)

def sync_data(request):
    if "email" in request.session:
        base_directory=settings.BASE_DIR
        global sync_var
        f=open(base_directory+'/'+'sync.txt','r')
        sync_var=int(f.read())
        f.close()
        context = {
            'sync_var': sync_var,
        }
        return JsonResponse({'context':context})


def test_scheduler(request):
    global sync_var
    list1=dict()
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            try:
                tester_email_id = Tester.objects.get(email=request.session['email'])
                tester_id=tester_email_id.id
                base_directory=settings.BASE_DIR
                data=Testbed.objects.all()
                accesspoint_all = AccessPoint.objects.all()
                testbed_all = Testbed.objects.all()
                testplan_all = Testplan.objects.all()
                testscheduler_all = TestScheduler.objects.all()
                firmware_all=FirmwareImage.objects.all()
                release_cycles=ReleaseCycle.objects.all()
                plans=dict()
                for i in testplan_all:
                    if(i.testplan_marker==None):
                        plans[i.testplan_name]=i.testplan_name
                        continue
                    plans[i.testplan_name]=i.testplan_marker
                    f=open(base_directory+"/new_testplan.json",'r')
                    data=jsn.load(f)
                    f.close()
                f = open(base_directory+'/'+'sync.txt', 'r')
                sync_var = int(f.read())
                f.close()
                # print(data)
                if request.method == 'POST':
                    celery_cmd = "celery -A pytest_web_ui status"
                    p=Popen(celery_cmd.split(),cwd=base_directory,stdin=PIPE,stdout=PIPE,stderr=PIPE)
                    polled=p.communicate()
                    if(p.returncode==0):
                        global lock
                        tester = Tester.objects.get(email=request.session['email']) 
                        task = "resources.tasks.run_schedule_task"
                        testplan = request.POST['testplan']
                        testbed = request.POST['testbed']
                        starttime = request.POST['starttime']
                        instance = Testplan.objects.get(testplan_name=testplan)
                        estimated_time = instance.Estimated_Time
                        tester_email_id = Tester.objects.get(email=request.session['email'])
                        firmware_m = request.POST['firmware_m'] # change variable name to something meaningful
                        id=str(tester.id)
                        name= id + "_" + testbed + "_" + starttime
                        testbed_obj=Testbed.objects.get(testbedname=testbed)
                        accesspoint=testbed_obj.accesspoint
                        accesspoint_mode=testbed_obj.accesspoint.mode
                        accesspoint_serial=testbed_obj.accesspoint.serial
                        trafficgenerator=testbed_obj.trafficgenerator
                        tester_name=tester.name
                        release_cycles = ReleaseCycle.objects.values()
                        allure_generate_cmd="allure generate "+name
                        if firmware_m=="":
                            firmware_m="Default"
                        else:
                            firmware_=firmware_m
                        allure_dir=base_directory+"/results/"+name # change path to generic ==done
                        alluredirstr = ("--alluredir=../../pytest-web-ui/results/")
                        combine_py_dir="python3 "+base_directory+"/scripts/combine.py "
                        allure_generate_dir=combine_py_dir+allure_dir+"/allure-report" # change patch to generic or move it to script
                        # if firmware_m=="":
                        #     argument = "pytest -m" + " " + '\"'+ plans[testplan] + '\"' + " "+"--testbed=" + ""+testbed + " "+alluredirstr+""+name+"/"+name + " -rfEsxXp --verbose --capture=no  --junitxml=../../../results/"+name+"/"+name+".xml --json=../../../results/"+name+"/"+name+".json --html=../../../results/"+name+"/"+name+".html"+" --skip-pcap"
                        #     marker =plans[testplan]
                        # else:
                        teststring1=plans[testplan]
                        # argument = "pytest -m" + " " + '\"'+ teststring1 + '\"' + " "+"--testbed=" + ""+testbed + " "+alluredirstr+""+name+"/"+name + " -o firmware="+ '\"'+ firmware_m+ '\"'+ " -rfEsxXp --verbose --capture=no  --junitxml=../../../results/"+name+"/"+name+".xml --json=../../../results/"+name+"/"+name+".json --html=../../../results/"+name+"/"+name+".html"+" --skip-pcap"
                        without_firmware = "pytest -m" + " " + '\"'+ teststring1 + '\"' + " "+"--testbed=" + ""+testbed + " "+alluredirstr+""+name+"/"+name + " -rfEsxXp --verbose --capture=no  --junitxml=../../pytest-web-ui/results/"+name+"/"+name+".xml --json=../../pytest-web-ui/results/"+name+"/"+name+".json --html=../../pytest-web-ui/results/"+name+"/"+name+".html"+" --skip-pcap --al.1"
                        marker=teststring1
                        # print("////////////////////aaaaaaaaaaaaaaaaaaa",marker)
                        outputfiletext=base_directory+"/results/"+name+"/"+name+".txt" # change patch to generic
                        outputfile_logs=base_directory+"/results/"+name+"/"+name+"_logs.txt"

                        for e in ReleaseCycle.objects.filter(start_date__lte=starttime,end_date__gte=starttime):
                            # status_active=True
                            # print("////////////////////aaaaaaaaaaaaaaaaaaa",e)

                            # f=ReleaseCycle.objects.get(release_cycle_name=e)
                            # print("////////////////////aaaaaaaaaaaaaaaaaaa",f)
                            # print(type(release_cycles),"-=-=-==-=-=-=-=-=-=-=-=-=-=")
                            # print("starrrrrrrrrrrrrrrrrrrr",e)
                            created_at=e.release_cycle_name
                            # print("================================",created_at)
                            
                            schedule, created = ClockedSchedule.objects.get_or_create(
                                clocked_time=starttime)
                            periodic_task = PeriodicTask.objects.create(
                                clocked=schedule, name=name, task=task, one_off=True, args=jsn.dumps([outputfiletext,allure_generate_cmd,allure_dir,allure_generate_dir,starttime,name,marker,firmware_m,testbed,without_firmware,tester_name,testplan,outputfile_logs]))  # , args = json.dumps([[2,3]]))
                            test_scheduler = TestScheduler(tester=tester,tester_name=tester_name, name=name, task=task, testplan=testplan,
                                                        testbed=testbed, starttime=starttime,estimated_time=estimated_time,firmware_name=firmware_m,accesspoint=accesspoint,accesspoint_mode=accesspoint_mode,accesspoint_serial=accesspoint_serial,trafficgenerator=trafficgenerator,created_at=created_at)
                            test_scheduler.save()
                            sync_var += 1
                            while(not lock):
                                lock = True
                                f = open(base_directory+'/'+'sync.txt', 'w')
                                f.write(str(sync_var))
                                f.close()
                            lock = False
                            data=TestScheduler.objects.values()
                            alldata = list(data)
                            # print("---------------------",alldata)
                            msg="successfully saved"
                            context = {
                                'alldata':alldata,
                            }
                            list1=dict()
                            list1.update(context)
                            base_directory=settings.BASE_DIR
                            config_file_dir=base_directory+"/data.json"
                            # print("---------------========================",config_file_dir)
                            with open(config_file_dir, 'w') as f:
                                jsn.dump(list1, f, indent=4)
                                f.close()
                            messages.success(request, 'Test Schedule Created Successfully')
                            return JsonResponse({'context':context})
                            
                        else:
                            created_at="RC-00"
                            # print("================================",created_at)
                            
                            schedule, created = ClockedSchedule.objects.get_or_create(
                                clocked_time=starttime)
                            periodic_task = PeriodicTask.objects.create(
                                clocked=schedule, name=name, task=task, one_off=True, args=jsn.dumps([outputfiletext,allure_generate_cmd,allure_dir,allure_generate_dir,starttime,name,marker,firmware_m,testbed,without_firmware,tester_name,testplan,outputfile_logs]))  # , args = json.dumps([[2,3]]))
                            test_scheduler = TestScheduler(tester=tester,tester_name=tester_name, name=name, task=task, testplan=testplan,
                                                        testbed=testbed, starttime=starttime,estimated_time=estimated_time,firmware_name=firmware_m,accesspoint=accesspoint,accesspoint_mode=accesspoint_mode,accesspoint_serial=accesspoint_serial,trafficgenerator=trafficgenerator,created_at=created_at)
                            test_scheduler.save()
                            sync_var += 1
                            f = open(base_directory+'/'+'sync.txt', 'w')
                            f.write(str(sync_var))
                            f.close()
                            data=TestScheduler.objects.values()
                            alldata = list(data)
                            # print("---------------------",alldata)
                            msg="successfully saved"
                            context = {
                                'alldata':alldata,
                            }
                            list1=dict()
                            list1.update(context)
                            base_directory=settings.BASE_DIR
                            config_file_dir=base_directory+"/data.json"
                            # print("---------------========================",config_file_dir)
                            with open(config_file_dir, 'w') as f:
                                jsn.dump(list1, f, indent=4)
                                f.close()
                            messages.error(request, 'Test Schedule Created out of Release Cycle')
                            return JsonResponse({'context':context})
                    else:
                        data=TestScheduler.objects.values()
                        alldata = list(data)
                        # print("---------------------",alldata)
                        msg="successfully saved"
                        context = {
                            'alldata':alldata,
                        }
                        messages.error(request,'Scheduler is not running. Please start the scheduler to schedule tests.')
                        return JsonResponse({'context':context})    
                return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'tester_id':tester_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'release_cycles':release_cycles,'sync_var':sync_var})
            except:
                data=TestScheduler.objects.values()
                alldata = list(data)
                # print("---------------------",alldata)
                msg="successfully saved"
                context = {
                    'alldata':alldata,
                }
                msg="Test Already Scheduled at the same time"
                # messages.success(request, 'Test Already Scheduled at the same time')
                return JsonResponse({'context':context})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, 'resources/login.html',{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

        # print("MMMMMMMMMMMMMMMMMMMMMMMMMmmmmmmmmmmmmmmmm",msg)
    # return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'tester_id':tester_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'release_cycles':release_cycles,'msg':msg})

def show_all(request):
    if request.method == 'GET':
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            release_cycles = ReleaseCycle.objects.values()
            testscheduler_all = TestScheduler.objects.all()
            #print(userinfo)
            return render(request, 'resources/show_all.html', {'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'release_cycles':release_cycles})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})               
    elif request.method == 'POST':
        return HttpResponse('POST test_scheduler.html')

def add_remarks(request):
    global sync_var
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            tester_id=tester_email_id.id
            base_directory=settings.BASE_DIR
            data=Testbed.objects.all()
            accesspoint_all = AccessPoint.objects.all()
            testbed_all = Testbed.objects.all()
            testplan_all = Testplan.objects.all()
            testscheduler_all = TestScheduler.objects.all()
            firmware_all=FirmwareImage.objects.all()
            release_cycles=ReleaseCycle.objects.all()
            f=open(base_directory+'/'+'sync.txt','r')
            sync_var=int(f.read())
            f.close()
            if request.method == 'POST':
                remarks = request.POST['remarks']
                id = request.POST['starttime']
                evaluator = request.POST['name']
                # print(id)
                # print(remarks)
                # print(evaluator)
                updating = TestScheduler.objects.filter(starttime=id).update(remarks=remarks,evaluator=evaluator)
                sync_var += 1
                f = open(base_directory+'/'+'sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
                #updating.save()
                messages.success(request, 'Remarks Added Successfully')
                return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'tester_id':tester_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'release_cycles':release_cycles})
            return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'tester_id':tester_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'release_cycles':release_cycles})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            # del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

def release_cycles(request):
    if request.method == 'GET':
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            release_cycles = ReleaseCycle.objects.values()
            releasecycle = request.GET.get('cycle')
            testscheduler_all = TestScheduler.objects.filter(created_at=releasecycle)
            #print(userinfo)
            return render(request, 'resources/release_cycles.html', {'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all,'releasecycle':releasecycle,'release_cycles':release_cycles})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg})               
    elif request.method == 'POST':
        return HttpResponse('POST test_scheduler.html')



        
    # data=ReleaseCycle.objects.all()
    # print('123456789012345678901234567890',data)
    # for V in ReleaseCycle.objects.filter():
    #     V.release_cycle_name

    
    # return render(request, 'resources/first.html', {'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all})

def refresh_data(request):
    list1=dict()
    data=TestScheduler.objects.values()
    alldata = list(data)
    # alldata2 = list(data2)
    # print(alldata)
    context = {
        'alldata':alldata,
    }
    list1.update(context)
    base_directory=settings.BASE_DIR
    
    config_file_dir=base_directory+"/data.json"
    with open(config_file_dir, 'w') as f:
        jsn.dump(list1, f, indent=4)
        f.close()
    list3=dict()
    alldata2=[]
    with open(base_directory+'/'+'new_testplan.json','r') as f:
        list2=jsn.load(f)
        f.close()
    context2 = {
        'alldata':alldata2,
    }
    for testplan in alldata:
        total_duration = 0
        for testcase in list2[testplan['testplan']]:
            t={}            
            t['id']=testplan['id']
            t['tester_id']=testplan['tester_id']
            t['tester_name']=testplan['tester_name']
            t['name']=testplan['name']
            t['task']=testplan['task']
            t['testplan']=testplan['testplan']
            t['accesspoint']=testplan['accesspoint']
            t['accesspoint_mode']=testplan['accesspoint_mode']
            t['accesspoint_serial']=testplan['accesspoint_serial']
            t['trafficgenerator']=testplan['trafficgenerator']
            t['testbed']=testplan['testbed']
            t['starttime']=testplan['starttime']
            #t['status']=testplan['status']
            t['firmware_name']=testplan['firmware_name']
            t['release_cycle']=testplan['created_at']
            t['test_case']=testcase
            t['feature']=list2[testplan['testplan']][testcase]['feature']
            t['band']=list2[testplan['testplan']][testcase]['band']
            t['security']=list2[testplan['testplan']][testcase]['security']
            t['channel']=list2[testplan['testplan']][testcase]['channel']
            t['bandwidth']=list2[testplan['testplan']][testcase]['bandwidth']
            t['protocol']=list2[testplan['testplan']][testcase]['protocol']
            t['sub_feature']=list2[testplan['testplan']][testcase]['sub_feature']
            t['test_case_name']=list2[testplan['testplan']][testcase]['name']
            t['duration']=0
            t['passed']=0
            t['failed']=0
            t['error']=0
            testscheduler=TestScheduler.objects.get(starttime=testplan['starttime'])
            if(testscheduler.status=='Pending'):
                t['result']='Pending'
                t['status']='Pending'
            elif(testscheduler.status=='Running'):
                t['result']='In Progress'
                t['status']='Running'
            elif(testscheduler.status=='Aborted'):
                t['result']='Aborted'
                t['status']='Aborted'
            elif(testscheduler.status=='Completed'):
                t['status']='Completed'
            elif(testscheduler.status=='Cancelling' or testscheduler.status=='Cancelled'):
                t['result']='Cancelled'
            try:
                f=open(base_directory+'/results/'+t['name']+'/'+t['name']+'.json','r')
                f_data=jsn.load(f)
                f.close()
                for case in f_data["report"]["tests"]:
                    if(case['name']==t['test_case_name']):
                        t['duration']=round(case['setup']['duration'] + case['call']['duration'] + case['teardown']['duration'])
                        total_duration+=t['duration']
                        t['passed']=[1 if case['outcome']=='passed' else 0][0]
                        t['failed']=[1 if case['outcome']=='failed' or case['outcome']=='xfailed' else 0][0]
                        t['error']=[1 if case['outcome']=='error' else 0][0]
                        t['result']=case['outcome']
                        # t['outcome']=case['outcome']
                        # if(case['outcome']=='passed'):
                        #     total_passed+=1
                        #     # print("views11111111111111111111111")
                        # elif(case['outcome']=='failed' or case['outcome']=='xfailed'):
                        #     total_failed+=1
                        #     # print("views2222222222222222222222")
                        # elif(case['outcome']=='error'):
                        #     # print("views3333333333333333333333")
                        #     total_error+=1
            except:
                pass
            context2['alldata'].append(t)
        try:
            total_duration_update=TestScheduler.objects.filter(starttime=t['starttime']).update(total_duration=total_duration)
        except:
            pass
    list3.update(context2)
    list1 = dict()
    data=TestScheduler.objects.values()
    alldata = list(data)
    # alldata2 = list(data2)
    # print(alldata)
    context = {
        'alldata':alldata,
    }
    list1.update(context)
    config_file_dir=base_directory+"/data.json"
    with open(config_file_dir, 'w') as f:
        jsn.dump(list1, f, indent=4)
        f.close()
    base_directory=settings.BASE_DIR
    with open(base_directory+'/'+'data_with_testcases.json','w') as f:
        jsn.dump(OrderedDict(list3), f, indent=4)
        f.close()
    return JsonResponse({'context':context,'final_data':list3})
def get_log(request):
    if "email" in request.session:
        base_directory=settings.BASE_DIR
        log_name = request.GET['starttime']
        try:
            schedule = TestScheduler.objects.filter(starttime=log_name)
            schedule = list(schedule)[0]
            tester = schedule.tester
            testbed = schedule.testbed
            name = str(tester.id) + '_' + testbed + '_' + log_name
            f=open(base_directory+"/results/"+name+"/" + name + '_RTlogs.txt','r')
            log_data=f.read()
            f.close()
        except:
            log_data=" "
        return JsonResponse({'logs': log_data})
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})   

def new_testplan(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            testplan_data=Testplan.objects.all()
            base_directory=settings.BASE_DIR
            f=open(base_directory+'/'+"testplans.json",'r')
            data=jsn.load(f)
            f.close()
            return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg}) 
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

def custom_plan(request):
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            testplan_all=Testplan.objects.all()
            feature_all=Feature.objects.all()
            testplan_data=Testplan.objects.all()
            base_directory=settings.BASE_DIR
            f=open(base_directory+'/'+'testplans.json','r')
            data=jsn.load(f)
            f.close()
            # firmware_all=Firmware.objects.all()
            base_directory=settings.BASE_DIR
            if request.method == 'POST':
                try:
                    # body_data = reuqest.
                    testplan_name=request.POST['new_testplan']
                    testplan_string=request.POST['testplan_new']
                    new_testplan_string = request.POST['testplan_new1']
                    accordian_string = request.POST['testplan_new1']
                    accordian_string = accordian_string.split(' or ')
                    accordian_string = "\n".join(accordian_string)
                    accordian_string1 = accordian_string.replace("(","")
                    accordian_string2 = accordian_string1.replace(")","")



                    features=[]
                    band=[]
                    security=[]
                    channels=[]
                    bandwidth=[]
                    protocol=[]
                    sub_features=[]
                    description=[]
                    final_super_string = new_testplan_string.split(' or ')
                    total_estimated_time = 0
                    all_e_time=[]
                    test_cases={
                        testplan_name: {

                        }
                    }
                    for i in range(len(final_super_string)):
                        temporary=final_super_string[i].replace('\xa0', ' ')
                        # feature_1,mode_1,security_1,band_1=temporary.strip('(').strip(')').split(' and ')
                        temporary1 = temporary.strip('(').strip(')').split(' and ')
                        # print(temporary1)
                        if(len(temporary1)==4):
                            feature_1=temporary1[0]
                            mode_1=temporary1[1]
                            security_1=temporary1[2]
                            band_1=temporary1[3]
                            if(band_1=='twog'):
                                band_1='2G'
                            if(band_1=='fiveg'):
                                band_1='5G'
                            test_cases[testplan_name].update(
                                {
                                    temporary : {
                                        'status':'',
                                        'running time':0,
                                        'feature':feature_1,
                                        'mode':mode_1,
                                        'security':security_1,
                                        'band':band_1,
                                        'name': data['Testplan']['Features'][feature_1]['Mode'][mode_1]["security"][security_1]["band"][band_1]['name']
                                    }
                                }
                            )
                            total_estimated_time += data['Testplan']['Features'][feature_1]['Mode'][mode_1]["security"][security_1]["band"][band_1]['estimated time']
                            all_e_time.append(str(data['Testplan']['Features'][feature_1]['Mode'][mode_1]["security"][security_1]["band"][band_1]['estimated time']))
                        else:
                            # feature_1=temporary1[0]
                            # mode_1=temporary1[1]
                            # security_1=temporary1[2]
                            # band_1=temporary1[3]
                            # marker=temporary1[4]
                            feature_1,band_1,security_1,channel_1,bandwidth_1,protocol_1,sub_feature_1 = temporary1[0],temporary1[1],temporary1[2],temporary1[3],temporary1[4],temporary1[5],temporary1[6]
                            if(band_1=='twog'):
                                band_1='2G'
                            if(band_1=='fiveg'):
                                band_1='5G'
                            # print(temporary)
                            # temp_2 = temporary.replace(' and '+marker,'')
                            test_cases[testplan_name].update(
                                {
                                    temporary : {
                                        'status':'',
                                        'running time':0,
                                        'feature':feature_1,
                                        'band':band_1,
                                        'security':security_1,
                                        'channel':channel_1,
                                        'bandwidth':bandwidth_1,
                                        'protocol':protocol_1,
                                        'sub_feature':sub_feature_1,
                                        'name': data['Testplan']['Features'][temporary1[0]]['band'][temporary1[1]]['security'][temporary1[2]]['channels'][temporary1[3]]['bandwidth'][temporary1[4]]['protocol'][temporary1[5]]['sub_features'][temporary1[6]]['name']
                                    }
                                }
                            )
                            total_estimated_time += data['Testplan']['Features'][temporary1[0]]['band'][temporary1[1]]['security'][temporary1[2]]['channels'][temporary1[3]]['bandwidth'][temporary1[4]]['protocol'][temporary1[5]]['sub_features'][temporary1[6]]['estimated time']
                            all_e_time.append(str(data['Testplan']['Features'][temporary1[0]]['band'][temporary1[1]]['security'][temporary1[2]]['channels'][temporary1[3]]['bandwidth'][temporary1[4]]['protocol'][temporary1[5]]['sub_features'][temporary1[6]]['estimated time']))
                    for j in range(len(final_super_string)):
                        i=final_super_string[j]
                        i=i.strip('(')
                        i=i.strip(')')
                        i=i.split('\xa0and\xa0')
                        features.append(i[0].replace('_',' ').title())
                        if(i[1]=='twog'):
                            temp='2G'
                            band.append('2G')
                        elif(i[1]=='fiveg'):
                            temp='5G'
                            band.append('5G')
                        else:
                            temp=i[1]
                            band.append(i[1])
                        security.append(i[2].replace('_',' ').title())
                        channels.append(i[3].replace('_',' ').title())
                        if(i[4]=='twentyMhz'):
                            bandwidth.append('20MHz')
                        elif(i[4]=='fourtyMhz'):
                            bandwidth.append('40MHz')
                        elif(i[4]=='eightyMhz'):
                            bandwidth.append('80MHz')
                        # bandwidth.append(i[4])
                        protocol.append(i[5].upper())
                        sub_features.append(i[6].replace('_',' ').upper())
                        if(len(i)==4):
                            t=data['Testplan']['Features'][i[0]]['Mode'][i[1]]['security'][i[2]]['band'][temp]['testcase name'].replace('&nbsp;', ' ')
                        else:
                            t=data['Testplan']['Features'][i[0]]['band'][i[1]]['security'][i[2]]['channels'][i[3]]['bandwidth'][i[4]]['protocol'][i[5]]['sub_features'][i[6]]['testcase name'].replace('&nbsp;', ' ')
                            final_super_string[j]='\xa0and\xa0'.join(temporary1)
                        description.append(t)
                    context = {
                        'testplans' : {
                            'features':features,
                            'band':band,
                            'security':security,
                            'channels':channels,
                            'bandwidth':bandwidth,
                            'protocol':protocol,
                            'sub_feature':sub_features
                        }
                    }
                    unique_features=','.join(list(set(features)))
                    unique_band=','.join(list(set(band)))
                    unique_security=','.join(list(set(security)))
                    unique_channels=','.join(list(set(channels)))
                    unique_bandwidth=','.join(list(set(bandwidth)))
                    unique_protocol=','.join(list(set(protocol)))
                    unique_subfeature=','.join(list(set(sub_features)))
                    features='\n'.join(features)
                    band='\n'.join(band)
                    security='\n'.join(security)
                    channels='\n'.join(channels)
                    bandwidth='\n'.join(bandwidth)
                    protocol='\n'.join(protocol)
                    sub_features='\n'.join(sub_features)
                    description='\n'.join(description)
                    all_e_time='\n'.join(all_e_time)
                    allure_dir=base_directory+"/results/"+testplan_name
                    final_super_string = '\n'.join(final_super_string)
                    testplan_string=' '.join(testplan_string.split('\xa0'))
                    #collect_argument= "pytest -m" + " " + '\"'+ testplan_string + '\"' + " "+"--collect-only  -q | tail -1 | cut  -d ' ' -f 1"
                    # print("ssssssssssssssssssssssSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",collect_argument)
                    #pytest_dir=base_directory+"/pytest/wlan-testing/tests"
                    #sp=Popen(collect_argument, cwd=pytest_dir,shell=True,stdin=PIPE, stdout=PIPE,stderr=PIPE)
                    #(out,err) = sp.communicate()
                    #stt=out.decode("utf-8")
                    #print(stt)
                    testplan_string1=testplan_string
                    # testplan_string1="(uc_firmware) or (" + testplan_string + ")"
                    
                    print("------------------------------")
                    new_testplan=Testplan(testplan_name=testplan_name,testplan_marker=testplan_string1,tester_id=tester_email_id,features=features,band=band,security=security,channels=channels,bandwidth=bandwidth,protocol=protocol,sub_feature=sub_features,time=all_e_time,unique_features=unique_features,unique_band=unique_band,unique_security=unique_security,unique_channels=unique_channels,unique_bandwidth=unique_bandwidth,unique_protocol=unique_protocol,testcases=accordian_string2,description=description,Total_Testcases=len(final_super_string.split('\n')),Estimated_Time=total_estimated_time,data=context)
                    new_testplan.save()
                    base_directory=settings.BASE_DIR
                    f=open(base_directory+'/'+'new_testplan.json','r+')
                    available_testcases=jsn.load(f)
                    available_testcases.update(test_cases)
                    f.seek(0)
                    jsn.dump(available_testcases,f,indent=4)
                    f.close()
                    testplan_all=Testplan.objects.all()
                    messages.success(request, 'New Testplan Addded Successfully')
                    #return JsonResponse({'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
                    return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
                except:
                    try:
                        na = Testplan.objects.get(testplan_marker = testplan_string1).testplan_name
                        msg="Testplan With Same Identity Exists"
                        messages.error(request, 'Testplan With Same Testcases Already Exists As - {}'.format(na) )                    
                        return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'msg':msg,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
                    except:
                        msg="Testplan With Same Name Already Exists"
                        messages.error(request, 'Testplan With Same Name Already Exists ' )                    
                        return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'msg':msg,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
            # except:
            #     messages.error(request, 'Testplan With Same Identity Already Exists')
            #     msg="Testplan With Same Identity Exists"
            #     return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'msg':msg,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg}) 
        return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})

    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})

# def delete_plan(request):
#     if "email" in request.session:
#         tester_email_id = Tester.objects.get(email=request.session['email'])
#         testplan_all=Testplan.objects.all()
#         testplan_data=Testplan.objects.all()
#         base_directory=settings.BASE_DIR
#         f=open(base_directory+"/testplans.json",'r')
#         data=jsn.load(f)
#         f.close()
#         if request.method == "POST":
#             try:
#                 testplan_name=request.POST['testplan_delete']
#                 testplan_all=Testplan.objects.all()
#                 testplan_all.filter(testplan_name=testplan_name).delete()
#                 messages.success(request, 'Testplan Deleted Successfully')
#                 return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
#             except:
#                 messages.success(request, 'Testplan Not Found')
#                 return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
#         else:
#             return render(request, 'resources/new_testplan.html',{'tester_email_id':tester_email_id,'feature_all':feature_all,'testplan_marker':testplan_all,'testplan_data':testplan_data,'mydata':jsn.dumps(data)})
#     else:
#         msg="Please Login Again to Continue"
#         return render(request, 'resources/login.html',{'msg':msg})
# base_directory=settings.BASE_DIR

def cancel_task(request):
    testbed_all = Testbed.objects.all()
    testplan_all = Testplan.objects.all()
    testscheduler_all=TestScheduler.objects.all()
    firmware_all=FirmwareImage.objects.all()
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            if request.method == 'POST':
                sid = request.POST['sid']
                tester_email_id = Tester.objects.get(email=request.session['email'])
                clock=ClockedSchedule.objects.get(clocked_time=sid)
                test_scheduler=TestScheduler.objects.get(starttime=sid)
                status = test_scheduler.status
                id = str(tester_email_id.id)
                test_scheduler=TestScheduler.objects.get(starttime=sid)
                result_name = id + '_' + test_scheduler.testbed + '_' + test_scheduler.starttime
                if status == "Running":
                    clock.delete()
                    print("Deleted the schedule from the clock")
                    TestScheduler.objects.filter(starttime=sid).update(status="Cancelling")
                    task_id = test_scheduler.celery_task_id
                    task_control.revoke(task_id=task_id,terminate=True)
                    print("Revoked the cancelled task worker")
                    f=open('sync.txt','r')
                    sync_var=int(f.read())
                    f.close()
                    sync_var += 1
                    f=open('sync.txt','w')
                    f.write(str(sync_var))
                    f.close()
                    time.sleep(30)
                    TestScheduler.objects.filter(starttime=sid).update(status="Cancelled")
                    TestScheduler.objects.filter(starttime=sid).update(completed=True)
                    print("Updated the Scheduler status to Cancelled")
                    testbed_update=Testbed.objects.filter(testbedname=test_scheduler.testbed).update(status=True)
                    print("Updated testbed status to available")
                    f=open('sync.txt','r')
                    sync_var=int(f.read())
                    f.close()
                    sync_var += 1
                    f=open('sync.txt','w')
                    f.write(str(sync_var))
                    f.close()
                elif status == "Pending":
                    clock.delete()
                    TestScheduler.objects.filter(starttime=sid).update(status="Cancelled")
                    TestScheduler.objects.filter(starttime=sid).update(completed=True)
                    print("Testbed Status Updated")
                    f=open('sync.txt','r')
                    sync_var=int(f.read())
                    f.close()
                    sync_var += 1
                    f=open('sync.txt','w')
                    f.write(str(sync_var))
                    f.close()
                else:
                    print("Task already executed")
                base_directory=settings.BASE_DIR
                try:
                    rmtree(base_directory + '/results/' + result_name)
                    print('Result folder removed successfully')
                except:
                    print('Cannot remove result folder')
                list1=dict()
                data=TestScheduler.objects.values()
                alldata = list(data)
                context = {
                    'alldata':alldata,
                }
                list1.update(context)
                config_file_dir=base_directory+"/data.json"
                with open(config_file_dir, 'w') as f:
                    jsn.dump(list1, f, indent=4)
                    f.close()  
                return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all})    
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg}) 

def delete_task(request):
    
    global sync_var
    global base_directory
    testbed_all = Testbed.objects.all()
    testplan_all = Testplan.objects.all()
    testscheduler_all=TestScheduler.objects.all()
    firmware_all=FirmwareImage.objects.all()
    f=open(base_directory+'/'+'sync.txt','r')
    sync_var=int(f.read())
    f.close()
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email = request.session['email'])
        if(tester_email_id.status):
            if request.method == 'POST':
                sid = request.POST['sid']
                tester_email_id = Tester.objects.get(email=request.session['email'])
                id = str(tester_email_id.id)
                test_scheduler=TestScheduler.objects.get(starttime=sid)
                result_name = id + '_' + test_scheduler.testbed + '_' + test_scheduler.starttime
                print(test_scheduler)
                print(test_scheduler.status,"STATUS")
                if test_scheduler.status=="Running":
                    clock=ClockedSchedule.objects.get(clocked_time=sid)
                    clock.delete()
                    print("Removing the schedule from the clock")
                    testbed_update=Testbed.objects.filter(testbedname=test_scheduler.testbed).update(status=True)
                    print("Made the testbed status as active")
                else:
                    print("Deleting Tescheduler without updating testbed status")
                task_id = test_scheduler.celery_task_id
                task_control.revoke(task_id=task_id,terminate=True)
                print("Revoked the deleted worker task")
                test_scheduler.delete()
                try:
                    rmtree(base_directory + '/results/' + result_name)
                    print('Result folder removed successfully')
                except:
                    print('Cannot remove result folder')
                sync_var += 1
                f=open(base_directory+'/'+'sync.txt','w')
                f.write(str(sync_var))
                f.close()
                data=TestScheduler.objects.values()
                list1=dict()
                data=TestScheduler.objects.values()
                alldata = list(data)
                context = {
                    'alldata':alldata,
                }
                list1.update(context)
                base_directory=settings.BASE_DIR
                config_file_dir=base_directory+"/data.json"
                with open(config_file_dir, 'w') as f:
                    jsn.dump(list1, f, indent=4)
                    f.close()
                # messages.error(request, 'Test Schedule Deleted')
                
                return JsonResponse({'context':context})
                
            return render(request, 'resources/test_scheduler.html', {'tester_email_id':tester_email_id,'testbed_all': testbed_all, 'testplan_all': testplan_all, 'testscheduler_all': testscheduler_all,'firmware_all':firmware_all})
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg}) 
    else:
        msg="Please Login Again to Continue"
        return render(request, 'resources/login.html',{'msg':msg})
def extra_charts(request):
    base_directory=settings.BASE_DIR
    if "email" in request.session:
        tester_email_id = Tester.objects.get(email=request.session['email'])
        if(tester_email_id.status):
            if(request.method == "GET"):
                testerObj = Tester.objects.get(email=request.session['email'])
                jsondata=testerObj.chart                                                                                                                                        
                return JsonResponse(jsondata, safe=False)
            elif(request.method == "POST"):
                testerObj = Tester.objects.get(email=request.session['email'])
                data = request.body.decode('utf-8')
                data= jsn.loads(data)
                testerObj.chart=data
                testerObj.save()
                    
                return JsonResponse(data)
        else:
            msg=tester_email_id.name + " is blocked by admin."
            del request.session['email']
            return render(request, "resources/login.html",{'msg' :msg}) 
sync_var = 0
base_directory=settings.BASE_DIR
s=base_directory+'/'+'sync.txt'
f = open(s, 'w')
f.write(str(0))
f.close()
