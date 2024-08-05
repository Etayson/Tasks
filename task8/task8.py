
#task8

def get_max_gain():
    max_gain, index, laptops_number, spent, total_gain = 0,0,0,0,0  
    lenght = len(gains_array)
    select = [0] * lenght 
    while True:        
        if spent+price_array[index]<=inp_C and laptops_number<inp_N:
            select[index]+=1
            total_gain +=gains_array[index]
            spent += price_array[index]
            laptops_number +=1
            if total_gain>max_gain:
                max_gain = total_gain                    
            index = 0
        else:
            if index<lenght-1:
                total_gain -= select[index] * gains_array[index]
                spent -= select[index] * price_array[index]
                laptops_number -= select[index]
                select[index] = 0
                index +=1
            else:
                break       
    print(f'maximum gain: {max_gain}')
    return max_gain
    
#inputs example   
#inp_N = 15
#inp_C = 4000
#gains_array = [45, 20, 50, 10, 30, 50]
#price_array = [650,400,700,300, 500,700]

inp_laptop_number = input("Enter integer number of laptop N: ") 
inp_N = int(inp_laptop_number)
inp_capital_size = input("Enter integer start capital C: ") 
inp_C = int(inp_capital_size)

while True:
    
    inp_gains_array = input("Enter integer values for gains array ex. 45, 20, 50, 10, 30, 50: ")
    gains_array = [int(x) for x in inp_gains_array.replace(" ", "").split(',')]
    inp_price_array = input("Enter integer values for price array ex. 650,400,700,300, 500,700: ")
    price_array = [int(x) for x in inp_price_array.replace(" ", "").split(',')]
    if len(gains_array) != len(price_array):
        print('Array sizes of gains array and price array must be the same!')
    else:
        break
   
print(f'capital at the end of the summer: {get_max_gain()+inp_C}')