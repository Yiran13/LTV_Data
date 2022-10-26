# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:23:44 2022

@author: apple
"""
# preparation
import requests
import pandas as pd
import numpy as np
import time
import datetime
from bs4 import BeautifulSoup


# Parser
def getHTMLText(url):
    try:
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70'}
        html = requests.get(url, headers = header)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.content, 'html.parser')
        MarginData_str = soup.prettify()
        MarginData_list = MarginData_str.split()
        return MarginData_list
    except:
        return 'Something goes wrong'


#  Collect the data
def getStockTotalMarginVolume():     #前一交易日的转融通数据
    url_for_parsering = 'http://www.csf.com.cn/IAutoDisclosure/js/margin' + (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d') + '.js'
    MarginData_list = getHTMLText(url_for_parsering)
 
    MarginData_df = pd.DataFrame(columns = ['se_code', 'se_name','margin_vol'])    #若margin_vol是'-'，则当日无该只股票融券交易
    for i in MarginData_list:    
        for num_1 in range(10):
            se_1 = 'zrqjyhzdata'+str(num_1)+'[1]'
            if i.find(se_1) != -1:            
                MarginData_df = MarginData_df.append({'se_code':i[17:-2], 
                             'se_name':MarginData_list[MarginData_list.index(i)+1][17:-2],
                             'margin_vol':MarginData_list[MarginData_list.index(i)+3][17:-2]},ignore_index = True)
        for num_2 in range(10,100):
           se_1 = 'zrqjyhzdata'+str(num_2)+'[1]'
           if i.find(se_1) != -1:            
               MarginData_df = MarginData_df.append({'se_code':i[18:-2], 
                             'se_name':MarginData_list[MarginData_list.index(i)+1][18:-2],
                             'margin_vol':MarginData_list[MarginData_list.index(i)+3][18:-2]},ignore_index = True)
        for num_3 in range(100,1000):
            se_1 = 'zrqjyhzdata'+str(num_3)+'[1]'
            if i.find(se_1) != -1:            
                MarginData_df = MarginData_df.append({'se_code':i[19:-2], 
                             'se_name':MarginData_list[MarginData_list.index(i)+1][19:-2],
                             'margin_vol':MarginData_list[MarginData_list.index(i)+3][19:-2]},ignore_index = True)
        for num_4 in range(1000,3000):
            se_1 = 'zrqjyhzdata'+str(num_4)+'[1]'
            if i.find(se_1) != -1:            
                MarginData_df = MarginData_df.append({'se_code':i[20:-2], 
                             'se_name':MarginData_list[MarginData_list.index(i)+1][20:-2],
                             'margin_vol':MarginData_list[MarginData_list.index(i)+3][20:-2]},ignore_index = True)
    
    MarginData_df = MarginData_df.drop(MarginData_df[(MarginData_df.margin_vol == '-')].index)    #删去当日无融券交易的股票

    return MarginData_df

if __name__ == '__main__':
	MarginData_df = getStockTotalMarginVolume()                
      

#导出为csv文件
outputpath = 'C:/Users/apple/Desktop/证金每日按股票总融通数量_' + str((datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')) + '.csv'
MarginData_df.to_csv(outputpath, index=False, header=['se_code','se_name','margin_vol'], encoding='utf_8_sig')



