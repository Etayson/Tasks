
#task7
        
def max_candies(pinatas):
    Stack=[]
    lenght = len(pinatas)
    maxcandies = 0
    quit = False
    index=0
    candies = 0
    loadedcandies=0    
    while not quit:        
             
        if pinatas[index]>0:
            center_candies = pinatas[index]
                            
            left_index  = (index-1) if index>0 else 1
            left_candies = pinatas[left_index]            
            
            right_index = (index+1) if index+1<lenght else 1
            right_candies = pinatas[right_index] 
            
            if left_candies * center_candies * right_candies>0:
                candies +=left_candies * center_candies * right_candies
                arrcopy = pinatas.copy()
                arrcopy[index] = 0
                Stack.append([arrcopy, index, candies])
                
                
                if candies>maxcandies:
                    maxcandies=candies
                candies = loadedcandies
        
        if index<lenght-1:
            index +=1
            
        else:
            if len(Stack):
                LastElem = Stack.pop()
                pinatas, index, candies = LastElem[0], LastElem[1], LastElem[2]
                loadedcandies = candies
                
                if index<lenght-1:
                    index +=1
            else:
                quit = True  
        
        
    return maxcandies

while True:
    #The solution will be correct if the array of nums is an array of candies for the pinata
    pinatas = []
    array_of_num = input('Enter array of nums ex. 3,5,1: ') 
    if len(array_of_num)>0:
        for x in array_of_num.replace(" ", "").split(','):
            pinatas.append(int(x))
        
        print(f'max amount of candies: {max_candies(pinatas)}')
    exit()