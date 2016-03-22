# coding=utf-8
__author__ = 'lihao,18621575908'
'''
版权所有：上海宁卫信息技术有限公司
功能说明：本程序只适用于落地与落地间消化话费，而不适用于其它骚扰类型的应用
授权模式：GPL
bug report:lihao@nway.com.cn
'''
import time
import thread
import os,sys
import psycopg2
from ESL import *
import string
import datetime
import random
mylock = thread.allocate_lock()
#global var

fs_ip = '127.0.0.1'
fs_esl_port = '8021'
fs_esl_auth = 'ClueCon'
rings = []
global ring_count
ring_count = 0

max_call = 30
base_path = '/usr/local/src/nway_ac/nway_ac/'
gateway_url = 'sofia/gateway/tojp/'

#//global var
def GetDbConn():
    conn = psycopg2.connect(database="nway_ac", user="postgres", password="nway_2015And", host="127.0.0.1", port="5432")
    return conn

def GetCurrentPath():
    return os.getcwd()

def SetAllIdle():
    conn = GetDbConn()
    querysql = 'UPDATE callout_numbers   SET callout_state=0, last_call_time=current_timestamp ;'
    cur = conn.cursor()
    cur.execute(querysql)
    conn.commit()
    print 'SetNumberIdle:ALL'
    cur.close()
    conn.close()

def GetBaseConfig():
    conn = GetDbConn()
    querysql = 'SELECT config_name, config_param  FROM base_config;'
    cur = conn.cursor()
    cur.execute(querysql)
    rows = cur.fetchall()
    conn.commit()

    for row in rows:
        config_name = row[0]
        if (cmp(config_name , 'max_call') == 0):
            max_call = row[1]
        if (cmp(config_name , 'base_path')==0):
            base_path = row[1]
        if (cmp(config_name , 'gateway_url')==0):
            gateway_url = row[1]
    print 'max_call:' + max_call
    print 'base_path:' +base_path
    print 'gateway_url:'+ gateway_url
    cur.close()
    conn.close()

def SetNumberBusy(dest_number):
    conn = GetDbConn()
    querysql = 'UPDATE callout_numbers   SET callout_state=1  WHERE call_numbers =\'' + dest_number +'\''
    cur = conn.cursor()
    cur.execute(querysql)
    conn.commit()
    print 'SetNumberBusy:' +dest_number
    cur.close()
    conn.close()

def CheckCallTime():
    conn = GetDbConn()
    querysql = 'SELECT a.id, a.start_time, a.stop_time,b.id \
                 FROM time_plan a, nway_call_tasks b where (now()::time > a.start_time ) and ' \
               '(now()::time < a.stop_time) and (now()<b.stop_time ) and (now() > b.begin_time);'
    cur = conn.cursor()
    cur.execute(querysql)
    rows = cur.fetchall()
    ret_value = False
    if cur.rowcount > 0:
        ret_value = True
    conn.commit()
    cur.close()
    conn.close()
    return ret_value


def CallOut(dial_string,call_number):
    con = ESLconnection(fs_ip, fs_esl_port, fs_esl_auth)
    if con.connected():
        e = con.api(dial_string)
        SetNumberBusy(call_number)
        print e.getBody()
    else:
        print 'not Connected'
    con.disconnect();

def GetRingPath():
    #print 'ring count:' .join(str(rings.count()))
    global ring_count
    index = random.randint(0,ring_count -1)
    print 'ring count:' + str(ring_count) + ',this index:'+ str(index)
    return rings[index]
def GetRandomTimeout():
    timeout =500
    timeout = random.randint(300,5000)
    return timeout

def AutoCall(a,b):

    print 'Start Auto Calls'
    while True:
        try:
            conn = GetDbConn()
            if CheckCallTime()==True:
                querysql = 'SELECT a.id, a.call_numbers,a. call_timeout, a.call_ring_id, a.callout_state, \
                            a.is_enable, a.last_call_time\
                            FROM callout_numbers a  where a.is_enable=True and' \
                           ' a.callout_state =0;  '
                #OR  ceil(abs(extract(epoch from current_timestamp -a. last_call_time))) > a.call_timeout)
                #print querysql
                cur = conn.cursor()
                cur.execute(querysql)
                rows = cur.fetchall()
                for row in rows:
                    print cur.rowcount
                    call_number = row[1]
                    call_timeout = row[2]
                    call_ring_id = row[3]
                    ring_path = base_path + GetRingPath()
                    dial_string = 'originate {execute_on_pre_answer=start_da,execute_on_answer=stop_da,execute_on_answer=\'sched_hangup +' + str(GetRandomTimeout()) + '\'}'+gateway_url + \
                                  call_number + ' &endless_playback(\'' + ring_path + '\')'
                    CallOut(dial_string, call_number)
                    print dial_string
                    time.sleep(0.070)
                cur.close()
            conn.close()
        except:
            print 'access database failed\n'
        time.sleep(0.10)
        #print 'CheckCallTime'

    #conn.close()
    thread.exit_thread()

def GetAllRings():
    conn = GetDbConn()
    querysql = 'SELECT ring_path from call_rings;'
    cur = conn.cursor()
    cur.execute(querysql)
    rows = cur.fetchall()
   #ring_count = rows.rowcount
    #count=0
    global ring_count
    for row in rows:
        rings.append(row[0])
        ring_count += 1
       # print row[0]
    for i in rings:
        print i
   # ring_count = count
    print 'ring_count:' + str(ring_count)
    conn.commit()
    cur.close()
    conn.close()


def SetNumberIdle(dest_number):
    conn = GetDbConn()
    querysql = 'UPDATE callout_numbers   SET callout_state=0, last_call_time=current_timestamp WHERE call_numbers =\'' + dest_number +'\''
    cur = conn.cursor()
    cur.execute(querysql)
    conn.commit()
    print 'SetNumberIdle:' + dest_number
    cur.close()
    conn.close()

if __name__ == '__main__':
    GetBaseConfig()
    #str='python- String function'
    #print '%s startwith t=%s' % (str,str.startswith('t'))
    #print '%s' % (str.replace('-',''))
    SetAllIdle()
    GetAllRings()
    con = ESLconnection(fs_ip, fs_esl_port, fs_esl_auth)
    if con.connected():
        thread.start_new_thread(AutoCall,(1,1))
        e = con.events('plain','CHANNEL_HANGUP_COMPLETE CUSTOM:da')
        #CUSTOM:da为自定义的电话铃音检测模块消息
        while True:
            ee = con.recvEvent()
            #print ee
            event_name = ee.getHeader( 'Event-Name')
            event_subclass = ee.getHeader('Event-Subclass')
            if ee and event_name == 'CUSTOM' and event_subclass == 'da':
                #检测到了电话铃音分析结果
                da_type = ee.getHeader('da_type')
                #分析结果，由da_type来送出，即空号，忙等
                da_similarity = ee.getHeader('da_similarity')
                #da_similarity是和样本库中检测的实际样本的相似性百分比
                print da_type, da_similarity
            if ee and event_name == 'HANGUP_COMPLETE':
                my_number =  ee.getHeader('Caller-Caller-ID-Number')
                dest_number = ee.getHeader('Caller-Destination-Number')
                SetNumberIdle(dest_number)
                #在此处处理挂机事件
    con.disconnect();
