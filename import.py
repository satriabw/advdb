# Import important library and constant definition

import pandas as pd
import time

from datetime import datetime


FILE = './data/tick-price-file'

def import_data():
    df = pd.read_csv(FILE, 
                names=['Id', 'SeqNo', 'TradeDate', 'TimeStamp', 'TradePrice', 'TradeSize', 'AskPrice', 'AskSize', 'BidPrice', 'BidSize', 'Type'],
                skiprows=1,
                sep='|')
    df['TradeDateTime'] = df[['TradeDate', 'TimeStamp']].astype(str).apply(lambda x: convert_to_epoch_time(''.join(x)), axis=1)
    df = df[df['TradeDateTime'].notna()]
    
    # convert minute precision to nanosecond precision
    #df["TradeDateTime"] = [str(df["TradeDateTime"][t]) + "000000000" for t in range(len(df))]
    
    lines = []
    for index, row in df.iterrows():
        lines.append('findata' + ',Id=' + str(df['Id']) + ',SeqNo='+str(df['SeqNo'])+',TradeDateTime='+str(df['TradeDateTime'])+',TradePrice='+str(df['TradePrice'])
                     +',TradeSize='+str(df['TradeSize'])+',AskPrice=' +str(df['AskPrice']) +',AskSize='+str(df['AskSize'])+',BidPrice='+str(df['BidPrice']) 
                     + ',BidSize=' + str(df['BidSize'])+ ',Type=' + df['Type'])
    
    with open('./data/chronograf.txt', 'w+') as thefile:
        for item in lines:
            thefile.write("%s\n" % item) 
                     
def convert_to_epoch_time(date_time):
    try:
        date_time= datetime.strptime(date_time.strip().replace("  ", " "), '%m/%d/%Y %H:%M:%S')
    except:
        return None
        
    return str(time.mktime(date_time.timetuple()))

import_data()