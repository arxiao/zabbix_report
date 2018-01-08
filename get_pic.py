#!/usr/bin/env python
# coding: utf-8

import shutil
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from get_data import *

group_dic = alarm_group()
mendian_alarm = int(group_dic['深圳桌面组']) + int(group_dic['厦门桌面组']) + int(group_dic['北京桌面组'])
recov_dic = recovery_group()
mendian_recov = int(group_dic['深圳桌面组']) + int(group_dic['厦门桌面组']) + int(group_dic['北京桌面组'])
#crm_alarm = int(group_dic['crm1.0']) + int(group_dic['crm2.0'])
# 必须配置中文字体，否则会显示成方块
# 注意所有希望图表显示的中文必须为unicode格式
#custom_font = mpl.font_manager.FontProperties(fname='/Library/Fonts/华文细黑.ttf')

font_size = 10 # 字体大小
fig_size = (8, 6) # 图表大小

names = (u'告警数', u'处理数')
subjects = (u'Admin', u'电话组', u'门店',u'互联网','crm',u'平台数据',u'coreuser') 
scores = ((int(group_dic['Admin']), int(group_dic['电话组']), mendian_alarm,int(group_dic['互联网运维']),int(group_dic['crm运维']),int(group_dic['大数据平台']),int(group_dic['coreuser'])), (int(recov_dic['Admin']), int(recov_dic['电话组']), mendian_recov,int(recov_dic['互联网运维']),int(recov_dic['crm运维']),int(recov_dic['大数据平台']),int(recov_dic['coreuser']))) 

# 更新字体大小
mpl.rcParams['font.size'] = font_size
# 更新图表大小
mpl.rcParams['figure.figsize'] = fig_size
# 设置柱形图宽度
bar_width = 0.35

index = np.arange(len(scores[0]))
# 绘制【告警】数量
rects1 = plt.bar(index, scores[0], bar_width, color='#ED1C24', label=names[0])
# 绘制【恢复】数量
rects2 = plt.bar(index + bar_width, scores[1], bar_width, color='#0072BC', label=names[1])
# X轴标题
plt.xticks(index + bar_width, subjects)
# Y轴范围
plt.ylim(ymax=int(group_dic['Admin']) + 50 , ymin=0)
# 图表标题
plt.title(u'各组告警以及处理数量(告警收敛，处理数可能大于告警数)')
# 图例显示在图表下方
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)

# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')

add_labels(rects1)
add_labels(rects2)

# 图表输出到本地
plt.savefig('group.png')
shutil.copy("group.png","/data/site/zabbix.zhenai.com/zabbix/")
