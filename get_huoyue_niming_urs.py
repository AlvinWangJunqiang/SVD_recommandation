# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:43:29 2017

@author: gzs10228
"""

'''日期  帐号(已加密) UID CCID 是否首次登录CC 当天第一次进入时间 当天最后一次退出时间 当天观看视频语音时长(分钟) 当天进入过的房间 用户类型'''

'''        
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

'''计算终端模板的月新用户数、月活跃用户（含匿名）、月匿名用户'''
import pandas as pd
from pandas import DataFrame
import zipfile
from collections import Counter 
import gzip
import calendar

def split_model(x):
    return x.split("\t")

def get_data(z):
#    z = zipfile.ZipFile(path+'20170501.online_urs.zip', "r")
    content = z.read( z.namelist()[0] )    #读取zip文件中的第一个文件
    content_list = content.split("\n")
#print content_list[0]                  #行首列名输出
    res=content_list[1:]
    data = map(split_model,res)
    
    today_urs = []
    niming_urs = []
    new_urs = 0
#    huoyue_urs = 0
#    niming_urs = 0
    for u_list in data:
        try:
            urs = u_list[1]
            uid = u_list[2]
            if (u_list[-1] == '2')&(u_list[4] == '1'):
                new_urs = new_urs+1
            if (u_list[-1] == '2')&(uid != '-2'):
#                huoyue_urs = huoyue_urs+1
                today_urs.append(urs)
            if (u_list[-1] == '2'):
#                niming_urs = niming_urs+1
                s1 = '@android.cc.163.com'
                s2 = '@ios.cc.163.com'
                s3 = '@web.cc.163.com'
                s4 = '@ipad.cc.163.com'
                if (u_list[1].find(s1) != -1)|(u_list[1].find(s2) != -1)|(u_list[1].find(s3) != -1)|(u_list[1].find(s4) != -1):                 
                    niming_urs.append(urs)
        except Exception as e:
            pass
#            print str(e)
    return new_urs,today_urs,niming_urs
#dict_urs = {}.fromkeys(login_urs,1)

def get_all_month_urs(year,month,terminal,template):
    temp = []
    niming_all = []
    room = 'all'
    day_list =  range(calendar.monthrange(year, month)[1]+1)[1:]
    new_urs_all = 0
#    huoyue_all = 0
#    niming_all = 0
    if month<10:
        month = '0'+str(month)
    else:
        month = str(month)
    for day in day_list:
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
  
#        path = r'/data1/cc_dmsystem_data/download_list/%s/%s.online_urs.zip' %('all',date)
        z = zipfile.ZipFile(file_route, "r")
        new_urs,today_urs,niming_urs = get_data(z)
        new_urs_all = new_urs_all+new_urs
        temp.extend(today_urs)
        niming_all.extend(niming_urs)
#        niming_all = niming_all+niming_urs
#        temp.extend(today_urs)
#        dict_urs[date] = new_urs
#        new_urs_num = len(new_urs)
    temp = list(set(temp))
    niming_all_len = len(list(set(niming_all)))
    login_urs = len(temp) -1
    huoyue_all = login_urs + niming_all_len
#        print '------------------------------%d--%s--:%d------------'% (i,date,new_urs_num)
    print terminal+'&:'+ template
    print '%d %d %d'%(new_urs_all,huoyue_all,niming_all_len)
    
if __name__ == '__main__':
    
#    try:
#        for month in range(10,13):
#            get_all_month_urs(2016,month,'all','game')
#    except Exception as e:
#        print str(e)
#    try:
#        for month in range(1,13):
#            get_all_month_urs(2016,month,'all','ent')
#    except Exception as e:
#        print str(e)
    for month in range(8,9):
        get_all_month_urs(2017,month,'all','game')
        get_all_month_urs(2017,month,'pc','game')
        get_all_month_urs(2017,month,'web','game')
        get_all_month_urs(2017,month,'mobile','game')
    
        get_all_month_urs(2017,month,'all','ent')
        get_all_month_urs(2017,month,'pc','ent')
        get_all_month_urs(2017,month,'web','ent')
        get_all_month_urs(2017,month,'mobile','ent')
#    get_all_month_urs(2017,5,'all','all')
#    get_all_month_urs(2017,3,'all','game')
#    get_all_month_urs(2017,2,'all','game')
#    get_all_month_urs(2017,1,'all','game')
#    get_all_month_urs(2016,12,'all','all')
#    get_all_month_urs(2016,11,'all','all')
#
#    get_all_month_urs(2017,5,'pc','game')
#    get_all_month_urs(2017,4,'pc','game')
#    get_all_month_urs(2017,3,'pc','game')
#    get_all_month_urs(2017,2,'pc','game')
#    get_all_month_urs(2017,1,'pc','game')
#    get_all_month_urs(2016,12,'pc','game')
#    get_all_month_urs(2016,11,'pc','game')
#    
#    get_all_month_urs(2017,5,'web','game')
#    get_all_month_urs(2017,4,'web','game')
#    get_all_month_urs(2017,3,'web','game')
#    get_all_month_urs(2017,2,'web','game')
#    get_all_month_urs(2017,1,'web','game')
#    get_all_month_urs(2016,12,'web','game')
#    get_all_month_urs(2016,11,'web','game')
#    
#    get_all_month_urs(2017,5,'mobile','game')
#    get_all_month_urs(2017,4,'mobile','game')
#    get_all_month_urs(2017,3,'mobile','game')
#    get_all_month_urs(2017,2,'mobile','game')
#    get_all_month_urs(2017,1,'mobile','game')
#    get_all_month_urs(2016,12,'mobile','game')
#    get_all_month_urs(2016,11,'mobile','game')    
#    
    
    
