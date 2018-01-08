#!/usr/bin/env python
#coding:utf8
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import sys
import os
import random
import shutil
import datetime
import time
import calendar
from get_data import *
from matplotlib import pyplot as plt 
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')


def send_mail(to_list, sub):
      me = mail_user 
      msg = MIMEMultipart()
      msg['Subject'] = sub
      msg['From'] = 'Monitor Center'
      msg['To'] = ",".join(to_reciver)
      msg['Cc'] = ",".join(cc_reciver)
      to_list = to_reciver + cc_reciver
      today = datetime.date.today()
      lastMonday = today - datetime.timedelta(days=7)
      begin_time = lastMonday.strftime('%Y-%m-%d 00:00:00')	
      print begin_time
      lastSunday = today - datetime.timedelta(days=1)
      end_time = lastSunday.strftime('%Y-%m-%d 23:59:59')
      print end_time
      get_data(begin_time,end_time)
      cpu_list = cpu_data()
      load_list = load_data()
      host_list = host_data()
      group_dic = alarm_group()
      percent_dic = items_percent()
      host_group = get_host_group()
      os.system("python /data/zabbix_report/get_pic.py")
      #print cpu_list
      #print load_list
      #print host_list
      #print group_dic
      #调节图形大小，宽，高
      plt.figure(figsize=(8,12))
      #定义饼状图的标签，标签是列表
      #labels = [u'第一部分',u'第二部分',u'第三部分']
      labels = percent_dic.keys()
      #每个标签占多大，会自动去算百分比
      #sizes = [60,30,10]
      sizes = percent_dic.values()
      title = u'各监控项告警占比'
      #colors = ['red','yellowgreen','lightskyblue']
      colors = plt.cm.rainbow(np.linspace(0.9,0,len(labels)))
      #将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
      explode = (0.1,0,0,0.1,0,0.1,0,0,0)
      #explode = [0 for _ in labels]

      patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = True,
                                startangle = 90,pctdistance = 0.6)

      #labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
      #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
      #shadow，饼是否有阴影
      #startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
      #pctdistance，百分比的text离圆心的距离
      #patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

      #改变文本的大小
      #方法是把每一个text遍历。调用set_size方法设置它的属性
      for t in l_text:
          t.set_size=(30)
      for t in p_text:
          t.set_size=(20)
      # 设置x，y轴刻度一致，这样饼图才能是圆的
      plt.axis('equal')
      plt.legend()
      plt.title(title)
      plt.savefig('item_percent.png')
      shutil.copy("item_percent.png","/data/site/zabbix.zhenai.com/zabbix/")

