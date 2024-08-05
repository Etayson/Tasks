import random
import time

#Task2

Entrance = '+'
Exit = '-'
Road = ' '
Wall = 'X'
Trap = '@'
Treasure = '?'
Step = '*'
isTraps = True
isTreasures = True
isExit = False

num_of_Tresures = random.randint(0,1) if isTreasures==True else 0
num_of_traps = random.randint(0,5) if isTraps==True else 0

def generate_matrix(xsize, ysize):
    global isExit       
    global num_of_Tresures
    global num_of_traps
    matrix = [[Wall] * xsize for i in range(ysize)] 
    Stack=[]
    sx, sy = (random.randint(1, xsize-2), random.randint(1, ysize-2))
    x, y = sx, sy
    #matrix[y][x] = Entrance
    dirpos=0
    isStart = False
    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(directions)
    while True:
        isNewIter = False
        matrix[y][x] = Road
        while dirpos<4: #max 4 elemets in directions array           
            dx, dy  = directions[dirpos] 
            dirpos +=1    
            nx, ny = x + dx, y + dy            
            if 1 <= nx < xsize-1 and 1 <= ny < ysize-1 and matrix[ny][nx] == Wall:
                if num_of_Tresures>0 and random.randint(0,5)>3:                    
                    num_of_Tresures -=1
                    matrix[y + dy // 2][x + dx // 2] = Treasure                    
                elif num_of_traps>0 and random.randint(0,5)>4:                    
                    num_of_traps -=1
                    matrix[y + dy // 2][x + dx // 2] = Trap                   
                else:
                    matrix[y + dy // 2][x + dx // 2] = Road
                
                Stack.append([directions, x, y, dirpos])                
                x, y = nx, ny
                directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
                random.shuffle(directions)                
                dirpos=0
                isNewIter = True
                break
                
            if  1 <= nx < xsize-1 and 0 <= ny <ysize and matrix[ny][nx] == Wall and isStart==False and isNewIter == False:
                matrix[y + dy // 2][x + dx // 2] = Road                
                matrix[ny][nx] = Entrance
                sx, sy = nx, ny
                print(f'Start at {sx}, {sy}')
                isStart = True
            elif 1 <= nx < xsize-1 and ny==-1 and matrix[y + dy // 2][x + dx // 2] == Wall and isStart==False and isNewIter == False:
                matrix[y + dy // 2][x + dx // 2] = Entrance
                sx, sy = x + dx // 2, y + dy // 2
                print(f'start at {sx}, {sy}')                
                isStart = True
                
            if 0 <= nx < xsize-1 and 0 <= ny <ysize and matrix[ny][nx] == Wall and isExit == False and isNewIter == False:
                #when the wall is double (left, right, bottom)
                if isStart==False or (isStart==True and sy!=ny) or (isStart==True and sy==ny and (sx-nx>xsize//4 or sx-nx<-xsize//4)):
                    matrix[y + dy // 2][x + dx // 2] = Road
                    print(f'exit at {nx}, {ny}')
                    matrix[ny][nx] = Exit
                    isExit = True
            elif (((nx<=0 or  nx>= xsize) and ny>=ysize//2) or (0 <= nx < xsize-1 and ny==ysize)) and matrix[y + dy // 2][x + dx // 2] == Wall and isExit == False and isNewIter == False:
                #when the wall is single (left, right, bottom)
                matrix[y + dy // 2][x + dx // 2] = Exit
                print(f'Exit at {x + dx // 2}, {y + dy // 2}')                
                isExit = True
            
        if isNewIter==False:
            if len(Stack):
                lastElem = Stack.pop()        
                directions, x, y, dirpos = lastElem[0], lastElem[1], lastElem[2], lastElem[3]
            else:
                break
    return matrix, sx, sy

def find_exit(matrix, x, y):
    global isExit 
    global Step
    isExit = False
    Stack=[]    
    dirpos=0    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    isNewIter = True
    while True: 
        if isNewIter==True:
            char = matrix[y][x]
            matrix[y][x] = Step
        isNewIter = False    
        while dirpos<4 and isExit == False: #max 4 elemets in directions array     
            dx, dy  = directions[dirpos] 
            dirpos +=1 
            nx, ny = x + dx, y + dy            
            if 0 <= nx < xsize and 0 <= ny < ysize and (matrix[ny][nx] == Road or matrix[ny][nx] == Trap or matrix[ny][nx] == Treasure):                
                #print_matrix(matrix)
                #time.sleep(0.15)
                Stack.append([directions, x, y, dirpos, char])                
                x, y = nx, ny
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)                
                dirpos=0
                isNewIter = True
                break        
            if 0 <= nx < xsize and 0 <= ny < ysize and matrix[ny][nx] == Exit: 
                isExit = True                                
            if isExit == True:
                break
        if isExit == False and isNewIter==False:
            matrix[y][x] = char
        if isNewIter==False:
            if len(Stack):
                lastElem = Stack.pop()        
                directions, x, y, dirpos, char = lastElem[0], lastElem[1], lastElem[2], lastElem[3], lastElem[4]
            else:
                break
    return matrix
    
def print_matrix(matrix):
    for row in matrix:
        print((''.join(str(j) for j in row) ))


while True:
    inp_matrix_size = input("Enter matrix size X,Y ex. 10,10: ") 
    if len(inp_matrix_size.replace(" ", "").split(','))==2:
        xsize, ysize = (int(x) for x in inp_matrix_size.replace(" ", "").split(','))
        break
print(f'Matrix size: {xsize}x{ysize}')
print(f'Number of tresures {num_of_Tresures} traps {num_of_traps}')
print(f"Entrance '{Entrance}' Exit '{Exit}' Road '{Road}' Wall '{Wall}' Trap '{Trap}' Treasure '{Treasure}'")

matrix, sx, sy = generate_matrix(xsize, ysize)
print_matrix(matrix)
print()

matrix = find_exit(matrix, sx, sy)
if isExit == True:
    print(f"Exit path '{Step}':")
    print_matrix(matrix)
