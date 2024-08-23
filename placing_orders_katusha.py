from ibapi.client import *
from ibapi.wrapper import * 
from ibapi.contract import ComboLeg
from ibapi.tag_value import TagValue

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):

        #order info
        # mycontract = Contract()
        # mycontract.symbol = "AAPL,TSLA"
        # mycontract.secType = "BAG"
        # mycontract.exchange = "SMART"
        # mycontract.currency = "USD"

        #FOR COMBO ORDERS
        # leg1 = ComboLeg()
        # leg1.conId = 76792991
        # leg1.ratio = 1
        # leg1.action = "BUY"
        # leg1.exchange = "SMART"

        # leg2 = ComboLeg()
        # leg2.conId = 265598
        # leg2.ratio = 1
        # leg2.action = "SELL"
        # leg2.exchange = "SMART"

        # mycontract.comboLegs = []
        # mycontract.comboLegs.append(leg1)
        # mycontract.comboLegs.append(leg2)

        # myorder = Order()
        # myorder.orderId = orderId
        # myorder.action = "BUY"
        # myorder.orderType = "LMT"
        # myorder.lmtPrice = 80
        # myorder.totalQuantity = 10
        # myorder.tif = "GTC"
        # myorder.smartComboRoutingParams = []
        # myorder.smartComboRoutingParams.append(TagValue('NonGuaranteed', '1'))

        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"


        parent = Order()
        parent.orderId = orderId
        parent.orderType = "LMT"
        parent.lmtPrice = 140
        parent.action = "BUY"
        parent.totalQuantity = 10
        parent.transmit = False


        profit_taker = Order()
        profit_taker.orderId = parent.orderId + 1
        profit_taker.parentId = parent.orderId
        profit_taker.action = "SELL"
        profit_taker.orderType = "LMT"
        profit_taker.lmtPrice = 137
        profit_taker.totalQuantity = 10
        profit_taker.transmit = False

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId
        stop_loss.orderType = "STP"
        stop_loss.auxPrice = 155
        stop_loss.action = "SELL"
        stop_loss.totalQuantity = 10
        stop_loss.transmit = True


        self.placeOrder(parent.orderId, mycontract, parent)
        self.placeOrder(profit_taker.orderId, mycontract, profit_taker)
        self.placeOrder(stop_loss.orderId, mycontract, stop_loss)

    #placing an order
    # def contractDetails(self, reqId: int, contractDetails: ContractDetails):
    #     print(contractDetails.contract)

    #     myorder = Order()
    #     myorder.orderId = reqId
    #     myorder.action = "SELL"
    #     #if no tif is specified then it will use a day order by default 
    #     myorder.tif = "GTC" 
    #     myorder.orderType = "LMT"
    #     myorder.lmtPrice = 144.80
    #     myorder.totalQuantity = 10

    #     self.placeOrder(reqId, contractDetails.contract, myorder)
    #     self.disconnect()

    #gives information on an order once it is placed
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    #provides information on the order after the order is placed
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    #gives a summary of the order, this is the execution details
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

app = TestApp()
app.connect("127.0.0.1", 7497, 0)
app.run()
