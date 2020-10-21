import sys

def searchpath(dic,main,target,path):
    path = path + [main]
   
    if main == target:
        print("please enter different main and target destination.") 
    elif target in dic[main]:
        print("Yes " + main + " and " + target + " are partners!\nYou can transfer your miles to "+target)
        path.append(target)
        stringPath = " -> ".join(path)
        print("The path is: " + stringPath)
        return path
        
    else:
        for elem in dic[main]:
            if elem not in path:
                newPath = searchpath(dic,elem,target,path)
                if newPath:
                    return newPath
        
f = open("airlines.txt", "r")

dic = {}
path = []

for line in f:
    splitline = line.strip().split(',')
    dic[splitline[0]] = splitline[1:]
    
f.close()

x = sys.argv[1]
y = sys.argv[2]

if x and y in dic:
    searchpath(dic,x,y,path)
else:
    print("Please enter valid arguments. e.g: British Airways\nList of Airlines: ")
    for key in dic.keys():
        print(key)
    exit()
