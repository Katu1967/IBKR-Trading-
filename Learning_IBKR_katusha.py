from ibapi.client import *
from ibapi.common import TickerId
from ibapi.contract import ContractDetails
from ibapi.wrapper import *
import datetime
import time 
import threading 
from ibapi.ticktype import TickTypeEnum

# class to combine the ewrapper and eclient modules 
class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    #to receive our order ID's
    def nextValidId(self, orderID):
        self.orderID = orderID

    #incriments the order ID to the next ID
    def nextId(self):
        self.orderID +=1 
        return self.orderID
    
    #return the current time in milliseconds or EPOCH TIME
    def currentTime(self, time):
        print(time)


    #error function will automatically return errors that happen in trader workstation 
    def error(self, reqId, errorCode, errorString, advancedOrderReject):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}")

    
    #contract details is a class that contains contract information in the form of a dictionary
    def contractDetails(self, reqId, contractDetails):
        attrs = vars(contractDetails)
        #print("\n" .join(f"{name}: {value}" for name, value in attrs.items()))
        print(contractDetails.contract)

    def contractDetailsEnd(self, reqId):
        print("End of contract details")
        self.disconnect()

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}")
    
    def tickSize(self, reqId, tickType, size):
        print(f"reqId: {reqId}, tickType: {TickTypeEnum.toStr(tickType)}, size: {size}")

        
    

# MAIN TESTING BELOW

app = TestApp()

#connecting our program to trader workstation 
#(host, port, client id) format
app.connect("127.0.0.1", 7497, 0)

threading.Thread(target=app.run).start()
time.sleep(1)


#testing the orderID's
#for i in range(0,5):
    #print(app.nextId())
   # app.reqCurrentTime()

mycontract = Contract()

#requesting stock contract details "STK" -> means stock "OPT"-> options, FUT-> futures 
#for stocks 
mycontract.symbol = "AAPL"
mycontract.secType = "STK"
mycontract.currency = "USD"
mycontract.exchange = "SMART"
mycontract.primaryExchange = "NASDAQ"


#this is for streaming market data 

app.reqMarketDataType(3)
app.reqMktData(app.nextId(), mycontract, "232", False, False, [])


#futures you cannot use SMART exchange for futures 
# mycontract.symbol = "ES"
# mycontract.secType = "FUT"
# mycontract.currency = "USD"
# mycontract.exchange = "CME"
# mycontract.lastTradeDateOrContractMonth = 202412

#options
# mycontract.symbol = "SPX"
# mycontract.secType = "OPT"
# mycontract.currency = "USD"
# mycontract.exchange = "SMART"
# mycontract.lastTradeDateOrContractMonth = 202412
# mycontract.right = "p"
# mycontract.tradingClass = "SPXW"
# mycontract.strike = 5300




#app.reqContractDetails(app.nextId(), mycontract)



        
