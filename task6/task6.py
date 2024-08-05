import requests
import time
import sys

#task6

timeout_s = 2

def get_tx(tx):
    try:
        url = f'https://mempool.space/api/tx/{tx}';
        r = requests.get(url);
        txinfo = r.json();
       
        return txinfo
    except requests.exceptions.RequestException as e:
        print(f"error {str(e)}")
        return ""

def get_outspend(tx, vout):
    try:
        url = f'https://mempool.space/api/tx/{tx}/outspend/{vout}';
        r = requests.get(url);
        txinfo = r.json();
       
        return txinfo
    except requests.exceptions.RequestException as e:
        print(f"error {str(e)}")
        return ""
        
def filtr(trans):               
    if len(trans['vin'])==1 and len(trans['vout'])==2:
        return True
    else:
        return False
    
        
def get_longest_utxo(txid, previoustx):
    Stack=[]
    quit = False
    number_steps=0
    maxNumerOfSteps=0
    index=0
    isNext=True
    rest = 1
    while not quit: 
        if  rest>0:   
            trans = get_tx(txid)
            isNext=False
            time.sleep(timeout_s)
            if trans:
                if len(trans['vin'])==1:
                    vi=trans['vin'][0]
                    if vi['txid']==previoustx:
                        value = vi['prevout']['value'] 
                        total = len(trans['vout'])                        
                        for i in range(index, len(trans['vout'])):                            
                            vo = trans['vout'][i]
                            print(f'TXID {txid} [{i}]/[{total}] {value} lenght {number_steps}')
                            print(f"{index} {vo['scriptpubkey_address']} {vo['value']}")            
                            outspend = get_outspend(txid,index)
                            time.sleep(timeout_s)
                            index +=1                            
                            if number_steps>maxNumerOfSteps:
                                maxNumerOfSteps = number_steps
                            if outspend:
                                if outspend['spent']==True:
                                    Stack.append([txid, previoustx, index, total-index, number_steps])
                                    number_steps +=1
                                    previoustx = txid                                
                                    txid = outspend['txid']
                                    index=0
                                    isNext = True
                                    break
                                else:
                                   print(f'{txid} [{index}] not spent, lenght {number_steps}')
                        
                else:
                    print(f'TXID {txid} have more then 1 input, lenght {number_steps}')
                    
                                   
        if isNext==False:    
            if len(Stack):
                lastElem = Stack.pop()
                txid = lastElem[0]
                previoustx = lastElem[1]
                index = lastElem[2]
                rest = lastElem[3]
                number_steps = lastElem[4]
            else:
                quit = True
                
    return  maxNumerOfSteps

if len(sys.argv)!=2:
    print (f'Usage: python task6.py SomeTxHash')
    exit()
tx = sys.argv[1]

trans = get_tx(tx)
longest=[0,0]
if trans:
    print(f'tx: {tx}')   
    print( f"Inputs: {len(trans['vin'])} Outputs:{len(trans['vout'])}")
    if filtr(trans):
        
        for i in range (2):
            print(f'Trace output {i}')
            outspend = get_outspend(tx,i)
            if outspend['spent']==True:
                longest[i] = get_longest_utxo(outspend['txid'], tx)
        if longest[0]!=longest[1]:
            winner = 0 if longest[0]>longest[1] else 1
            print(f'Longest UTXO have output {winner} with chain length {longest[winner]} in tx {tx}')
        else:
            print(f'Both outputs have the same chain length {longest[0]}')
    else:
        print('This transaction did not pass the filter, choose other..')