#构造html
      html = """\
<html xmlns="http:#zabbix.oa.com/">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>监控系统运营周报</title>
<body>
<div id="container">
<p align="left" style="font-size:15px"><font color="336666"><strong>统计分析时间段:  """ + str(lastMonday) + '    to    ' + str(lastSunday) + """</strong></font></p>

<div align="center"><img src="http://10.1.1.64/zabbix/item_percent.png" alt="图片加载失败" width=600 height=600/></div>
<div align="center"><img src="http://10.1.1.64/zabbix/group.png" alt="图片加载失败" width=600 height=600/></div>

<p align="center" style="font-size:20px"><strong>CPU利用率Top10</strong></p>
<div id="content">
 <table width="900" border="1" cellspacing="1" bordercolor="009393" align="center">
<tr>
  <td bgcolor="810C0C0" align="center"><strong>排名</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>主机</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>所属组</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>告警类型</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>值</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>业务负责人</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>运维负责人</strong></td>
</tr>
<tr>
  <td align="center">1</td>
  <td align="center">""" + cpu_list[0][0] + """</td>
  <td align="center">""" + host_group[cpu_list[0][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[0][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[0][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[0][0]]] + """</td>
</tr>
<tr>
  <td align="center">2</td>
  <td align="center">""" + cpu_list[1][0] + """</td>
  <td align="center">""" + host_group[cpu_list[1][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[1][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[1][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[1][0]]] + """</td>
</tr>
<tr>
  <td align="center">3</td>
  <td align="center">""" + cpu_list[2][0] + """</td>
  <td align="center">""" + host_group[cpu_list[2][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[2][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[2][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[2][0]]] + """</td>
</tr>
<tr>
  <td align="center">4</td>
  <td align="center">""" + cpu_list[3][0] + """</td>
  <td align="center">""" + host_group[cpu_list[3][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[3][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[3][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[3][0]]] + """</td>
</tr>
<tr>
  <td align="center">5</td>
  <td align="center">""" + cpu_list[4][0] + """</td>
  <td align="center">""" + host_group[cpu_list[4][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[4][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[4][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[4][0]]] + """</td>
</tr>
<tr>
  <td align="center">6</td>
  <td align="center">""" + cpu_list[5][0] + """</td>
  <td align="center">""" + host_group[cpu_list[5][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[5][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[5][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[5][0]]] + """</td>
</tr>
<tr>
  <td align="center">7</td>
  <td align="center">""" + cpu_list[6][0] + """</td>
  <td align="center">""" + host_group[cpu_list[6][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[6][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[6][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[6][0]]] + """</td>
</tr>
<tr>
  <td align="center">8</td>
  <td align="center">""" + cpu_list[7][0] + """</td>
  <td align="center">""" + host_group[cpu_list[7][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[7][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[7][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[7][0]]] + """</td>
</tr>
<tr>
  <td align="center">9</td>
  <td align="center">""" + cpu_list[8][0] + """</td>
  <td align="center">""" + host_group[cpu_list[8][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[8][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[8][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[8][0]]] + """</td>
</tr>
<tr>
  <td align="center">10</td>
  <td align="center">""" + cpu_list[9][0] + """</td>
  <td align="center">""" + host_group[cpu_list[9][0]] + """</td>
  <td align="center">CPU利用率平均值</td>
  <td align="center">""" + cpu_list[9][1] + '%' + """</td>
  <td align="center">""" + business[host_group[cpu_list[9][0]]] + """</td>
  <td align="center">""" + operation[host_group[cpu_list[9][0]]] + """</td>
</tr>
</table>
</div>
<div id="container">
<p align="center" style="font-size:20px"><strong>5分钟平均负载Top10</strong></p>
<div id="content">
 <table width="900" border="1" bordercolor="009393" cellspacing="1" align="center">
<tr>
  <td bgcolor="810C0C0" align="center"><strong>排名</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>主机</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>所属组</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>告警类型</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>值</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>业务负责人</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>运维负责人</strong></td>
</tr>
<tr>
  <td align="center">1</td>
  <td align="center">""" + load_list[0][0] + """</td>
  <td align="center">""" + host_group[load_list[0][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[0][1] + """</td>
  <td align="center">""" +business[host_group[load_list[0][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[0][0]]] + """</td>
</tr>
<tr>
  <td align="center">2</td>
  <td align="center">""" + load_list[1][0] + """</td>
  <td align="center">""" + host_group[load_list[1][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[1][1] + """</td>
  <td align="center">""" +business[host_group[load_list[1][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[1][0]]] + """</td>
</tr>
<tr>
  <td align="center">3</td>
  <td align="center">""" + load_list[2][0] + """</td>
  <td align="center">""" + host_group[load_list[2][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[2][1] + """</td>
  <td align="center">""" +business[host_group[load_list[2][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[2][0]]] + """</td>
</tr>
<tr>
  <td align="center">4</td>
  <td align="center">""" + load_list[3][0] + """</td>
  <td align="center">""" + host_group[load_list[3][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[3][1] + """</td>
  <td align="center">""" +business[host_group[load_list[3][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[3][0]]] + """</td>
</tr>
<tr>
  <td align="center">5</td>
  <td align="center">""" + load_list[4][0] + """</td>
  <td align="center">""" + host_group[load_list[4][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[4][1] + """</td>
  <td align="center">""" +business[host_group[load_list[4][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[4][0]]] + """</td>
</tr>
<tr>
  <td align="center">6</td>
  <td align="center">""" + load_list[5][0] + """</td>
  <td align="center">""" + host_group[load_list[5][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[5][1] + """</td>
  <td align="center">""" +business[host_group[load_list[5][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[5][0]]] + """</td>
</tr>
<tr>
  <td align="center">7</td>
  <td align="center">""" + load_list[6][0] + """</td>
  <td align="center">""" + host_group[load_list[6][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[6][1] + """</td>
  <td align="center">""" +business[host_group[load_list[6][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[6][0]]] + """</td>
</tr>
<tr>
  <td align="center">8</td>
  <td align="center">""" + load_list[7][0] + """</td>
  <td align="center">""" + host_group[load_list[7][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[7][1] + """</td>
  <td align="center">""" +business[host_group[load_list[7][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[7][0]]] + """</td>
</tr>
<tr>
  <td align="center">9</td>
  <td align="center">""" + load_list[8][0] + """</td>
  <td align="center">""" + host_group[load_list[8][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[8][1] + """</td>
  <td align="center">""" +business[host_group[load_list[8][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[8][0]]] + """</td>
</tr>
<tr>
  <td align="center">10</td>
  <td align="center">""" + load_list[9][0] + """</td>
  <td align="center">""" + host_group[load_list[9][0]] + """</td>
  <td align="center">Processor load (5 min average per core)</td>
  <td align="center">""" + load_list[9][1] + """</td>
  <td align="center">""" +business[host_group[load_list[9][0]]] + """</td>
  <td align="center">""" + operation[host_group[load_list[9][0]]] + """</td>
</tr>
</table>

<!--
<div id="container">
<p align="center" style="font-size:20px"><strong>告警主机top5</strong></p>
<div id="content">
<table width="600" border="1" bordercolor="009393" cellspacing="1" align="center">
<tr>
  <td bgcolor="810C0C0" align="center"><strong>排名</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>主机</strong></td>
  <td bgcolor="810C0C0" align="center"><strong>次数</strong></td>
</tr>
<tr>
  <td align="center">1</td>
  <td align="center">""" + host_list[0][1] + """</td>
  <td align="center">""" + host_list[0][0] + """</td>
</tr>
<tr>
  <td align="center">2</td>
  <td align="center">""" + host_list[1][1] + """</td>
  <td align="center">""" + host_list[1][0] + """</td>
</tr>
<tr>
  <td align="center">3</td>
  <td align="center">""" + host_list[2][1] + """</td>
  <td align="center">""" + host_list[2][0] + """</td>
</tr>
<tr>
  <td align="center">4</td>
  <td align="center">""" + host_list[3][1] + """</td>
  <td align="center">""" + host_list[3][0] + """</td>
</tr>
<tr>
  <td align="center">5</td>
  <td align="center">""" + host_list[4][1] + """</td>
  <td align="center">""" + host_list[4][0] + """</td>
</tr>
<tr>
  <td align="center">6</td>
  <td align="center">""" + host_list[5][1] + """</td>
  <td align="center">""" + host_list[5][0] + """</td>
</tr>
<tr>
  <td align="center">7</td>
  <td align="center">""" + host_list[6][1] + """</td>
  <td align="center">""" + host_list[6][0] + """</td>
</tr>
<tr>
  <td align="center">8</td>
  <td align="center">""" + host_list[7][1] + """</td>
  <td align="center">""" + host_list[7][0] + """</td>
</tr>
<tr>
  <td align="center">9</td>
  <td align="center">""" + host_list[8][1] + """</td>
  <td align="center">""" + host_list[8][0] + """</td>
</tr>
<tr>
  <td align="center">10</td>
  <td align="center">""" + host_list[9][1] + """</td>
  <td align="center">""" + host_list[9][0] + """</td>
</tr>
</table>
-->
<!--
<div id="container">
<p align="center" style="font-size:20px"><strong>告警数量统计</strong></p>
<div id="content">
<table width="1200" border="1" bordercolor="009393" cellspacing="1" style="font-size:15px" align="center">
<tr>
  <td bgcolor="810C0C0" align="center"><strong>组名</strong></td>
  <td align="center">Admin</td>
  <td align="center">crm运维</td>
  <td align="center">互联网运维</td>
  <td align="center">大数据平台</td>
  <td align="center">coreuser</td>
  <td align="center">深圳桌面组</td>
  <td align="center">厦门桌面组</td>
  <td align="center">北京桌面组</td>
  <td align="center">电话组</td>
  <td align="center">网络组</td>
  <td align="center">互联网业务组</td>
  <td align="center">crm1.0业务</td>
  <td align="center">crm2.0业务</td>
  <td align="center">coreuser业务</td>
  <td align="center">大数据业务</td>
</tr>
<tr>
  <td bgcolor="810C0C0" align="center"><strong>数量</strong></td>
  <td align="center">""" + group_dic['Admin'] + """</td>
  <td align="center">""" + group_dic['crm运维'] + """</td>
  <td align="center">""" + group_dic['互联网运维'] + """</td>
  <td align="center">""" + group_dic['大数据平台'] + """</td>
  <td align="center">""" + group_dic['coreuser'] + """</td>
  <td align="center">""" + group_dic['深圳桌面组'] + """</td>
  <td align="center">""" + group_dic['厦门桌面组'] + """</td>
  <td align="center">""" + group_dic['北京桌面组'] + """</td>
  <td align="center">""" + group_dic['电话组'] + """</td>
  <td align="center">""" + group_dic['网络组'] + """</td>
  <td align="center">""" + group_dic['互联网业务组'] + """</td>
  <td align="center">""" + group_dic['crm1.0业务'] + """</td>
  <td align="center">""" + group_dic['crm2.0业务']  + """</td>
  <td align="center">""" + group_dic['coreuser业务'] + """</td>
  <td align="center">""" + group_dic['大数据业务'] + """</td>
</tr>
</table>
-->

<p align="right"><font color="336666"><strong>邮件负责人: xiaofeng.chen</strong></font></p>
</div>
</body>
</html>
      """
      context = MIMEText(html,_subtype='html',_charset='utf-8')  #解决乱码
      msg.attach(context) 
      try:
              send_smtp = smtplib.SMTP()
              send_smtp.connect(mail_host)
              send_smtp.login(mail_user, mail_pass)
              send_smtp.sendmail(me, to_list, msg.as_string())
              send_smtp.close()
              return True
      except Exception, e:
              print str(e)[1]
              return False
if __name__ == '__main__':
  mail_host='smtp.exmail.qq.com'
  mail_user='*******'
  mail_pass='**********'
  mailto_list = ['']
  sub= "监控系统运营周报"
  sub=sub.decode('utf-8')
  if send_mail(mailto_list, sub):
          print "Send mail succed!"
  else:
          print "Send mail failed!"
