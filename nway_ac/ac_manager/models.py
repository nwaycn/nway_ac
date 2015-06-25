# coding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
'''
版权所有：上海宁卫信息技术有限公司
功能说明：本程序只适用于落地与落地间消化话费，而不适用于其它骚扰类型的应用
授权模式：MPL
bug report:lihao@nway.com.cn
'''
from __future__ import unicode_literals

from django.db import models
from django.db import connection
import sys
#sys.setdefaultencoding('utf-8')

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self
def get_sequence_val(seq_name):
    cursor = connection.cursor()
    cursor.execute('select nextval(\'%s\')' % seq_name)
    maxvalue = 1
    try:
        maxvalue = cursor.fetchone()[0]
    except:
        maxvalue = 1
    return maxvalue
class BaseConfig(models.Model):
    config_name = models.CharField(primary_key=True, max_length=50)
    config_param = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_config'


class CallRings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ring_name = models.CharField(max_length=200, blank=True, null=True)
   # ring_path = models.CharField(max_length=255, blank=True, null=True)
    ring_path = models.FileField(u'文件', upload_to='uploads/rings')
    ring_description = models.TextField(blank=True, null=True)
    ring_category = models.BigIntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if (self.id < 1):
            self.id = get_sequence_val('call_rings_id_seq')
        super(CallRings, self).save(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'call_rings'
    def __unicode__(self):
        return self.ring_name


class CalloutNumbers(models.Model):
    id = models.BigIntegerField(primary_key=True)
    call_numbers = models.CharField(max_length=200, blank=True, null=True)
    call_timeout = models.IntegerField(blank=True, null=True)
    call_ring = models.ForeignKey(CallRings, blank=True, null=True)
    callout_state = models.IntegerField(blank=True, null=True)
    is_enable = models.NullBooleanField(default=True)
    last_call_time = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if (self.id < 1):
            self.id = get_sequence_val('callout_numbers_id_seq')
        super(CalloutNumbers, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'callout_numbers'


class NwayCallTasks(models.Model):
    id = models.BigIntegerField(primary_key=True)
    callout_name = models.CharField(max_length=200, blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if (self.id < 1):
            self.id = get_sequence_val('nway_call_tasks_id_seq')
        super(NwayCallTasks, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'nway_call_tasks'


class TimePlan(models.Model):
    id = models.BigIntegerField(primary_key=True)
    start_time = models.TimeField(blank=True, null=True)
    stop_time = models.TimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if (self.id < 1):
            self.id = get_sequence_val('time_plan_id_seq')
        super(TimePlan, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'time_plan'
