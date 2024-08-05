import requests
import re
import threading
import time
import sys

#task4

path=[]
link_pattern = re.compile(r'href=["\'](/wiki/[A-Za-z0-9_]+)["\']', re.IGNORECASE)
stop_event = threading.Event()

def get_page(url):
    try:        
        r = requests.get(url);        
        return r
    except requests.exceptions.RequestException as e:
        print(f"error {str(e)}")
        return ""

def check(links):     
    for link in links:
        if link == target_url:
            return True
    return False
    
def delTrashLink(url, links):
    #this function removes unnecessary pages from the links array to prevent recursion       
    trashs=[start_url.lower(), url.lower(), 'https://en.wikipedia.org/wiki/Main_Page'.lower(), 'https://en.wikipedia.org/wiki/Wikipedia'.lower()]
    pos = 0
    while pos<len(links):        
        #ignore case
        if links[pos].lower() in trashs:               
            del links[pos]
        else:
            pos +=1
    return links

def clear_line(length):    
    print('\r', end='')    
    print(' ' * length, end='')    
    print('\r', end='')
 
def get_links_page(url):    
    content_links=[]
    response = get_page(url)            
    if response:            
        content = response.text                                
        relative_links = link_pattern.findall(content)    
        for lnk in relative_links:
            content_links.append('https://en.wikipedia.org' + lnk)           
        content_links = delTrashLink(url, content_links)
    return  content_links  
    
def isHitler_crawler(numThread):
 
    Stack=[]
    quit = False
    isFound = False    
    while not isFound and not stop_event.is_set():
        if start_links:
            url = start_links.pop(0)
            print(f'Thread #{numThread} page {url}')
        else:
            break
        NumberOfHops = 1
        isNext = True
        rest = 1  
        index = 0
        total = 1 
        links=[]
        links.append(url)
        length = 1
        while not quit and not stop_event.is_set():
            time.sleep(0.001)
            rest = total - index
            if  rest>0:
                url = links[index]
                content_links = get_links_page(url)            
                isNext = False
                if content_links:            
                    
                    if content_links:
                    
                        if check(content_links)==False:                                                
                            index +=1
                            
                            if NumberOfHops <maxNumberOfHops:                               
                                Stack.append((links, index, total,  NumberOfHops))
                                NumberOfHops +=1                            
                                isNext = True
                                links = content_links
                                total = len(links)
                                index = 0
                            else:
                                #Reached max number of hops
                                isNext = True
                                    
                        else:
                           
                            #Hitler found, reconstruct the path                            
                            path.insert(0, links[index])
                            while len(Stack):
                                LastElem = Stack.pop()
                                links_elem = LastElem[0]
                                index_elem = LastElem[1]
                                path.insert(0, links_elem[index_elem-1])                        
                            isFound = True
                            stop_event.set()
                    else:
                        index +=1
                        isNext = True
                else:
                    index +=1
                    isNext = True
            else:
                isNext=False
                
            if isNext==False:    
                if len(Stack):                
                    LastElem = Stack.pop()                
                    links = LastElem[0]
                    index = LastElem[1]
                    total = LastElem[2]
                    NumberOfHops = LastElem[3]                                    
                else:
                    quit = True    
                
    return isFound

def check_double_path(path):
    copy_path = path    
    if len(copy_path)>1:
        isOk = False
        while not isOk:
            isOk = True
            for i in range(0, len(copy_path)-1):
                isFindDouble = False
                for j in range(i+1, len(copy_path)):
                    if copy_path[i] == copy_path[j]:                        
                        isFindDouble = True
                        isOk = False
                        double_index = j
                if isFindDouble==True: 
                    double_index -= i                    
                    for k in range(0, double_index):                        
                        del copy_path[i+1]
        
    return copy_path
  
maxNumberOfHops = 6 
target_url ='https://en.wikipedia.org/wiki/Adolf_Hitler'


if len(sys.argv)!=2:
    print (f'Usage: python task4.py https://en.wikipedia.org/wiki/Banana')
    exit()
start_url = sys.argv[1]
    
start_links = get_links_page(start_url)

if start_links:
    try:
        numberOfThreads = 6 
        threads = []
        for i in range(numberOfThreads):
            thread = threading.Thread(target=isHitler_crawler, args=(i,))
            thread.start()
            threads.append(thread)
            time.sleep(0.1)
            
        isLive = True
        print(f'\\', end='', flush=True)
        arr = ['|', '/', '-', '\\']
        i = 0
        length= len(f'\\')
        while isLive:
            isLive = False
            time.sleep(0.5)
            clear_line(length)
            a = arr[i]
            length = len(f'{a}')
            i +=1
            if i>3:
                i=0                
            print(a, end='', flush=True)
            for thread in threads:
                if thread.is_alive():
                    isLive = True
        
        clear_line(length)         
        if path:
            print('Path to Hitler page:')            
            print(start_url)
            clear_path = check_double_path(path) 
            for elem in clear_path:
                print(elem)
                
        else:
            print('Hitler not found')
            
    except KeyboardInterrupt: 
    
        stop_event.set()
        for thread in threads:
            thread.join()
        
        
    