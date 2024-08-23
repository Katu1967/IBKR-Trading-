#send request to interactive brokers
from ibapi.client import EClient 

#recieve data from interactive brokers 
from ibapi.common import BarData
from ibapi.wrapper import EWrapper

#for creating the charts 
from lightweight_charts import Chart


from threading import Thread
import time, datetime
from ibapi.client import Contract



INITIAL_SYMBOL = "TSM"

DEFAULT_HOST = '127.0.0.1'
DEFAULT_CLIENT_ID = 1
INITIAL_TIMEFRAME = "5 mins"

LIVE_TRADING = False
LIVE_TRADING_PORT = 7496
PAPER_TRADING_PORT = 7497

TRADING_PORT = PAPER_TRADING_PORT

if LIVE_TRADING_PORT:
    TRADING_PORT = LIVE_TRADING_PORT



#this class inherits from Eclient and Ewrapper
class IBClient(EWrapper, EClient):
     
    def __init__(self, host, port, client_id):
        EClient.__init__(self, self) 
        
        self.connect(host, port, client_id)

        thread = Thread(target=self.run)
        thread.start()


    def error(self, req_id, code, msg, misc=""):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print('Error {}: {}'.format(code, msg))

    #printing historical data
    def historicalData(self, reqId, bar):
        print(bar)

    
    def historicalDataEnd(self, reqId: int, start, end):
        print(f"end of data {start} {end}")


#to create chart
def getBarData(symbol, timeframe):

    #creating a new contract 
    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange ='SMART'
    contract.currency = 'USD'
    what_to_show = 'TRADES'

    client.reqHistoricalData(2, contract, '', '30 D', timeframe, what_to_show, True, 2, False, [])

    time.sleep(1)
    
    chart.watermark(symbol)
        

#################################################################################################################################


if __name__ == '__main__':
    client = IBClient(DEFAULT_HOST, 7497, DEFAULT_CLIENT_ID)

    time.sleep(1)

    chart = Chart(toolbox=True, width=1000, inner_width=0.6, inner_height=1)

    getBarData(INITIAL_SYMBOL, INITIAL_TIMEFRAME)
    chart.show(block=True)