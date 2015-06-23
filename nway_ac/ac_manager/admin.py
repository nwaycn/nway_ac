# -*-coding:utf-8 -*-
'''
版权所有：上海宁卫信息技术有限公司
功能说明：本程序只适用于落地与落地间消化话费，而不适用于其它骚扰类型的应用
授权模式：MPL
bug report:lihao@nway.com.cn
'''
from django.contrib import admin
from ac_manager.models import *
class BaseConfigAdmin(admin.ModelAdmin):
    list_display = ('config_name','config_param')

class CallRingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ring_name', 'ring_path')
    readonly_fields = ('id',)
    fields =  ('id', 'ring_name', 'ring_path')

class CalloutNumbersAdmin(admin.ModelAdmin):
    list_display = ('id' , 'call_numbers', 'call_timeout', 'call_ring', 'callout_state', 'is_enable')
    readonly_fields = ('id',)

class NwayCallTasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'callout_name', 'begin_time', 'stop_time')
    readonly_fields = ('id',)

class TimePlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'stop_time')
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(BaseConfig, BaseConfigAdmin)
admin.site.register(CallRings, CallRingsAdmin)
admin.site.register(CalloutNumbers, CalloutNumbersAdmin)
admin.site.register(NwayCallTasks, NwayCallTasksAdmin)
admin.site.register(TimePlan, TimePlanAdmin)