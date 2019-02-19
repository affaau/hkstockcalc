'''Calculate profit/loss & cost for HK stock exchange
    
ref:https://docs.python.org/2/howto/argparse.html
'''
import argparse

# constants
HKFX_TRADING_FEE = 0.005   # percentage
PER_LOT_CHARGE = 5.0       # HKD
BROKEAGE_FEE = 0.25        # percentage
STAMP_DUTY = 0.1           # percentage
TRANSACTION_LEVY = 0.003   # percentage

# help functions
def buy():
    basic_principle = buy_price*per_lot*lot
    cost = trading_fee(basic_principle) +\
           deposit_transction_charge() +\
           brokeage_fee(basic_principle) +\
           stamp_duty(basic_principle) +\
           transaction_levy(basic_principle)
    # (investment amount, cost)
    return (basic_principle + cost, cost)

def buy_sell():
    invest_amt, cost_buy = buy()
    gross_gain = sell_price*per_lot*lot
    cost_sell =\
           trading_fee(gross_gain) +\
           brokeage_fee(gross_gain) +\
           stamp_duty(gross_gain) +\
           transaction_levy(gross_gain)
    total_cost = cost_buy + cost_sell
    # (invest amount, net gain, total cost, take back amount)
    return (invest_amt, gross_gain - invest_amt - cost_sell, total_cost, gross_gain - cost_sell)

def code_name():
    '''Return code name of the given stock code
    **Future to search for nore online info**'''
    return args.code

def brokeage_fee(amt):
    '''Min. is $100'''
    charge = amt*BROKEAGE_FEE/100.0
    if charge > 100.0:
        return charge
    return 100.0
    
def stamp_duty(amt):
    '''flat rate'''
    return amt*STAMP_DUTY/100.0

def transaction_levy(amt):
    '''flat rate'''
    return amt*TRANSACTION_LEVY/100.0
    
def trading_fee(amt):
    '''flat rate'''
    return amt*HKFX_TRADING_FEE/100.0

def deposit_transction_charge():
    '''Charge according to no. of lots
    Min. $30, Max. $200'''
    charge = lot*PER_LOT_CHARGE
    
    if  30.00 <= charge <= 200.0:
        return charge
        
    if charge > 200.0:
        return 200.0
        
    if charge < 30.0:
        return 30.0

def show(result):
    '''Present transaction result'''
    print("Stock: ", code_name())
    print("Action: ", mode)
    print("Total share: {:.0f} units".format(per_lot*lot))
    if mode=="SELL":
        invest_amt, gain, cost, cash_in = result
        print("buy  : ${}".format(buy_price))
        print("sell : ${}".format(sell_price))
        print("Total transaction cost: ${:.2f} ({:.2f}%)".format(cost, cost/invest_amt*100))
        print("Bank debit (withdraw): ${:.0f}".format(invest_amt))
        print("Bank credit (deposit): ${:.0f}".format(cash_in))
        print("Net gain: ${:.0f} ({:.2f}%)".format(gain, gain/invest_amt*100))
    else:
        invest_amt, cost = result
        print("buy  : ${}".format(buy_price))
        print("Transaction cost: ${:.2f} ({:.2f}%)".format(cost, cost/invest_amt*100))
        print("Bank debit (withdraw): ${:.0f}".format(invest_amt))
 
# initialize
examples = '''=======================
Examples
To check cost and amount to buy in stock:
    $> python HKStockCalc.py --buy --code 0005 "68.4, 400, 2"
    $> python HKStockCalc.py -b -c 0005 "68.4, 400, 2"

To check profit/loss of selling stock:
    $> python HKStockCalc.py --sell --code 0005 "68.4, 68.05, 400, 2"
    $> python HKStockCalc.py -s -c 0005 "68.4, 68.05, 400, 2"
=======================
'''
parser = argparse.ArgumentParser(
            description="Calculator for transaction cost and result for HK Stock market",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=examples)
# positional arguments
parser.add_argument("data", help='a list of key data embraced with quotes,\nformat: "buy price, [sell price,] share per lot, number of lot"')

# optional arguments
group = parser.add_mutually_exclusive_group()  # only work for optional arguments
group.add_argument('-b', "--buy", help="BUY mode", action="store_true")
group.add_argument('-s', "--sell", help="SELL mode", action="store_true")
parser.add_argument('-c', '--code', help="a reference HK stock code", default="Anonymous")

# prepare data
args = parser.parse_args()
try:
    data = [float(e) for e in args.data.split(sep=',')]
except ValueError as e:
    print("Error: ", e)

# main
if args.sell:
    if len(data)!=4:
        raise("Error: 4 data is expected as input for SELL mode!")
    else:
        buy_price, sell_price, per_lot, lot = data
        mode = "SELL"
        show(buy_sell())
else:
    if len(data)!=3:
        raise("Error: 3 data is expected as input for BUY mode!")
    else:
        buy_price, per_lot, lot = data
        mode = "BUY"
        show(buy())

