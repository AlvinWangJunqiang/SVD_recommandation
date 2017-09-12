# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:43:29 2017

@author: gzs10228
"""

'''日期  帐号(已加密) UID CCID 是否首次登录CC 当天第一次进入时间 当天最后一次退出时间 当天观看视频语音时长(分钟) 当天进入过的房间 用户类型'''
'''       
    计算月活跃用户天数分布 
 if room=='all' and terminal=='all' and template!='all'  : #全终端不同模板
        file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(template,date)
    if room=='all' and template=='all'  and terminal!='all': #全版本不同终端
        file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(terminal,date)
    if room=='all' and template!='all'  and terminal!='all': #不同终端与模板
        file_route = r'/data1/cc_dmsystem_data/download_list/all_%s_%s/%s.online_urs.zip' %(template,terminal,date)
    if room=='all' and template=='all'  and terminal=='all':#全终端全模板
        file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %('all',date)
    if room!='all' and template=='all'  and terminal=='all':
        file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(room,date)
         
'''
import pandas as pd
from pandas import DataFrame
import zipfile
from collections import Counter 

def split_model(x):
    return x.split("\t")

#获取明细的数据，登录用户urs
def get_data(z):
#    z = zipfile.ZipFile(path+'20170501.online_urs.zip', "r")
    content = z.read( z.namelist()[0] )    #读取zip文件中的第一个文件
    content_list = content.split("\n")
#print content_list[0]                  #行首列名输出
    res=content_list[1:]
    data = map(split_model,res)
    
    today_urs = []
    try:
        for u_list in data:
            urs = u_list[1]
            uid = u_list[2]
            if (u_list[-1] == '2')&(uid != '-2'):#登录用户
                today_urs.append(urs)
    except:pass
    login_urs = list(set(today_urs))
    try:
        login_urs.remove('-2')
    except:
        pass
    return login_urs
#dict_urs = {}.fromkeys(login_urs,1)

#按月存每个用户的在线日期
import calendar
def get_all_terminal(year,month,terminal,template):
    temp = []
    room = 'all'
    day_list =  range(calendar.monthrange(year, month)[1]+1)[1:]
#    dict_urs = {}
    if month<10:
        month = '0'+str(month)
    else:
        month = str(month)
    for day in day_list:
#        if day == 30:break

        if day <10:
            date = str(year)+month+'0'+str(day)
        else:
            date = str(year)+month+str(day)
            
        if room=='all' and terminal=='all' and template!='all'  : #全终端不同模板
            file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(template,date)
        if room=='all' and template=='all'  and terminal!='all': #全版本不同终端
            file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(terminal,date)
        if room=='all' and template!='all'  and terminal!='all': #不同终端与模板
            file_route = r'/data1/cc_dmsystem_data/download_list/all_%s_%s/%s.online_urs.zip' %(template,terminal,date)
        if room=='all' and template=='all'  and terminal=='all':#全终端全模板
            file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %('all',date)
        if room!='all' and template=='all'  and terminal=='all':
            file_route = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %(room,date)

        z = zipfile.ZipFile(file_route, "r")
        login_urs = get_data(z)
        temp.extend(login_urs)
#        print day
#        print '------------------------------%d--%s--%s------------'% (i,date[4:6],file_route[37:45])
    return temp
#计算活跃天数分布
def count_passion_day(temp):
    values_counts = Counter(temp)
    df = DataFrame(data = values_counts.items())                     
    grouped = df.groupby(1).count()
    return grouped
#打印活跃天数分布情况
def print_passion_day(year,month,terminal,template):
#    terminal = 'all'
#    template = 'all'
    print str(month)+':'+terminal+'&'+template
    temp = get_all_terminal(year,month,terminal,template)
    grouped = count_passion_day(temp)
    grouped_list = list(grouped[0])
#    area = 1
    for i in grouped_list:
#        if area == 1:
        print i
        i += 1
        
if __name__ == '__main__':  
    year = 2017
    for month in range(8,9):
        print '----------------------------------------------------------all:all-------------------------------------------------'
        print_passion_day(year,month,'all','all')
        print '----------------------------------------------------------pc:all-------------------------------------------------'
        print_passion_day(year,month,'pc','all')
        print '----------------------------------------------------------web:all-------------------------------------------------'
        print_passion_day(year,month,'web','all')
        print '----------------------------------------------------------mobiletotal:all-------------------------------------------------'
        print_passion_day(year,month,'mobiletotal','all')
        print '----------------------------------------------------------all:ent-------------------------------------------------'
        print_passion_day(year,month,'all','ent')
        print '----------------------------------------------------------all:gametotal-------------------------------------------------'
        print_passion_day(year,month,'all','gametotal')
        
        
        #'fufei_urs.csv'hive，每月调整月份，存在本脚本的目录下
        '''
select distinct to_date(cost_time) as time,
case when template_type in ('game', 'mgame', 'gamestar','gamehost') then 'game'
when template_type='dating' then 'dating'
when template_type='live' then 'live'
else 'ent' end as template,urs
from cc.coin_cost
where date between 20170701 and 20170801 
and coin_type = 'pquan'
        
        
        '''
        
        
        #游戏模板付费用户活跃天数分布
        gametotal_dict = get_all_terminal(year,month,'all','gametotal')
        path_gamefufei = 'fufei_urs.csv'

        gamefufei_urs = pd.read_csv(path_gamefufei) 
        gamefufei_urs = gamefufei_urs[gamefufei_urs['template']=='game']['urs']
        gamefufei_urs_dict = {}
        for item in gamefufei_urs:
            try:
                gamefufei_urs_dict[item] = gametotal_dict[item]
            except:
                gamefufei_urs_dict[item] = 1
                                  
        grouped = count_passion_day(gamefufei_urs_dict)
        grouped_list = list(grouped[0])
        for i in grouped_list:
    #        if area == 1:
            print i
            i += 1



        #娱乐模板付费用户
        ent_dict = get_all_terminal(year,month,'all','ent')
        path_entfufei = 'fufei_urs.csv'
        
        entfufei_urs = pd.read_csv(path_entfufei) 
        entfufei_urs = entfufei_urs[entfufei_urs['template']=='ent']['urs']
        
        entfufei_urs_dict = {}
        for item in entfufei_urs:
            try:
                entfufei_urs_dict[item] = ent_dict[item]
            except:
                entfufei_urs_dict[item] = 1
                                  
        grouped = count_passion_day(entfufei_urs_dict)
        grouped_list = list(grouped[0])
        for i in grouped_list:
    #        if area == 1:
            print i
            i += 1

        