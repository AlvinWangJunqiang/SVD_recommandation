# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:18:10 2017

@author: gzs10228
"""

import pandas as pd
from pandas import DataFrame
import zipfile
from collections import Counter 
import gzip
import re
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
    for u_list in data:
        try:
            if (u_list[-1] == '2')&(u_list[4] == '1'):#首次登陆的视频语音用户
                today_urs.append(u_list[2])
        except:
#            print str(e)
            pass
    new_urs = list(set(today_urs))
    try:
        new_urs.remove('-2')
    except:
        pass
    return new_urs


def read_data(date_str):
    try:
#        date_str_chat  = 'cc.'+date_str[:4]+'-'+date_str[4:6]+'-'+date_str[6:]
#        path_chat = u'/data3/data/%s/%s.log' % ('chat',date_str_chat)      
#        path_4_5 = u'/data3/data/logs/%s/%s.log' % ('4_5',date_str)
#        path_9_31_2 = u'/data3/data/logs/%s/%s.log' % ('9_31_2',date_str)
        path_2_5 = u'/data3/data/logs/%s/%s.log' % ('coin_cost',date_str)
#        f = open(path_9_31_2, 'r')
        f2 = open(path_2_5,'r')
#        f3 = open(path_chat,'r')
#        f4 = open(path_4_5,'r')
    except:
#        path_9_31_2 = u'/data3/data/logs/%s/%s.log.gz' % ('9_31_2',date_str)
        path_2_5 = u'/data3/data/logs/%s/%s.log.gz' % ('coin_cost',date_str)
#        path_chat = u'/data3/data/%s/%s.log.gz' % ('chat',date_str_chat)
#        path_4_5 = u'/data3/data/logs/%s/%s.log.gz' % ('4_5',date_str)
#        f = gzip.open(path_9_31_2, 'rb')
        f2 = gzip.open(path_2_5,'rb')
#        f3 = gzip.open(path_chat,'rb')
#        f4 = gzip.open(path_4_5,'rb')
    return f2


import datetime
def getDays(date_str):  
    date_format="%Y%m%d";  
    bd=datetime.datetime.strptime(date_str,date_format)
    sevenDay=datetime.timedelta(days=6)   
    ed = bd+sevenDay
#    ed=datetime.datetime.strptime(bd+sevenDay,date_format)
    oneday=datetime.timedelta(days=1)  
    count=0
    while bd!=ed:  
        ed=ed-oneday  
        count+=1
    li=[]  
    for i in range(0,count+1):   
        li.append(str(bd.date()).replace('-',''))  
        bd=bd+oneday  
    return li  
import calendar
def get_all_month_urs(year,month,terminal,template):
#    temp = []
    room = 'all'
    day_list =  range(calendar.monthrange(year, month)[1]+1)[1:]
    
    uid_new_urs = []
    dict_result = {}
    
    if month<10:
        month = '0'+str(month)
    else:
        month = str(month)
    for day in day_list:
        if day == 24:
            break
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
        new_urs = get_data(z)  #this date new_urs
        uid_new_urs.extend(new_urs)
        date_list = getDays(date)
        
#        uid_sevenDays_dianping = []
        uid_sevenDays_cost = []
#        uid_sevenDays_chat = []
#        uid_sevenDays_sugar = []
#        print date_list
#        print '---%s---new_urs:%d'%(date,len(new_urs)) 
        print date
        for date_str in date_list:
            f2 = read_data(date_str)
#            for content in f.readlines():
#                try:
#                    content = content.split(",,")
#                    uid = content[2][4:]
#                    if uid != '-2':
#                        uid_sevenDays_dianping.append(uid)
##                        uid_dianping.extend()
#                except Exception as e:
#                    print 'dianping read_lines:%s'%(str(e))
#            f.close()

            
            for content in f2.readlines():
                try:
                    content = content.split(",,")
                    uid = content[6][4:]
                    coin_type = content[8][10:]
                    template_type = content[14][14:]
                    if uid != '-2' and coin_type == 'pquan' and template_type == template:
                        uid_sevenDays_cost.append(uid)
                except Exception as e:
                    print 'cost read_lines:%s'%(str(e))
            f2.close()
    
            

            
#            for content in f3.readlines():
#                try:
#                    uid = re.findall('"Uid":(.*?),',content)[0].strip() 
#                    Action = re.findall('"Action":(.*?),',content)[0].strip()
#                    if (uid !='-2') & (Action == '48'):
#                        uid_sevenDays_chat.append(uid)
#                except Exception as e:
##                    print 'chat read_lines:%s'%(str(e))
#                    pass
#            f3.close()                    
#            
            
#            for content in f4.readlines():
#                try:
#                    content = content.split(",,")
#                    uid = content[2][7:]
#                    if uid != '-2':
#                        uid_sevenDays_sugar.append(uid)
#                except Exception as e:
#                    print 'cost read_lines:%s'%(str(e))                
#            f4.close()
#            
            
            
        result_cost = list(set(new_urs).intersection(set(uid_sevenDays_cost)))
#        result_dianping = list(set(new_urs).intersection(set(uid_sevenDays_dianping)))
#        result_chat = list(set(new_urs).intersection(set(uid_sevenDays_chat)))
#        result_sugar = list(set(new_urs).intersection(set(uid_sevenDays_sugar)))
        
#        inter_list = []
#
#        inter_list.append(result_dianping)
#        inter_list.append(result_chat)
#        inter_list.append(result_sugar)
        
#        hudong = list(set(inter_list[0]).union(*inter_list[1:]))
#        hudong_result = list(set(new_urs).intersection(set(hudong)))
        temp = []
#        temp.append(len(hudong_result))
        temp.append(len(result_cost))
        dict_result[date] = temp        
        
#        print '--%s,new_urs:%d,dianping:%d,sugar:%d,chat:%d,hudong:%d,cost:%d'%(date,len(set(new_urs)),len(set(result_dianping)),len(set(result_sugar)),len(set(result_chat)),len(set(hudong_result)),len(set(result_cost)))
#        print '--%s:dianping:%d,cost:%d,chat:%d,sugar:%d'%(date,len(set(result_dianping)),len(set(result_cost)),len(set(result_chat)),len(set(result_sugar)))
#    print pd.DataFrame(dict_result,index = ['hudong','fufei']).T
    print pd.DataFrame(dict_result,index = ['fufei']).T
    print 'new_urs_23:%d'%(len(uid_new_urs))
        


if __name__ == '__main__':
    year = 2017
#    month = 6
#    terminal = 'all'
#    template = 'ent'
#    print 'all'
#    for month in range(1,7):
#        print month
#        get_all_month_urs(year,month,'all','all')
    print 'all'
    for month in range(1,2):
        print month
        get_all_month_urs(year,month,'all','game')
#    print 'game'
#    for month in range(2,7):
#        get_all_month_urs(year,month,'all','game')



#def read_data(date_str):
#    try:
#        date_str_chat  = 'cc.'+date_str[:4]+'-'+date_str[4:6]+'-'+date_str[6:]
#        path_chat = u'/data3/data/%s/%s.log' % ('chat',date_str_chat)      
#        path_4_5 = u'/data3/data/logs/%s/%s.log' % ('4_5',date_str)
#        path_9_31_2 = u'/data3/data/logs/%s/%s.log' % ('9_31_2',date_str)
#        path_2_5 = u'/data3/data/logs/%s/%s.log' % ('2_5',date_str)
#        f = open(path_9_31_2, 'r')
#        f2 = open(path_2_5,'r')
#        f3 = open(path_chat,'r')
#        f4 = open(path_4_5,'r')
#    except:
#        path_9_31_2 = u'/data3/data/logs/%s/%s.log.gz' % ('9_31_2',date_str)
#        path_2_5 = u'/data3/data/logs/%s/%s.log.gz' % ('2_5',date_str)
#        path_chat = u'/data3/data/%s/%s.log.gz' % ('chat',date_str_chat)
#        path_4_5 = u'/data3/data/logs/%s/%s.log.gz' % ('4_5',date_str)
#        f = gzip.open(path_9_31_2, 'rb')
#        f2 = gzip.open(path_2_5,'rb')
#        f3 = gzip.open(path_chat,'rb')
#        f4 = gzip.open(path_4_5,'rb')
#    return f,f2,f3,f4
#
#


#a = [[1,2,3],[1,2],[2,4]]

        
