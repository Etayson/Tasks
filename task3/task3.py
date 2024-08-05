import sys

#Task3

Users=[]

def read_csv(file_path, day):    
    with open(file_path, mode='r', newline='') as file:
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
                isFound = False
                for user in Users:
                    if user[0]==fields[0]:
                        isFound = True
                        user[day].append(fields[1])
                        break
                if isFound==False:
                    if day==1:
                        Users.append([fields[0],[fields[1]],[]])
                    else:
                        Users.append([fields[0],[],[fields[1]]])
            else:
                print(f"lenght of fields  not match to headers lenght: {line}")                
          
        
#due to clarification by the author we can determine for ourselves what order the files will be loaded in
if len(sys.argv)!=3:
    print (f'Usage: python task3.py CSVfileFirstDay CSVfileSecondDay')
    print (f'Note: CSVfileFirstDay is the file where timestamps earlier than in CSVfileSecondDay')
    exit()
    
file_path = sys.argv[1] #file where visits on the FIRST day
read_csv(file_path,1)

file_path = sys.argv[2] #file where visits on the SECOND day
read_csv(file_path,2)

for user in Users:
    isMatchCr1 = False
    isMatchCr2 = False
    if len(user[1])>0 and len(user[2])>0:
        #Creteria 1: Visited some pages on both days
        isMatchCr1 = True
            
    for visited_in_day2 in user[2]:
        isFound = False
        for visited_in_day1 in user[1]:
            if visited_in_day1==visited_in_day2:                    
                isFound = True
        if isFound==False:
            #Creteria 2: On the second day visited the page that hadn’t been visited by this user on the first day
            isMatchCr2 = True
            break
    if isMatchCr1 and isMatchCr2:
        print(f'user_id: {user[0]}')     
