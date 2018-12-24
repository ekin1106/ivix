import requests
from requests_html import HTMLSession
import re
import csv
import datetime
import numpy as np
import pandas as pd


def test_1():
    url = 'http://quote.eastmoney.com/center/gridlist.html#options_sh50etf_all'
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    odd = r.html.find('.odd .listview-col-Name a')
    even = r.html.find('.even .listview-col-Name a')
    c =  r.html.find('.even .listview-col-Name a')
    # for i,n,m in zip(odd,even,c):
    #     print(i.text,'\n',n.text,'\n',m.text)

def ivixDATA():
    #创建CSV文件
    csvfile = open('options.csv', 'a', newline='',encoding='GBK')
    writer = csv.writer(csvfile)
    # writer.writerow(('DATE','CODE','SEC_NAME','EXE_MODE','EXE_PRICE','EXE_ENDDATE','CLOSE'))
    url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240565871612842938_1536046239791&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(Code)&sr=1&p=1&ps=20&_=1536046239981'
    url_2 = [
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451475&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=1&ps=20&_=1536051451490',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451475&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=2&ps=20&_=1536051451495',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=3&ps=20&_=1536051451500',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=4&ps=20&_=1536051451503',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=5&ps=20&_=1536051451506',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=6&ps=20&_=1536051451510',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=7&ps=20&_=1536051451512'
    ]
    for u in url_2:
        session = HTMLSession()
        r = session.get(u)
        a = r.html.text
        session.close()
        p1 = re.compile(r'[[](.*?)[]]', re.S) #获取括号内的内容
        result = re.findall(p1,a)[0]     #期权结果第一页
        resultList=result.split('","')

        tup = tuple(resultList[0].strip('"').split(','))
        #获取当前日期
        date = datetime.datetime.now()
        year =str(int(date.strftime('%Y')))  #去0
        month =str(int(date.strftime('%m')))
        day =str(int(date.strftime('%d')))
        formateDate = year+'/'+month+'/'+day

        # ss=(('10001233','50ETF购9月2750','认购','0.0048','0.0018','60.00%','18206','753105'))
        #将结果列表转为元组
        for i in resultList:
            tup = i.strip('"').split(',')
            if '50ETF购' in tup[2]:
                EXE_MODE = '认购'
            else:
                EXE_MODE = '认沽'
            delta = datetime.timedelta(days=int(tup[10]))
            endDate = date + delta
            endYear = str(int(endDate.strftime('%Y')))
            endMonth = str(int(endDate.strftime('%m')))
            endDay = str(int(endDate.strftime('%d')))
            FormateEndDate = endYear+'/'+endMonth+'/'+endDay
            test_1=[formateDate,tup[2],EXE_MODE,tup[9],FormateEndDate+' 0:00',tup[3]]  #增加日期,后:CODE,合约名称,增加认购认沽,行权价,到期时间,收盘价
            test_2=tuple(test_1)
            ss=((test_2))

            writer.writerow(ss)
    csvfile.close()

def getTradeDay():
    csvfile = open('tradeday.csv', 'a', newline='')
    writer = csv.writer(csvfile)
    # writer.writerow(('DateTime'))
    date = datetime.datetime.now()
    year =str(int(date.strftime('%Y')))
    month =str(int(date.strftime('%m')))
    day =str(int(date.strftime('%d')))
    formateDate = [year + '/' + month + '/' + day]
    f = tuple(formateDate)
    writer.writerow((formateDate))
    csvfile.close()

def checkCsv():
    shibor_rate = pd.read_csv('shibor.csv', index_col=0, encoding='GBK')
    options_data = pd.read_csv('options.csv', index_col=0, encoding='GBK')
    tradeday = pd.read_csv('tradeday.csv', encoding='GBK')
    true_ivix = pd.read_csv('tradeday.csv', encoding='GBK')
    ivix = []
    for day in tradeday['DateTime']:
        options = options_data.loc[day,:]
        print(options)
        # vixDate = datetime.datetime.strptime(day, '%Y/%m/%d')
        # optionsExpDate = list(pd.Series(options.EXE_ENDDATE.values.ravel()).unique())
        # optionsExpDate = [datetime.datetime.strptime(i, '%Y/%m/%d %H:%M') for i in optionsExpDate]
        # near = min(optionsExpDate)
        # optionsExpDate.remove(near)
        # if near.day - vixDate.day < 1:
        #     near = min(optionsExpDate)
        #     optionsExpDate.remove(near)
        # nt = min(optionsExpDate)
        # print(near,nt)
        # return near, nt

