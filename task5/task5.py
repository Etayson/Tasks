import random
import math
import time
import sys

#task5

LIMIT = 1*1024*1024 #MB
Cur_tx_id = 1
block ={'size':0, 'fee':0, 'txarr':[]}
Num_tx=100000
csv_file = 'task5.csv'

def generate_CSV_tx(csv_file, Num_tx):
    try:
        with open(csv_file, "w") as f:
            f.write('tx_id,tx_size,tx_fee\n')
            for line in range(Num_tx):
                rnd_sat_per_b = random.randint(4, 390)
                rnd_size = random.randint(248, 6000)
                rnd_fee = rnd_size * rnd_sat_per_b
                f.write(f'{line+1},{rnd_size},{rnd_fee}\n')
    except FileNotFoundError:
        print(f'{csv_file} not found')
    return None

def open_CSV_tx(csv_file):
    try:
        with open(csv_file, mode='r', newline='') as file:
            #in CSV delemiter can be ';' or ',' and we don`t know which one will be in files
            delemiter = ','
            rline = file.readline().strip()
            headers = rline.split(delemiter)
            if len(headers)==1:
                delemiter=';'
                headers = rline.split(delemiter)
                 
            for line in file:            
                fields = line.strip().split(delemiter)            
                if len(fields) == len(headers):               
                    block['size'] += int(fields[1])
                    block['fee'] += int(fields[2])
                    block['txarr'].append((fields[0], int(fields[1]), int(fields[2]))) #format block['txarr'] =[(tx_id, tx_size, tx_fee),...]                   
                else:
                    print(f"lenght of fields  not match to headers lenght: {line}")
                    exit() 
            
    except FileNotFoundError:
        print(f'{csv_file} not found')
        exit() 

if len(sys.argv)!=2:
    print (f'A new file {csv_file} with {Num_tx} txs will be generated and used.')
    generate_CSV_tx(csv_file, Num_tx)
else:
    csv_file = sys.argv[1]
print(f'{csv_file} file is used.')

open_CSV_tx(csv_file)

block['txarr'].sort(reverse = False, key=lambda x: x[2]/x[1]) #array should be sorted by feerate = tx_fee / tx_size
print('Before construction:')
print(f"Size: {block['size']} free: {LIMIT-block['size']} fee: {block['fee']} {len(block['txarr'])}")

MinSize=LIMIT
id_t=0
start = time.time()        
while block['size']>LIMIT:
    diff = block['size']-LIMIT  
    
    for tx in range(0, len(block['txarr'])):
        if block['txarr'][tx][1]<=diff:
            block['size'] -= block['txarr'][tx][1]
            block['fee']  -= block['txarr'][tx][2]            
            del block['txarr'][tx]
            break
        else:
            if block['txarr'][tx][1] - diff<MinSize:
                MinSize = block['txarr'][tx][1]
                id_t = tx
                
    if  block['size']-LIMIT == diff:        
        #print(f'Lowest size nearest to {diff} is {MinSize} at in array at index {id_t}')
        
        block['size'] -= block['txarr'][id_t][1]
        block['fee']  -= block['txarr'][id_t][2]
        #print(f'del {mempool[id_t]}')
        del block['txarr'][id_t]
        break 
     


Construction_time = time.time() - start
print('After construction:')
print(f'Amount of transactions in the block: {len(block['txarr'])}')
print(f'Block Size: {block['size']}b limited to {LIMIT}b free: {LIMIT-block['size']}b')
print(f'The total extracted value: {block['fee']}sat')
print(f'Construction time: {Construction_time}s')
