import sys
import os
import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

print("Python executable:", sys.executable)
print("PYTHONPATH:", os.environ.get('PYTHONPATH', 'Not set'))
print("ibapi module imported successfully!")

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.orderId = None
    
    def nextValidId(self, orderId):
        self.orderId = orderId
        print(f"Next valid order ID: {self.orderId}")
    
    def nextId(self):
        if self.orderId is None:
            raise ValueError("orderId is not set. nextValidId has not been called.")
        self.orderId += 1
        return self.orderId

    def error(self, reqId, errorCode, errorString, advancedOrderReject):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}")

    def contractDetails(self, reqId, contractDetails):
        attrs = vars(contractDetails)
        print("\n".join(f"{name}: {value}" for name, value in attrs.items()))
    
    def contractDetailsEnd(self, reqId):
        print("End of contract details")
        self.disconnect()

app = TestApp()

# Ensure TWS or IB Gateway is running on the specified host and port
host = "127.0.0.1"
port = 7497
clientId = 0
print(f"Connecting to TWS on {host}:{port} with clientId {clientId}...")
app.connect(host, port, clientId)
print("Connected to TWS")

print("Starting the app...")
app_thread = threading.Thread(target=app.run)
app_thread.start()
print("App started, waiting for contract details...")

# Wait until nextValidId is called
while app.orderId is None:
    print("Waiting for next valid order ID...")
    time.sleep(1)

# Define the contract
mycontract = Contract()
# Option contract
mycontract.symbol = "SPX"
mycontract.secType = "OPT"
mycontract.currency = "USD"
mycontract.exchange = "SMART"
mycontract.lastTradeDateOrContractMonth = "202412"
mycontract.right = "P"
mycontract.tradingClass = "SPXW"
mycontract.strike = 5300

# Request contract details
try:
    app.reqContractDetails(app.nextId(), mycontract)
    print("Requested contract details")
except Exception as e:
    print(f"Error requesting contract details: {e}")

# Allow some time to receive data
time.sleep(5)
print("Disconnecting from TWS...")
app.disconnect()
print("Disconnected from TWS")

# Ensure the app thread finishes
app_thread.join()
print("App thread finished")
