# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:19:48 2017

@author: azfv1n8
"""

import json
import urllib2
import pandas as pd
import datetime as dt
import cPickle as pkl


def build_points_url(min_date, max_date, api_keypath='settings/apikey.pkl', model='ecm-ensemble-dk15', param='temperature-statistics', lat=56.15395, lon=10.203883):
    
    with open(api_keypath, 'r') as f:
        api_key = pkl.load(f)
    base = 'https://secure.dmi.dk/GWS/model/points?cookie='
    url = ''.join([base, api_key,
                     '&model=', model,
                     '&param=', param,
                     '&lat=', str(lat),
                     '&lon=', str(lon),
                     '&mindate=', dt.datetime.strftime(min_date, '%Y%m%d%H'),
                     '&maxdate=', dt.datetime.strftime(max_date, '%Y%m%d%H'),
                     '&choose=all'])
                     
    return url


def forecast_to_flatdf(url):
    """ Takes url as a string """
    
    dic = json.load(urllib2.urlopen(url))
    
    list_of_flat_dics = []
    for d in dic['data']:
        flat_dic = {k:d['p'][0][k] for k in d['p'][0].keys()}
        flat_dic['date'] = d['date']
    
        list_of_flat_dics.append(flat_dic)
    
    
    df = pd.DataFrame(list_of_flat_dics)
    dt_timestamps = [dt.datetime.strptime(str(d), '%Y%m%d%H') for d in df['date']]
    df.index = dt_timestamps
    
    return df