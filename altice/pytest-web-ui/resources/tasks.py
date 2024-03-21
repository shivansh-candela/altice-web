from __future__ import absolute_import,unicode_literals
from asyncio import subprocess
from datetime import datetime
from encodings import utf_8
# from tkinter import E
import json
from celery import shared_task
import sys
from subprocess import run,PIPE
from .models import *
from django.shortcuts import render
from signal import pthread_kill
import subprocess
from subprocess import CalledProcessError, check_output
from subprocess import Popen,PIPE
from celery import current_task
import time
import os
from django.conf import settings
from .models import *
from collections import OrderedDict
# from celery import current_task
# print(current_task.request)
# print(current_task.request.id)z

try:
    f=open('sync.txt', 'r')
    sync_var=int(f.read())
    f.close()
    sync_var += 1
    f=open('sync.txt', 'w')
    f.write(str(sync_var))
    f.close()
    running_schedules = TestScheduler.objects.all()
    for i in running_schedules:
        # print(i.starttime)
        if(i.status=='Running'):
            if(Testbed.objects.get(testbedname=i.testbed).status==True):
                print("**********************************")
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
                TestScheduler.objects.filter(starttime=i.starttime).update(status='Aborted')
                print("==================================")
                TestScheduler.objects.filter(starttime=i.starttime).update(completed = True)
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
        if(i.status=='Pending'):
            s_starttime = i.starttime
            curr_time = datetime.now()
            curr_time = curr_time.isoformat()
            curr_time = curr_time[0:16]
            if(s_starttime < curr_time):
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
                TestScheduler.objects.filter(starttime=i.starttime).update(status='Aborted')
                TestScheduler.objects.filter(starttime=i.starttime).update(completed = True)
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()    
except Exception as e:
    print("new db sqlite3")

