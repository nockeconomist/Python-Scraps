# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:32:09 2016

@author: NockEconomist
"""

import pandas as pd
import io
import requests
import matplotlib.pyplot as plt


#%%        
class cdid(object):
    
    def __init__(self, url):
        self.url = url
        
    def cdid_dataset(self):
    
        s=requests.get(self.url).text
    
        df = {}    
        
        df['full'] = pd.read_csv(io.StringIO(s), low_memory=False)
        
        columns = [x for x in df['full'].columns]
        
        df['meta'] = cdid_dict = {}
        
        for x in columns:
            y = df['full'].at[0,x]
            cdid_dict[y] = x
            df['full']= df['full'].rename(columns={x:y})
        df['full'] = df['full'][6:]
        df['full']['year'] = df['full']['CDID'].str[0:5].astype('int')
        
     
        
        df['q'] = pd.DataFrame()
        df['q'] = df['full'][df['full']['CDID'].str.len() == 7]
        
        df['m'] = pd.DataFrame()
        df['m'] = df['full'][df['full']['CDID'].str.len() == 8]
           
        df['a'] = pd.DataFrame()
        df['a'] = df['full'][df['full']['CDID'].str.len() == 4]
        
        return df


#%%
def cdid_chart(dataset,a, *args, **kwargs):
    
    start = kwargs.get('start', None)
    end = kwargs.get('end', None)    
    series_2 = kwargs.get('series_2', None)  
    freq = kwargs.get('freq', None)  
    
    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    
    if freq==None:
        freq_var = 'q'
    if freq=='q':
        freq_var = 'q'
    if freq=='m':
        freq_var = 'm'
    if freq=='a':
        freq_var = 'a'
    
    if start==None:
        x = dataset[freq_var].index
        plt.xticks(dataset[freq_var].index[0::8]-0.5,dataset[freq_var]['CDID'][0::8].str[0:5])
        plt.xlim(min(dataset[freq_var].index)-0.5, max(dataset[freq_var].index)+0.5)
        
        y = dataset[freq_var][a]
        
    if start!=None:
        dataset[freq_var]['index']=dataset[freq_var].index
        x = dataset[freq_var]['index'][dataset[freq_var]['CDID'].str[0:5].astype(float)>=start]
        x1 = dataset[freq_var]['CDID'][dataset[freq_var]['CDID'].str[0:5].astype(float)>=start]
        plt.xticks(x[0::12]-0.5,x1[0::12].str[0:5])
        plt.xlim(min(x1.index)-0.5, max(x1.index)+0.5)
        y = dataset[freq_var][a][dataset[freq_var]['CDID'].str[0:5].astype(float)>=start]
        
    ax.plot(x,y, 'red', linewidth=2.0, label = dataset['meta'][a])
        
    if series_2==None:
    
        plt.title(dataset['meta'][a])
        ax.plot(x,y, 'red', linewidth=2.0)
    
    if series_2!=None:
        y2 = dataset[freq_var][series_2][dataset[freq_var]['CDID'].str[0:5].astype(float)>=start]
        ax.plot(x,y2, 'blue', linewidth=2.0, label=dataset['meta'][series_2])     

        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True)
        

    
    
    plt.show()
    
#%%
###################################################
#                                                 #
#                                                 #
#           Profitability Example                 #
#                                                 #
#                                                 #
###################################################

prof_data = cdid("https://www.ons.gov.uk/file?uri=/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies/current/prof.csv")
prof = prof_data.cdid_dataset()
    
cdid_chart(prof,'LRWW')
cdid_chart(prof,'LRYQ', start=2005)
cdid_chart(prof,'LRYC')
cdid_chart(prof,'LRXP')

cdid_chart(prof,'LRYQ', series_2='LRYC', start=1997)

#%%
###################################################
#                                                 #
#                                                 #
#      Labour Market Stats Example                #
#                                                 #
#                                                 #
###################################################

lms_data = cdid("https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/labourmarketstatistics/current/lms.csv")
lms = lms_data.cdid_dataset()

cdid_chart(lms,'YBUV', start=1994)

cdid_chart(lms,'MGSX', start=1994)
cdid_chart(lms,'MGSX', series_2 = 'A493', start=2000)

cdid_chart(lms,'DPAJ', series_2 = 'MGSX', start=1973)
cdid_chart(lms,'DPAJ', series_2 = 'MGSX', start=2013, freq='m')
cdid_chart(lms,'KAI9',  series_2 = 'MGSX', freq='m', start=2001)


#%%
###################################################
#                                                 #
#                                                 #
#      Labour Productivity Example                #
#                                                 #
#                                                 #
###################################################


prod_data = cdid("https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/labourproductivity/datasets/labourproductivity/current/prdy.csv")
prod = prod_data.cdid_dataset()

cdid_chart(prod,'LZVB',start=1970)
cdid_chart(prod,'DMWN',start=1992)
cdid_chart(lms,'A2FC',start=2000, freq='m')


#%%
###################################################
#                                                 #
#                                                 #
#                 Blue Book                       #
#                                                 #
#                                                 #
###################################################

bb_data = cdid("http://www.ons.gov.uk/file?uri=/economy/grossdomesticproductgdp/datasets/bluebook/current/bb.csv")
bb = bb_data.cdid_dataset()

cdid_chart(bb, 'ABMI', start=1950, freq='a')




