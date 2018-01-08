#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import datetime,time

today = datetime.date.today()
#today = today - datetime.timedelta(days=1)
print today
def get_data(start_time,end_time ):
    #start_time='2017-11-08 18:00:00'
    #end_time='2017-11-08 19:00:00'
    os.system("zabbix_api --report \"CPU busy\" \"%s\" \"%s\" --hostgroupid \"2\" --sort 6 --desc >/tmp/cpu.log" % (start_time,end_time))
    os.system("zabbix_api --report \"Processor load (5 min average per core)\" \"%s\" \"%s\" --hostgroupid \"2\" --sort 6 --desc >/tmp/load.log" % (start_time,end_time))

def cpu_data():
    cpu_list=[]
    os.system("cat /tmp/cpu.log |awk 'NR!=1&&NR!=2&&NR!=3&&NR!=4{print $2,$9}'|head -n10 >/tmp/cpu_host.list")
    ch=open("/tmp/cpu_host.list","r")
    for line in ch.readlines():
        line =line.strip('\n')
        line = line.split(' ')
        cpu_list.append(line)
    ch.close()
   # print cpu_list
    return cpu_list

def load_data():
    load_list=[]
    os.system("cat /tmp/load.log |awk 'NR!=1&&NR!=2&&NR!=3&&NR!=4{print $2,$12}'|head -n10 >/tmp/load_host.list")
    lh=open("/tmp/load_host.list","r")
    for line in lh.readlines():
        line = line.strip('\n')
        line = line.split(' ')
        load_list.append(line)
    lh.close()
   # print load_list
    return load_list

def host_data():
    host_list=[]
    os.system("cat /data/police/logs/report.log.%s |grep -A4 -w 'Admin'|grep -w '告警主机'|grep -v '台'|sort |uniq -c |awk '{$2=\"\";sub(\" \",\"\");print |\"sort -r -n -k1\"}'|head -n 10 >/tmp/alarm_host.list" % today)
    ah=open("/tmp/alarm_host.list","r")
    for line in ah.readlines():
        line = line.strip('\n')
        line = line.split(' ')
        host_list.append(line)
    ah.close()
    print host_list
    return host_list

def item_data():
    item_list=[]
    os.system("cat /data/police/logs/report.log.%s |grep -A4 -w 'Admin'|grep -w '告警项目'|awk '{$1=\"\";print}'|sort |uniq  -c|sort -rn -k1|head -n 5 >/tmp/item_host.list" % today)
    ah=open("/tmp/item_host.list","r")
    for line in ah.readlines():
        line = line.strip('\n')
        line = line.split('\t')
        item_list.append(line)
    ah.close()
    for i in range(0,5):
	print item_list[i][0]
    return item_list

def alarm_group():
    group = ['Admin','网络组','电话组','深圳桌面组','互联网业务组','厦门桌面组','北京桌面组','crm运维','互联网运维','coreuser','大数据平台','北京机房运维','互联网数据库','crm1.0业务','大数据业务','crm2.0业务','coreuser业务']
    result = dict()
    os.system("cat /data/police/logs/report.log.%s |grep  '\"【'|awk '{print $1,$2}'|sort |uniq -c|awk '{print $3\":\"$1 }' >/tmp/alarm_group.list" % today)
    f = open("/tmp/alarm_group.list","r")
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        result[line.split(':')[0]] = line.split(':')[1]
    for i in range(0,len(group)):
	if result.has_key(group[i]) == False:
	    os.system("echo '%s:0' >>/tmp/alarm_group.list" % group[i])
	    result[group[i]]=0
	    result[group[i]]=bytes(result[group[i]])
	    print("%s not exists" % group[i])
	else:
	    print("%s exists!!" % group[i])
    f.close()
    #print result
    return result

def recovery_group():
    group = ['Admin','网络组','电话组','深圳桌面组','互联网业务组','厦门桌面组','北京桌面组','crm运维','互联网运维','coreuser','大数据平台','北京机房运维','互联网数据库','crm1.0业务','大数据业务','crm2.0业务','coreuser业务']
    result = dict()
    os.system("cat /data/police/logs/report.log.%s |grep  '\"恢复'|awk '{print $1,$2}'|sort |uniq -c|awk '{print $3\":\"$1 }' >/tmp/recov_group.list" % today)
    f = open("/tmp/recov_group.list","r")
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        result[line.split(':')[0]] = line.split(':')[1]
    for i in range(0,len(group)):
	if result.has_key(group[i]) == False:
	    os.system("echo '%s:0' >>/tmp/recov_group.list" % group[i])
	    result[group[i]]=0
	    result[group[i]]=bytes(result[group[i]])
	    print("%s not exists" % group[i])
	else:
	    print("%s exists!!" % group[i])
    f.close()
    #print result
    return result

def items_percent():
    items_list=[]
    result=dict()
    f = open("/tmp/item_percent.list","r")
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        result[line.split(':')[0]] = line.split(':')[1]
    f.close()
    return result

def get_host_group():
    result = dict()
    os.system("python /home/chenxiaofeng/get_host.py '互联网' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":互联网\"}' >/tmp/host_group")
    os.system("python /home/chenxiaofeng/get_host.py '平台数据部' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":平台数据部\"}' >>/tmp/host_group")
    os.system("python /home/chenxiaofeng/get_host.py 'coreuser' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":coreuser\"}' >>/tmp/host_group")
    os.system("python /home/chenxiaofeng/get_host.py 'crm1.0' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":crm1.0\"}' >>/tmp/host_group")
    os.system("python /home/chenxiaofeng/get_host.py 'crm2.0' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":crm2.0\"}' >>/tmp/host_group")
    os.system("python /home/chenxiaofeng/get_host.py 'Unknown' |sed 's/{u/\\n/g'|grep '10\.'|awk '{print $2}'|awk -F \"'\" '{print $2\":Unknown\"}' >>/tmp/host_group")
    f = open("/tmp/host_group", "r")
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        result[line.split(':')[0]] = line.split(':')[1]
    f.close()
    return result

if __name__ == "__main__":
    #get_data()
    #cpu_data()
    #load_data()
    #host_data()
    alarm_group()
    recovery_group()
    #item_data()
    #items_percent()
    #get_host_group()
