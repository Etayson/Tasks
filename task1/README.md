Usage: python task1.py  
Note:  
Order format: {user_id int64, amount int64, price int64, side bool}  
Example:  
for sell {1,100,3,False}    
for buy {2,100,2,True}  
If the order amount is less or equal to the order amount in the orderbook, then the order is executed in O(1), otherwise for O(n) were n = amount_in_the_orderbook / amount  
