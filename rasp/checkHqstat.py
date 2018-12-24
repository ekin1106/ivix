def getHqStat():
    import requests, re
    state = set(['-1','0','2'])

    url = 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011&token=44c9d251add88e27b65ed86506f6e5da&cb=callback020420580954748035&callback=callback020420580954748035&_=1541401708403'
    session = requests.session()
    resp = session.get(url)
    resp.encoding = 'utf-8'
    p1 = re.compile(r'[[](.*?)[]]', re.S)
    result = re.findall(p1, resp.text)[1].split(',')[44].strip('"')
    
    if result in state:
        print('today is tradeday')
        with open('/home/pi/Desktop/ivix/gethqstat.txt', 'w') as f:
            f.write('tradeday')
            f.close()
    else:
        print('today is not tradeday')
        with open('/home/pi/Desktop/ivix/gethqstat.txt', 'w') as f:
            f.write('not_tday')
            f.close()
    print(result)


def loadhqstat():
    with open('/home/pi/Desktop/ivix/gethqstat.txt') as f:
        stat = f.readline()
        f.close()
    return stat

if __name__ == '__main__':
    getHqStat()
