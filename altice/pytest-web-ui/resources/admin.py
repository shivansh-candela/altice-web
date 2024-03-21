from django.contrib import admin
from .models import *
from django import forms

class ReleaseCycleAdmin(admin.ModelAdmin):
    form = RCForm
    list_display = ('release_cycle_name', 'start_date', 'end_date',)
    list_filter = ('release_cycle_name', 'start_date', 'end_date',)
    search_fields = ('release_cycle_name',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select ReleaseCycle to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)
    class Media:
        js = ('js/releasecycle.js',)
class FeatureAdmin(admin.ModelAdmin):
    # list_display = ('feature_name', 'feature_description', 'release_cycle',)
    list_filter = ('feature_name',)
    search_fields = ('feature_name', 'feature_label',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select Feature to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)
# Register your models here.

class TestplanAdmin(admin.ModelAdmin):
    list_display = ('testplan_name', 'testplan_marker',)
    list_filter = ('testplan_name',)
    search_fields = ('testplan_name',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select Testplan to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)

class AccessPointAdmin(admin.ModelAdmin):
    list_display = ('model', 'ip','attached',)
    list_filter = ('model', 'ip',)
    search_fields = ('model', 'ip',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select AccessPoint to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    class Media:
        js = ('js/accesspoint.js',)

class TrafficGeneratorAdmin(admin.ModelAdmin):
    list_display = ('name','ip','attached',)
    list_filter = ('name','ip',)
    search_fields = ('name','ip',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select TrafficGenerator to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    class Media:
        js = ('js/trafficgenerator.js',)

class CategoryChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            if(hasattr(obj,"serial")):
                if(obj.attached):
                    return obj.model + " : " + obj.ip + " : attached"
                else:
                    return obj.model + " : " + obj.ip
            else:
                if(obj.attached):
                    return obj.name + " : attached"
                else:
                    return obj.name

class TestbedAdmin(admin.ModelAdmin):
    form=TBForm
    list_display = ('testbedname','accesspoint','trafficgenerator','status',)
    list_filter = ('testbedname','accesspoint','trafficgenerator','status',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select TestBed to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    class Media:
        js = ('js/testbed.js','data_files/testbeds.json')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if(db_field.name == "accesspoint"):
            # print(kwargs)
            #kwargs["queryset"] = "akhil"
            return CategoryChoiceField(queryset=AccessPoint.objects.all())
        elif(db_field.name == "trafficgenerator"):
            return CategoryChoiceField(queryset=TrafficGenerator.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class TestSchedulerAdmin(admin.ModelAdmin):
    list_display = ('tester','starttime','testbed',)
    list_filter = ('tester','starttime','testbed',)
    search_fields = ('tester','starttime','testbed',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select TestScheduler to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)

class TesterAdmin(admin.ModelAdmin):
    list_display = ('name','email','status')
    list_filter = ('name','email','status')
    search_fields = ('name','email')
    exclude = ('chart',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select Tester to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        js = ('js/tester.js',)

class FirmwareImageAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Select Firmware Image to Change/View'} 
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Tester,TesterAdmin)
admin.site.register(AccessPoint,AccessPointAdmin)
admin.site.register(TrafficGenerator,TrafficGeneratorAdmin)
admin.site.register(Testbed,TestbedAdmin)
admin.site.register(TestScheduler,TestSchedulerAdmin)
admin.site.register(Testplan,TestplanAdmin)
admin.site.register(FirmwareImage,FirmwareImageAdmin)
admin.site.register(ReleaseCycle,ReleaseCycleAdmin)
admin.site.register(Feature,FeatureAdmin)