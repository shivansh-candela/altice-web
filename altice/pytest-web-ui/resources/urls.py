
"""pytest_web_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path
from .import views

admin.site.site_header = 'Altice WebGUI Admin Panel'
admin.site.site_title = 'Altice WebGUI Admin Panel'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('statistics/', views.statistics,name='statistics'),
    path('', views.login, name='login'),
    # path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    # path('add_testbed/', views.add_testbed, name='add_testbed'),
    # path('select_testbed/', views.select_testbed, name='select_testbed'),
    # path('add_accesspoint/', views.add_accesspoint, name='add_accesspoint'),
    # path('add_lanforge/', views.add_lanforge, name='add_lanforge'),
    path('view_all/', views.view_all, name='view_all'),
    path('accesspoint_details/<int:pk>', views.accesspoint_details, name='accesspoint_details'),
    path('lanforge_details/<int:pk>', views.lanforge_details, name='lanforge_details'),
    path('testbed_details/<int:pk>', views.testbed_details, name='testbed_details'),
    path('json/', views.json,name='json'),
    #path('json', views.json,name='json'),
    #path('collect_only/',views.collect_only,name='collect_only'),
    #path('runtime_only/',views.runtime_only,name='runtime_only'),
    path('test_scheduler/',views.test_scheduler,name='test_scheduler'),
    path('show_all/',views.show_all,name='show_all'),
    path('sync_data/',views.sync_data,name='sync_data'),
    path('get_log/',views.get_log,name='get_log'),
    path('add_remarks/',views.add_remarks,name='add_remarks'),
    path('new_testplan/',views.new_testplan,name='new_testplan'),
    path('custom_plan/',views.custom_plan,name='custom_plan'),
    path('collect_only/',views.collect_only,name='collect_only'),
#    path('test_scheduler_info/',views.test_scheduler_info,name='test_scheduler_info'),
    # path('logfile_collect/',views.logfile_collect,name='logfile_collect'),
    # path('logfile_runtest/',views.logfile_runtest,name='logfile_runtest'),
    # path('schedule_task/',views.schedule_task,name='schedule_task'),
    # path('allure_run/',views.allure_run,name='allure_run'),
    # path('output_file/',views.output_file,name='output_file'),
    # path('delete_plan/',views.delete_plan,name='delete_plan'),
    path('delete_task/',views.delete_task,name='delete_task'),
    path('cancel_task/',views.cancel_task,name='cancel_task'),
    path('refresh_data/',views.refresh_data,name='refresh_data'),
    path('release_cycles/',views.release_cycles,name='release_cycles'),
    path('extra_charts/',views.extra_charts,name='extra_charts'),
]
