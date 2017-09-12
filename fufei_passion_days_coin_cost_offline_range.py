# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:12:38 2017

@author: gzs10228
"""

#'''付费用户的活跃天数分布。
#'''

import pandas as pd
from pandas import DataFrame
import zipfile
from collections import Counter 
import gzip
import calendar
import re
from collections import Counter 

def get_source_data(path):

    f = open(path, 'r')
    return f

def get_fufei_urs_by_month(template,path):
    dict_fufei = {}
    f = get_source_data(path)   
    for line in f.readlines():
        try:
            content = line.split(",")
            uid = content[2][:-1]
            date_this = content[0].replace('-','')
            template_this = content[1]
#        except:pass
            if template_this != template:continue#
#            this_month = content[0][5:7]
#            this_year = content[0][:4]
#            if int(this_month)>=7:continue
#            if int(this_month) == 6:
#                if this_year == '2016':
#                    continue          
#            template_this = content[1]
#            if template_this != template:
#                continue        
            try:
                if uid in dict_fufei[str(date_this)]:
                    continue
            except:pass
            if str(date_this) in dict_fufei.keys():
                temp = []
                temp.append(uid)
                dict_fufei[str(date_this)].extend(temp)
#                        dict_day[uid]=list(set(dict_day[uid]))
            else:
#                        pass
                temp = []
                temp.append(uid)
                dict_fufei[str(date_this)] = temp 
        except Exception as e:
            print str(e)
    return dict_fufei

#用于跑各模板登录匿名用户活跃天数分布
#def get_dict_2(path):
#
#    f = get_source_data(path)   
#    dict_day = {}
#    for line in f.readlines():
#        try:
#            content = line.split(",")
##            except:pass
#            uid = content[1][:-1]
#            date_this = content[0].replace('-','')
#            if date_this[3] == '6' or date_this[5] != '8':continue
##            template_this = content[1]
#            day = date_this[6:]
##            except:pass
##            if template_this != template:continue#
#            
#            try:
#                temp = []
#                temp.append(str(day))
#                dict_day[uid].extend(temp)
##                        dict_day[uid]=list(set(dict_day[uid]))
#            except:
##                        pass
#                temp = []
#                temp.append(str(day))
#                dict_day[uid] = temp 
#        except Exception as e:print str(e)
#    return dict_day

#用户跑付费用户活跃天数分布
def get_dict(template,path):

    f = get_source_data(path)   
    dict_day = {}
    for line in f.readlines():
        try:
            content = line.split(",")
#            except:pass
            uid = content[2][:-1]
            date_this = content[0].replace('-','')
            template_this = content[1]
            day = date_this[6:]
#            except:pass
            if template_this != template:continue#
            
            try:
                temp = []
                temp.append(str(day))
                dict_day[uid].extend(temp)
#                        dict_day[uid]=list(set(dict_day[uid]))
            except:
#                        pass
                temp = []
                temp.append(str(day))
                dict_day[uid] = temp 
        except Exception as e:print str(e)
    return dict_day

def get_area(dict_day):
    all_list = []
    for item in dict_day.items():
        all_list.append(len(dict_day[item[0]]))
    
    all_list = Counter(all_list)
#    return less_1,t_1_100,t_100_1000,t_1000_10000,t_up_10000,all_list
    return all_list

def print_result(a):
    for i in a.items():
        print i[1]
    

if __name__ == '__main__':
    year = 2017
    month = 8
#    dict_game = get_fufei_urs_by_month('ent')

    path = 'fufei_pquan_8.csv'#执行下面hive代码，保存一份付费用户名单fufei_pquan_8.csv'
    dict_res = get_dict('ent',path)
    g = get_area(dict_res)
    print_result(g)


'''
付费用户统一使用付费C券用户
    
#
    select distinct to_date(cost_time) as date,
       case when template_type in ('game', 'mgame', 'gamestar','gamehost') then 'game'
            when template_type='dating' then 'dating'
            when template_type='live' then 'live'
            else 'ent' end as template,
       uid
from cc.coin_cost
where date between 20170701 and 20170801 
and coin_type = 'pquan'
#    
'''

    
    
    
    
    