import requests
import json
import pandas as pd
from checkHqstat import loadhqstat
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)

def getAll():
    for pa in range(1, 44):
        url = 'http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=tdate&sr=1&p={}'.format(pa)+'&ps=50&js=var%20IPNoxhoO={pages:(tp),data:%20(x)}&type=RZRQ_LSTOTAL_NJ&mk_time=1&rt=51328540'
        session = requests.session()
        resp = session.get(url)
        resp.encoding = 'utf-8'
        jsonResult = resp.text.split('=')[1].replace('pages','"pages"').replace('data', '"data"')
        jsonLoad = json.loads(jsonResult)
        #     print(jsonLoad)
        for jl in jsonLoad['data']:
            save_data = pd.DataFrame([[
                jl['tdate'].split('T')[0], jl['close'], jl['zdf'],
                jl['rzye'], jl['rzyezb'], jl['rzmre'], jl['rzche'],
                jl['rzjmre'], jl['rqye'], jl['rqyl'], jl['rqmcl'], jl['rqchl'],
                jl['rqjmcl'], jl['rzrqye'], jl['rzrqyecz']
            ]])
            print(jl['tdate'].split('T')[0])
            save_data.to_csv('/home/pi/Desktop/ivix/rzrq.csv', mode='a', header=False, index=None)


def getToday():
    url = 'http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=tdate&sr=-1&p=1&ps=50&js=var%20OeDvEAhD={pages:(tp),data:%20(x)}&type=RZRQ_LSTOTAL_NJ&mk_time=1&rt=51331149'
    session = requests.session()
    resp = session.get(url)
    #     resp.encoding = 'utf-8'
    jsonResult = resp.text.split('=')[1].replace('pages', '"pages"').replace(
        'data', '"data"')
    jsonLoad = json.loads(jsonResult)
    print(jsonLoad['data'][0])
    jl = jsonLoad['data'][0]
    save_data = pd.DataFrame([[
        jl['tdate'].split('T')[0], jl['close'], jl['zdf'], jl['rzye'],
        jl['rzyezb'], jl['rzmre'], jl['rzche'], jl['rzjmre'], jl['rqye'],
        jl['rqyl'], jl['rqmcl'], jl['rqchl'], jl['rqjmcl'], jl['rzrqye'],
        jl['rzrqyecz']
    ]])
    print(jl['tdate'].split('T')[0])
    save_data.to_csv('/home/pi/Desktop/ivix/rzrq.csv', mode='a', header=False, index=None)
    print('SAVE DONE')

#getAll()
if __name__ == '__main__':
    load_check = loadhqstat()
    print('start')
    print(str(load_check))
    if str(load_check) == 'tradeday':
        getToday()
        GPIO.output(37,GPIO.HIGH)
        time.sleep(1)
        GPIO.cleanup()
        print('done')
    else:
        print('not TradeDay')

