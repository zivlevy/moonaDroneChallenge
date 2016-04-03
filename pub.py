from __future__ import print_function
 
import time
from random import choice
from random import randrange
 
import zmq
 
if __name__ == "__main__":
    stock_symbols = ['RAX', 'EMC', 'GOOG', 'AAPL', 'RHAT', 'AMZN']
 
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:4999")
    a = 0
    while a<10:
        time.sleep(1)
        a = a + 1
        # pick a random stock symbol
        stock_symbol = choice(stock_symbols)
        # set a random stock price
        stock_price = randrange(1, 100)
 
        # compose the message
        msg = "{0} ${1}".format(stock_symbol, stock_price)
 
        print("Sending Message: {0}".format(msg))
 
        # send the message
        socket.send(msg)
        # Python3 Note: Use the below line and comment
        # the above line out
        # socket.send_string(msg)
