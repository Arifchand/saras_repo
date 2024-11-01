# package import statement
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect
import pyotp 
from logzero import logger
import pandas as pd

#import smartapi.smartExceptions(for smartExceptions)

#create object of call

token = '76F3AXOS25UKUDHNRVRQJE3OAI'
myotp= pyotp.TOTP(token).now()
print(myotp)
#login api call

obj=SmartConnect(api_key="5WVLHRQB")
data = obj.generateSession("P51657588","1995",pyotp.TOTP(token).now())
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
print(userProfile)

refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()
# logger.info(f"Feed-Token :{feedToken}")
res = obj.getProfile(refreshToken)
# logger.info(f"Get Profile: {res}")
obj.generateToken(refreshToken)
res=res['data']['exchanges']

orderparams = {
    "variety": "NORMAL",
    "tradingsymbol": "SBIN-EQ",
    "symboltoken": "3045",
    "transactiontype": "BUY",
    "exchange": "NSE",
    "ordertype": "LIMIT",
    "producttype": "DELIVERY",
    "duration": "DAY",
    "price": "19500",
    "squareoff": "0",
    "stoploss": "0",
    "quantity": "1"
}

# Method 1: Place an order and return the order ID
orderid = obj.placeOrder(orderparams)
logger.info(f"PlaceOrder : {orderid}")
# Method 2: Place an order and return the full response
response = obj.placeOrderFullResponse(orderparams)
logger.info(f"PlaceOrder : {response}")

pos=obj.position()
logger.info(f"Position : {pos}")

#holdings=obj.holding()
#logger.info(f"Holdings : {holdings}")