def shibor():
    #shibor获取
    date = datetime.datetime.now()
    year =str(int(date.strftime('%Y')))
    month =str(int(date.strftime('%m')))
    day =str(int(date.strftime('%d')))
    formatDate = date.strftime('%Y-%m-%d') #获取时间，用于判断网页上的数据是否是最新的
    print(formatDate)



    csvfile = open('shibor.csv', 'a') #newline=''
    writer = csv.writer(csvfile)
    url = 'http://www.shibor.org/shibor/web/html/shibor.html'
    session = HTMLSession()
    r = session.get(url)

    dateDATA = r.html.find('.infoTitleW',first=True)
    shiborDate = dateDATA.text.split(' ')[0]
    if formatDate == shiborDate:
        changeDate = year+'-'+month+'-'+day
        sh = r.html.xpath('/html/body/html', first=True)
        time = r.html.find('.shiborquxian tr')
        dataList =[]
        dataList.append(changeDate)
        for data in time[0:8]:
            shiborData = data.find('td')
            dataList.append(shiborData[2].text)
        dataList = tuple(dataList)
        writer.writerow((dataList))
        csvfile.close()
        print(dataList)
    else:
        print('日期不符，请稍晚再获取')

def optionDATA():
    #创建CSV文件
    csvfile = open('optionsDATA.csv', 'a', newline='')
    writer = csv.writer(csvfile)
    #writer.writerow(('DATE','CODE','SEC_NAME','EXE_MODE','EXE_PRICE','涨跌额','涨跌幅','成交量','成交额(万)','持仓量','行权价','EXE_ENDDATE','持仓量','日增','昨收','今开'))
    url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240565871612842938_1536046239791&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(Code)&sr=1&p=1&ps=20&_=1536046239981'
    url_2 = [
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451475&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=1&ps=20&_=1536051451490',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451475&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=2&ps=20&_=1536051451495',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=3&ps=20&_=1536051451500',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=4&ps=20&_=1536051451503',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=5&ps=20&_=1536051451506',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=6&ps=20&_=1536051451510',
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery1124020432924300003052_1536051451481&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOL&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C.OP.SO.510050.SH&st=(ExerciseDateRemain)&sr=1&p=7&ps=20&_=1536051451512'
    ]
    for u in url_2:
        session = HTMLSession()
        r = session.get(u)
        a = r.html.text
        session.close()
        p1 = re.compile(r'[[](.*?)[]]', re.S) #获取括号内的内容
        result = re.findall(p1,a)[0]     #期权结果第一页
        resultList=result.split('","')

        tup = tuple(resultList[0].strip('"').split(','))
        #获取当前日期
        date = datetime.datetime.now()
        year =str(int(date.strftime('%Y')))  #去0
        month =str(int(date.strftime('%m')))
        day =str(int(date.strftime('%d')))
        formateDate = year+'/'+month+'/'+day

        # ss=(('10001233','50ETF购9月2750','认购','0.0048','0.0018','60.00%','18206','753105'))
        #将结果列表转为元组
        for i in resultList:
            tup = i.strip('"').split(',')
            if '50ETF购' in tup[2]:
                EXE_MODE = '认购'
            else:
                EXE_MODE = '认沽'
            delta = datetime.timedelta(days=int(tup[10]))
            endDate = date + delta
            endYear = str(int(endDate.strftime('%Y')))
            endMonth = str(int(endDate.strftime('%m')))
            endDay = str(int(endDate.strftime('%d')))
            FormateEndDate = endYear+'/'+endMonth+'/'+endDay
            test_1 = [formateDate, tup[1], tup[2],EXE_MODE,tup[3],tup[4],tup[5],tup[6],tup[7],tup[8],tup[9],FormateEndDate + ' 0:00',tup[11],tup[12],tup[13]] 
            test_2=tuple(test_1)
            ss=((test_2))

            writer.writerow(ss)
    csvfile.close()

if __name__ == '__main__':
    ivixDATA()
    getTradeDay()
    shibor()
    # checkCsv()
    optionDATA()

#/html/body/html:form/div/table/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[3]