@shared_task
def run_schedule_task(outputfiletext,allure_generate_cmd,allure_dir,allure_generate_dir,starttime,name,marker,firmware_m,testbed,without_firmware,tester_name,testplan,outputfile_logs):
    base_directory=settings.BASE_DIR
    base_directory1=settings.BASE_DIR1
    schedule = TestScheduler.objects.get(starttime=starttime)
    testbed_details = Testbed.objects.get(testbedname=schedule.testbed)
    # print("Testbed Status",testbed_details.status)
    create_a_folder=base_directory+"/results/"+name
    rt_logs = base_directory+"/results/"+name+"/"+name+'_RTlogs.txt'
    try:
        os.makedirs(create_a_folder)
    # except FileExistsError:
    #     print("Folder already exists")
        global_logs_file=base_directory+"/results/global_logs.txt"
        if(testbed_details.status==True and testbed_details.availability==True):
            task_id=current_task.request.id   
            celery_task_id=TestScheduler.objects.filter(starttime=starttime).update(celery_task_id=task_id)
            testbed_details = Testbed.objects.filter(testbedname=schedule.testbed).update(status=False)
            status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Running")
            f=open('sync.txt', 'r')
            sync_var=int(f.read())
            f.close()
            sync_var += 1
            f=open('sync.txt', 'w')
            f.write(str(sync_var))
            f.close()
            # result = my_task.AsyncResult(task_id)
            # y = result.get()
            # print("//////////////////////////////////////////////////////////////////////////status",y)
            
            pytest_dir=base_directory1+"/wlan-testing/tests"
            collect_argument= "pytest -m" + " " + '\"'+ marker + '\"' + " "+"--collect-only  -q | tail -1 | cut  -d ' ' -f 1"
            # with open(outputfile_logs, "w") as output_file_testplan:
            #     output_file_testplan.write("Test Plan: " + testplan + "\nOn Testbed: " + testbed + "\nBy Tester: " + tester_name + "\nAt Time: " + str(starttime)+"\n=================================\n========Connectivity Logs========\n")
            try:
                sp12=Popen(collect_argument, cwd=pytest_dir,shell=True,stdin=PIPE, stdout=PIPE,stderr=PIPE) #path should be generic
                (out,err) = sp12.communicate()
                print("Collect only Ran Successfully on "+str(starttime)+" on Testbed:"+testbed)
                ret_code=sp12.returncode
                # with open(outputfile_logs, "a") as output_file_testplan:
                #     output_file_testplan.write("Collected the number of testcases="+str(out.decode('utf-8')))
            except:
                print("Except Statement for Collecting testcases") # remove this or add good
            # with open(collect_result, 'w') as outputf1:
            #     stt12=out.decode("utf-8")
            #     outputf1.write(stt12)
            #     print(stt12)
            collect_number=out.decode("utf-8")
            
            num_tests_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_testcases=collect_number)
            if collect_number!="no":

                status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Running")
                with open(global_logs_file, 'a') as global_logs:
                    global_logs.write("\nExecution started on testbed:"+testbed+"| Scheduled at:"+starttime+" | By Tester:"+tester_name+" | With testplan:"+testplan)
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
                
                try:
                    base_directory=settings.BASE_DIR
                    output_dir= base_directory + "/results/" + name+"/"
                    try:
                        print(without_firmware)
                        print(pytest_dir)
                        print("Pytest Going to Run")
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nPytest Ran Started")
                        with open(rt_logs,"ab") as out, open(rt_logs,"ab") as err:
                            sp=Popen(without_firmware, cwd=pytest_dir,shell=True,stdin=PIPE, stdout=out,stderr=err) #path should be generic
                            (out,err) = sp.communicate()
                        print("Pytest Ran Successfully on"+str(starttime)+" on Testbed:"+testbed)
                        ret_code=sp.returncode
                        if ret_code==0:
                            with open(outputfile_logs, "a") as output_file_testplan:
                                output_file_testplan.write("\nAll the testcases passed")   
                        else:
                            with open(outputfile_logs, "a") as output_file_testplan:
                                output_file_testplan.write("\nAll the testcases not passed")
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nPytest ran Successfully")
                    except:
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nPytest Didn't Executed")
                        print("Except Statement For Pytest Run Failure Without Firmware")
                    try:
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nOutput Log file Created For Pytest Run") 
                    except:
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nOutput Log file not Created For Pytest Run")
                        print("Except Statement For Writing Pytest Output")   
                    print("Allure Generate Command Initiated")
                    try:
                        with open(rt_logs,"ab") as out, open(rt_logs,"ab") as err:
                            sp1=Popen(allure_generate_cmd.split(" "), cwd=allure_dir, stdout=out,stderr=err)
                        print("Allure Generate Ran Successfully")
                        with open(outputfile_logs, "a") as output_file_testplan:
                            output_file_testplan.write("\nAllure Generated For Pytest Run")
                        # else:
                        #     with open(outputfile_logs, "a") as output_file_testplan:
                        #         output_file_testplan.write("\nIssue in Allure Generate For Pytest Run")
                    except:
                        print("Except Statement For Allure Generate")
                    # with open(outputfiletext, 'a') as outputerr:
                        # er=err.decode("utf_8")
                        # outputerr.write("Error Return Code for Pytest"+er)
                    
                    print("Return Code added in the output file for pytest on Testbed",testbed)
                    # print("Allure Generated")
                    x=datetime.now()
                    print("Test Completed at",x)
                    time.sleep(5)
                    sp2=subprocess.check_output(allure_generate_dir.split(" "))
                    time.sleep(5)
                    print("Task Completed for Testbed",testbed)
                    schedule = TestScheduler.objects.get(starttime=starttime)
                    print("At Starttime:",str(schedule))
                    status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Completed")
                    status_value=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
                    testbed_details = Testbed.objects.filter(testbedname=schedule.testbed).update(status=True)
                    print("Status Updated for Completed on Testbed",testbed+"At time:",str(starttime))
                    f=open('sync.txt','r')
                    sync_var=int(f.read())
                    f.close()
                    sync_var += 1
                    f=open('sync.txt','w')
                    f.write(str(sync_var))
                    f.close()
                    json_dir=base_directory+"/results/"+name+"/"+name+".json"
                    try:
                        with open(json_dir) as f:
                            data = json.load(f)

                            # print("//////////////////////////////////////data",data)
                            # for i in data['report']:
                            #     for j in data[]
                            try:
                                total_passed=data["report"]["summary"]["passed"]
                                print("Total Passed",total_passed)
                                pass_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_passed=total_passed)
                            except:            
                                total_passed=0
                                print("No Passed Testcases Found")
                        
                            try:
                                total_failed=data["report"]["summary"]["failed"]
                                print("Total Failed",total_failed)
                                fail_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_failed=total_failed)
                            except:                
                                total_failed=0
                                print("No Failed Testcases Found")

                            try:
                                total_xfailed=data["report"]["summary"]["xfailed"]
                            except:                
                                print("No xFailed Testcases Found")

                            try:
                                if total_xfailed>=1:
                                    total_failed=total_failed+total_xfailed
                                    fail_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_failed=total_failed)
                                else:
                                    print("No xFailed Testcases Found")
                            except:
                                print("No xFailed Testcases Found")

                            try:
                                num_tests=data["report"]["summary"]["num_tests"]
                                print("Total Tests",num_tests)
                            except:                
                                print("No Testcases Found")

                            try:
                                total_error=num_tests-total_passed-total_failed
                                error_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_error=total_error)
                            except:      
                                total_error=0          
                                print("No error Testcases Found")
                            try:
                                # total_duration=data["report"]["summary"]["duration"]
                                total_duration = round(sum([case['setup']['duration'] + case['call']['duration'] + case['teardown']['duration'] for case in data["report"]["tests"]]))
                                total_duration_update=TestScheduler.objects.filter(starttime=starttime).update(total_duration=total_duration)
                            except:
                                print("No duration Found")                                    
                            f.close()
                            with open(outputfile_logs, "a") as output_file_testplan:
                                output_file_testplan.write("\n==============Summary==============\n"+"Total Testcases: "+str(num_tests)+"\nTotal Passed: "+str(total_passed)+"\nTotal Failed: "+str(total_failed)+"\nTotal Error: "+str(total_error)+"\nTotal Duration: "+str(total_duration)+"\n===================================")
                            try:
                                try:
                                    alldata=list(TestScheduler.objects.values())
                                    # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",alldata)
                                    list3=dict()
                                    alldata2=[]
                                    with open(base_directory+'/'+'new_testplan.json','r') as f:
                                        list2=jsn.load(f)
                                        f.close()
                                    context2 = {
                                        'alldata':alldata2,
                                    }
                                    for testplan in alldata:
                                        # total_passed = 0
                                        # total_failed = 0
                                        # total_error = 0
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
                                            # t['status']=testplan['status']
                                            t['firmware_name']=testplan['firmware_name']
                                            t['release_cycle']=testplan['created_at']
                                            # t['celery_task_id']=testplan['celery_task_id']
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
                                            t['result']="-"
                                            # print(t)
                                            try:
                                                f=open(base_directory+'/results/'+t['name']+'/'+t['name']+'.json','r')
                                                f_data=jsn.load(f)
                                                f.close()                   
                                                for case in f_data["report"]["tests"]:
                                                    if(case['name']==t['test_case_name']):
                                                        t['duration']=round(case['setup']['duration'] + case['call']['duration'] + case['teardown']['duration'])
                                                        t['passed']=[1 if case['outcome']=='passed' else 0][0]
                                                        t['failed']=[1 if case['outcome']=='failed' or case['outcome']=='xfailed' else 0][0]
                                                        t['error']=[1 if case['outcome']=='error' else 0][0]
                                                        t['result']=case['outcome']
                                                        # if(t['passed']==1):
                                                        #     # print("tasks111111111111111111111111111111111111")
                                                        #     total_passed+=1
                                                        # elif(t['failed']==1):
                                                        #     # print("tasks222222222222222222222222222222222222")
                                                        #     total_failed+=1
                                                        # elif(t['error']==1):
                                                        #     # print("tasks333333333333333333333333333333333333")
                                                        #     total_error+=1
                                                        # if(case['outcome']=='passed'):
                                                        #     total_passed+=1
                                                        #     print("tasks1111111111111111111111111111")
                                                        # elif(case['outcome']=='failed' or case['outcome']=='xfailed'):
                                                        #     total_failed+=1
                                                        #     print("tasks2222222222222222222222222222")
                                                        # elif(case['outcome']=='error'):
                                                        #     total_error+=1
                                                        #     print("tasks3333333333333333333333333333")
                                                context2['alldata'].append(t)
                                            except:
                                                print("Reading json data error")
                                except:
                                    print("Reading File Error")                
                                try:
                                    list3.update(context2)
                                    with open('data_with_testcases.json','w') as f:
                                        jsn.dump(OrderedDict(list3), f, indent=4)
                                        f.close()
                                except:
                                    print("Except statement for data_with_testcases.json")
                            except:
                                print("Except statement for new_testplan.json")
                            # print(total_passed)
                            # print(total_failed)
                            # print(total_error)
                            # pass_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_passed=total_passed)
                            # fail_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_failed=total_failed)
                            # error_data_update=TestScheduler.objects.filter(starttime=starttime).update(total_error=total_error)
                            # status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Completed")
                            # status_update=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
                            # testbed_details = Testbed.objects.filter(testbedname=schedule.testbed).update(status=True)
                            f=open('sync.txt','r')
                            sync_var=int(f.read())
                            f.close()
                            sync_var += 1
                            f=open('sync.txt','w')
                            f.write(str(sync_var))
                            f.close()
                    except:
                        print("Error in Testcase level update from json")
                except:
                    print("Except statement to run connectivity testcases")
                    status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Aborted")
                    status_value=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
                    with open(global_logs_file, 'a') as global_logs:
                        global_logs.write("Aborting pytest on following"+"testbed: "+testbed+" at: "+starttime+" by tester: "+tester_name+" On testplan "+testplan+"due to test connectivity failure")
                    
                    with open(outputfile_logs, "a") as output_file_testplan:
                        output_file_testplan.write("\nTestbed is already reserved") 
                    f=open('sync.txt', 'r')
                    sync_var=int(f.read())
                    f.close()
                    sync_var += 1
                    f=open('sync.txt', 'w')
                    f.write(str(sync_var))
                    f.close()
            else:
                #Else statement for not getting slected any testcases from the testplan
                status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Aborted")
                status_value=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
                with open(global_logs_file, 'a') as global_logs:
                    global_logs.write("Aborting pytest following "+"testbed: "+testbed+" at: "+starttime+" by tester: "+tester_name+" On testplan "+testplan+"due to no testcases selected")
                
                with open(outputfile_logs, "a") as output_file_testplan:
                    output_file_testplan.write("\nNo testcases selected on testplan: "+testplan+"Aborting pytest")
                f=open('sync.txt', 'r')
                sync_var=int(f.read())
                f.close()
                sync_var += 1
                f=open('sync.txt', 'w')
                f.write(str(sync_var))
                f.close()
        else:
            status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Aborted")
            status_value=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
            if(testbed_details.status==False):
                with open(outputfile_logs, "a") as output_file_testplan:
                    output_file_testplan.write("\nTestbed is already reserved")
                    print("Testbed status false")
            else:
                with open(global_logs_file, 'a') as global_logs:
                    global_logs.write("Aborting pytest following "+"testbed: "+testbed+" is not available at: "+starttime+" by tester: "+tester_name+" On testplan "+testplan)
                    print("Testbed disabled by admin")
            f=open('sync.txt', 'r')
            sync_var=int(f.read())
            f.close()
            sync_var += 1
            f=open('sync.txt', 'w')
            f.write(str(sync_var))
            f.close()
            print("Ending up else statement after abort due to testbed issue")
    except FileExistsError:
        print("Folder already exists")
        status_update=TestScheduler.objects.filter(starttime=starttime).update(status="Aborted")
        status_value=TestScheduler.objects.filter(starttime=starttime).update(completed=True)
        with open(global_logs_file, 'a') as global_logs:
            global_logs.write("Aborting pytest following "+"testbed: "+testbed+" is not available at: "+starttime+" by tester: "+tester_name+" On testplan "+testplan)
        
        with open(outputfile_logs, "a") as output_file_testplan:
            output_file_testplan.write("\Same Testplan already ran before resulting conflict,aborting the schedule") 
        f=open('sync.txt', 'r')
        sync_var=int(f.read())
        f.close()
        sync_var += 1
        f=open('sync.txt', 'w')
        f.write(str(sync_var))
        f.close()
    # testbed_details = Testbed.objects.filter(testbedname=schedule.testbed).update(status=True)


# class CallPytestDir():

    
#     def call_python_command(self,outputfiletext):

#     	with open("/home/imgd/abcd/venv1/pytest-web-ui/runtest_task_string.txt", 'r') as out_file:
#             v=out_file.readline()
#             sp=subprocess.check_output(v.split(" "), cwd='/home/imgd/abcd/venv1/pytest/wlan-testing/wlan-testing/tests')
                
#             print("Schedule Ran Successfully")
#             #print("SSSSSSSSSSSSsssssssssssssssssssssss",sp)
#             # with open(n, 'r') as outs:
#             #     s=outs.readline()
#             #     #print("popopoppoopopopopopopopop",type(s),s)
#             with open(outputfiletext, 'w') as outputf:
#                 #print("pipipipipipipipipipi",sp)
#                 stt=sp.decode("utf-8")
#                 outputf.write(stt)
#                 print("Output File Created")
#                 print("Allure Generated")