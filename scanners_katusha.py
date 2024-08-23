from ibapi.client import *
from ibapi.wrapper import *

#paper trading port number
port = 7497

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqScannerParameters()
    
    def ScannerParameters(self, xml):
        dir = "C:\\user\\jacksonkatusha\\downloads\\ibjts\\samples\\python\\testbed\\scanners.xlm"
        open(dir, "W").write(xml)
        print("Scanner parameters recieved")

app = TestApp()
app.connect("127.0.0.1", port, 1001)
app.run()
