
#task1

Order_book=[[],[]]

def print_book():
    print('Order book sell orders:')
    for order in Order_book[False]:
        print(order)
    print('Order book buy orders:')
    for order in Order_book[True]:
        print(order)

def update_user_balace(user_id, base_balance, quote_base_balance):     
    change1 = {'user_id':user_id, 'value':base_balance, 'currency':'UAH'}
    change2 = {'user_id':user_id, 'value':quote_base_balance, 'currency':'USD'}
    print(f'BalanceChange:{change1}')
    print(f'BalanceChange:{change2}')    
 
def check_match(order):
    sign = -1 if order['side']==False else 1
    signInv = -1 * sign
    while order['amount']>0 and len(Order_book[1-order['side']])>0:                                           
        check_order = Order_book[1-order['side']][0]
        if (order['price'] >check_order['price'] and order['side']==False) or (order['price'] <check_order['price'] and order['side']==True):                
            break
        else:
            rest_amount = order['amount'] - check_order['amount']                
            if  rest_amount>0:  
                #new order amount>amount in orderbook
                update_user_balace(order['user_id'], sign * check_order['amount'], signInv * check_order['amount'] * check_order['price'])
                update_user_balace(check_order['user_id'], signInv * check_order['amount'], sign * check_order['amount'] * check_order['price'])
                order['amount'] -= check_order['amount']                                 
                del Order_book[1-order['side']][0]                        
            elif rest_amount<0:
                #new order amount<amount in orderbook
                update_user_balace(order['user_id'], sign * order['amount'], signInv * order['amount'] * check_order['price'])
                update_user_balace(check_order['user_id'], signInv * order['amount'], sign * order['amount'] * check_order['price'])
                check_order['amount'] -= order['amount']
                order['amount'] = 0                  
            else:
                #new order amount=amount in orderbook                      
                update_user_balace(order['user_id'], sign * order['amount'], signInv * order['amount'] * check_order['price'])
                update_user_balace(check_order['user_id'], signInv * order['amount'], sign * order['amount'] * check_order['price'])
                order['amount'] = 0
                del Order_book[1-order['side']][0]
    return order
        
def add_new_ordr(order):    
    new_order = check_match(order)
    if new_order['amount']>0:        
        Order_book[order['side']].append({'user_id':new_order['user_id'], 'amount':new_order['amount'], 'price':new_order['price']})            
        Order_book[order['side']].sort(key = lambda x: x['price'], reverse = order['side']) #Sell orders for people who want to sell UAH. This list is sorted by price from the lowest price to the highest

while True: 
    #ex. for sell {1,100,3,False} 
    #ex. for buy  {2,100,2,True} 
    inp_order = input("Enter order {user_id int64, amount int64, price int64, side bool}: ")    
    order = inp_order.replace("{", "").replace("}", "").split(',')
    add_new_ordr({'user_id':int(order[0]), 'amount':int(order[1]), 'price':int(order[2]), 'side':order[3]== 'True'})
    print_book()
