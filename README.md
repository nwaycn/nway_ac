# NWayRtcSDK介绍

## iOS版本：

https://github.com/nwaycn/NWayRtcDemo-IOS

## android版本：

https://github.com/nwaycn/NWayRtcDemo_Android

## AMR版本：

https://github.com/nwaycn/NWayRtcDemo_ARM


## 能力及标准：
```
1 支持标准SIP RFC3261协议。多平台支持(andorid,ios. mac ,windows,linux,嵌入式linux arm)。

2 音频：
  A 支持编码解码格式：ISAC、G722、G711 ,L16,OPUS，ILBC
  B 音频前处理3A算法，AEC (Acoustic Echo Cancellation)，ANS (Automatic Noise Suppression)，AGC (Automatic Gain Control)。
C 支持动态抖动缓冲区和错误隐藏（丢包补偿）算法NetEQ。
D 支持JitterBuff，FEC，NACK。

3 视频：
   A 支持编码解码格式：VP8,VP9,H264,H265，支持硬件编解码。
   B 支持QOS：
NACK、FEC、SVC、JitterBuffer、IDR Request、PACER、Sender Side BWE、VFR（动态帧率调整策略）、AVSync（音视频同步）、动态分辨率调整。

 4功能：
   A：支持单人,多人视频通话,视频会议。
   B：支持主流SIP服务器，如：opensips，freeswitch。
   C：支持传输原生编码好的音视频数据。
   D：支持ICE P2P模式和服务器转发模式。
   E：支持移动平台Push Notification，配合我们定制的opensips服务器可以很好的唤醒sdk接受呼叫
   F：服务端支持分布式，集群部署。
```


mobile(wechat) +8618621575908


有不少朋友问，我们如何实现cdr呢,那么可以编译时加pg-core条件，且配置cdr_pg让cdr直接记录到postgresql数据库中。

# nway_ac
提醒：如果呼的量比较大的话，可以先关掉log或者把log中的debug，info等去掉。没必要的话，把cdr_csv模块也干掉，不然呼的太快，磁盘受不了。

一、	说明

Nway_ac为nway auto call的缩写，主要用于落地间对接时，可能需要产生一定量的话费消耗，故而采用FreeSWITCH作为后端，使用python作为开发及运行语言来实现定向呼叫。


二、	运行环境搭建（centos为例,debian,windows基本类似）

1.	以FreeSWITCH 1.2.24为例，不再另行介绍

2.	安装python2.7


#wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz

#tar zxvf Python-2.7.3.tgz

#cd Python-2.7.3

#./configure --prefix=/usr && make && make install


3.	curl https://bootstrap.pypa.io/ez_setup.py | python 用于安装easy_install工具

4.	安装postgresql，这里不多讲这个数据库安装的用例

5.	安装django:# easy_install django

6.	安装 psycopg2：#easy_install psycopg2

7.	在FreeSWITCH的源码环境下：#cd  libs/esl

   #make pymod

8.	下载nway_ac  #git clone https://github.com/nwaycn/nway_ac.git

9.	导入数据库，安装好的预创建数据库nway_ac 并进入db目录下

#psql  -U postgres  -W -d nway_ac-f nway_ac.sql


10.	修改nway_ac/nway_ac/ settings.py 将正确的数据库配置更新在其中

11.	修改 fs_ac/ nway_ac.py 将正确的数据库配置更新其中

12.	在 nway_ac下运行

#python manage.py runserver 0.0.0.0:8000
这样即可在浏览器中ip:8000/admin中访问该页面
默认的用户名：admin 密码：nway123

13.	在fs_ac下运行 

#python nway_ac.py即可开始工作

三、	页面简易说明
1.	所有页面菜单
 
2.	基本配置
 
3.	彩铃管理
 
4.	时间计划(在此时间段内才会有效呼叫，全天的则只需要00:00-24:00即可)
 
5.	呼叫任务管理(和时间计划配合在内实现自动呼叫)
 
6.	号码管理(基本为固定的，和并发量差不多的号码即可)
 
这里用于维护呼叫的号码等
相关的图在docs中使用说明中有
