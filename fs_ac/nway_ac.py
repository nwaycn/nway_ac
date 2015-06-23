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

mylock = thread.allocate_lock()
#global var

fs_ip = '127.0.0.1'
fs_esl_port = '8021'
fs_esl_auth = 'ClueCon'


max_call = 30
base_path = '/usr/local/src/nway_ac/'
gateway_url = '/sofia/gateway/abc/'

#//global var
def GetDbConn():
    conn = psycopg2.connect(database="nwaycc", user="postgres", password="nway2013", host="127.0.0.1", port="5432")
    return conn

def GetCurrentPath():
    return os.getcwd()


def GetBaseConfig():
    conn = GetDbConn()
    querysql = 'SELECT config_name, config_param  FROM base_config;'
    cur = conn.cursor()
    cur.execute(querysql)
    rows = cur.fetchall()
    conn.commit()

    for row in rows:
        config_name = row[0]
        if (config_name == 'max_call'):
            max_call = row[1]
        if config_name == 'base_path':
            base_path = row[1]
        if config_name == 'gateway_url':
            gateway_url = row['config_param']

    cur.close()
    conn.close()

def SetNumberBusy(dest_number):
    conn = GetDbConn()
    querysql = 'UPDATE callout_numbers   SET callout_state=1  WHERE call_numbers =\'' + dest_number +'\''
    cur = conn.cursor()
    cur.execute(querysql)
    conn.commit()
    cur.close()
    conn.close()

def CallOut(dial_string,call_number):
    con = ESLconnection(fs_ip, fs_esl_port, fs_esl_auth)
    if con.connected():
        e = con.api(dial_string)
        SetNumberBusy(call_number)
        print e.getBody()
    else:
        print 'not Connected'
    con.disconnect();

def AutoCall():
    conn = GetDbConn()
    while True:
        querysql = 'SELECT a.id, a.call_numbers,a. call_timeout, a.call_ring_id, a.callout_state, \
                    a.is_enable, a.last_call_time, b.ring_path \
                    FROM callout_numbers a, call_rings b where a.is_enable=True and' \
                   ' (a.callout_state =0 OR  ceil(abs(extract(epoch from current_timestamp -a. last_call_time))) > a.call_timeout)  \
                    and b.id=a.call_ring_id '
        cur = conn.cursor()
        cur.execute(querysql)
        rows = cur.fetchall()
        for row in rows:
            call_number = row['call_numbers']
            call_timeout = row['call_timeout']
            call_ring_id = row['call_ring_id']
            ring_path = base_path + row['ring_path']
            dial_string = 'originate {execute_on_answer=\'sched_hangup +' + call_timeout + '\'}'+gateway_url + \
                          call_number + ' &endless_playback(\'' + ring_path + '\')'

    conn.close()
    thread.exit_thread()

def SetNumberIdle(dest_number):
    conn = GetDbConn()
    querysql = 'UPDATE callout_numbers   SET callout_state=0, last_call_time=current_timestamp WHERE call_numbers =\'' + dest_number +'\''
    cur = conn.cursor()
    cur.execute(querysql)
    conn.commit()
    cur.close()
    conn.close()
if __name__ == '__main__':
    GetBaseConfig()
    #str='python- String function'
    #print '%s startwith t=%s' % (str,str.startswith('t'))
    #print '%s' % (str.replace('-',''))
    con = ESLconnection(fs_ip, fs_esl_port, fs_esl_auth)
    if con.connected():
        thread.start_new_thread(AutoCall)
        e = con.events('plain','CHANNEL_HANGUP_COMPLETE')
        while True:
            ee = con.recvEvent()
            if ee:
                my_number =  ee.getHeader('Caller-Caller-ID-Number')
                dest_number = ee.getHeader('Caller-Destination-Number')
                SetNumberIdle(dest_number)
                #在此处处理挂机事件
    con.disconnect();