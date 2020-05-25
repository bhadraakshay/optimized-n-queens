class Node:
    def __init__(self, x, y, parent, depth, occurrence, total):
        self.x=x
        self.y=y
        self.parent=parent
        self.depth=depth
        self.occurrence=occurrence
        self.total=total
        
def getTotal(node):
        return node.total 
    
def checkConflict(node1,node2):
    if node1.x==node2.x:
        return True
    if node1.y==node2.y:
        return True
    if abs(node1.x-node2.x)==abs(node1.y-node2.y):
        return True
    if node1.occurrence>node2.occurrence:
        return True
    else:
        return False
    
def checkAllConflicts(node1,node2,startNode):
    if checkConflict(node1,node2):
        return True
    else:
        if node2.parent.x != startNode.x and node2.parent.y != startNode.y:
            return checkAllConflicts(node1,node2.parent,startNode)   
        else:
            return False

def solvePath(node,yi,xList,yList,depth,startNode,noOfOfficers):
    """Use backtracking to find all solutions"""
    #base case
    if yi==len(yList) or depth==noOfOfficers:
        return True
    
    res=False
    for x in xList:
        if checkAllConflicts(Node(x,yList[yi],None,0,0,0),node,startNode)==False:
            node=Node(x,yList[yi],node,depth+1,0,node.total)
                            
            res = solvePath(node, yi+1,xList,yList,depth+1,startNode,noOfOfficers)
            if res:
                return res
            else:    
            #backtrack
                node=node.parent
    return res

def solveInitialPath(node,yi,xList,yList,depth,startNode,noOfOfficers):
    """Use backtracking to find all solutions"""
    #base case
    global maxPoints
    global nodesList
    if yi==len(yList) or depth==noOfOfficers:
        maxPoints=node.total
        return True
    
    res=False
    for x in xList:
        if checkAllConflicts(Node(x,yList[yi],None,0,0,0),node,startNode)==False:
            node=Node(x,yList[yi],node,depth+1,0,node.total)
            for n in nodesList:
                if node.x==n.x and node.y==n.y:
                    node.occurrence=n.occurrence
                    node.total+=n.occurrence
                    
            res = solveInitialPath(node, yi+1,xList,yList,depth+1,startNode,noOfOfficers)
            if res:
                return True
            else:    
            #backtrack
                node=node.parent
    return res

def checkPath(node,startNode,noOfOfficers,xList,yList):
            
    n1=node
    while n1.x!=-1:
        xList.remove(n1.x)
        yList.remove(n1.y)
        n1=n1.parent
    n2=node   
    return solvePath(n2,0,xList,yList,n2.depth,startNode,noOfOfficers)
   
    
fin=open("input.txt","r")
inputLines=fin.readlines()
gridSize=0
noOfOfficers=0
noOfScooters=0
maxPoints=0
startNode = Node(-1,-1,None,0,0,0)
nodesList=[]

for index,f in enumerate(inputLines):
    if index==0:
        gridSize=int(f.strip())
        continue
    if index==1:
        noOfOfficers=int(f.strip())
        if noOfOfficers>gridSize:
            break
        continue
    if index==2:
        noOfScooters=int(f.strip())
        continue
    if gridSize==0 or noOfOfficers==0 or noOfScooters==0:
        break
    if index>2:
        x,y=f.strip().split(",")
        x=int(x)
        y=int(y)
        flag=True
        for n in nodesList:
            if n.x==x and n.y==y:
                n.occurrence+=1
                n.total=n.occurrence         
                flag=False
             
        if flag:
            nodesList.append(Node(x,y,startNode,1,1,1))            
            
if noOfOfficers<=gridSize:
    
    nodesList=sorted(nodesList,key=getTotal,reverse=True)
    nodesListIndex=0
    
    tempTotalList=[]
    i=1
    for k in nodesList[0:]:
        temp=k.total
        counter=1
        for l in nodesList[i:]:
            if checkAllConflicts(l,k,startNode)==False:
                if counter<noOfOfficers:
                    temp+=l.total
                    
                else:
                    break
                counter+=1    
        i+=1
        tempTotalList.append(temp)
    
    max=0
    
    for n in nodesList:
        xList=[]
        yList=[]
        i=0
        while i<gridSize:
            xList.append(i)
            yList.append(i)
            i+=1
            
        n1=n
        while n1.x!=-1:
            xList.remove(n1.x)
            yList.remove(n1.y)
            n1=n1.parent
        n2=n
        
        res=solveInitialPath(n2,0,xList,yList,n2.depth,startNode,noOfOfficers)
        if res:
            if max<maxPoints:
                max=maxPoints
            
    maxPoints=max 
    
    for n in nodesList:
        total=0
        if nodesListIndex<len(nodesList)-1:
            total=tempTotalList[nodesListIndex]
        
        nodesListIndex+=1
        if maxPoints>=total:
            continue
            
        allNodesList = []
        allNodesList.append([n])
        levelCount=1
        
        if len(nodesList)>1:
            while levelCount<=noOfOfficers:
                    
                for node2 in allNodesList[levelCount-1]:

                    index=0
                    for n in nodesList:
                        if node2.x==n.x and node2.y==n.y:
                            index+=1
                            break
                        index+=1 

                    for node1 in nodesList[index:]:
                        if checkAllConflicts(node1,node2,startNode)==False: 
                            a=Node(node1.x,node1.y,node2,node2.depth+1,node1.occurrence,node1.occurrence+node2.total)       
                            
                            
                            sum=a.total
                            counter=0
                            for k in nodesList[index:]:
                                if checkAllConflicts(k,a,startNode)==False:
                                    if counter<noOfOfficers-a.depth:
                                        sum+=k.total
                                    else:
                                        break
                                    counter+=1
                            if maxPoints<sum:  
                                if len(allNodesList)<=levelCount:
                                    allNodesList.append([])
                                allNodesList[levelCount].append(a)
                                    
                
                if len(allNodesList)<=levelCount:        
                    break
                print levelCount
                print len(allNodesList[levelCount])
                
                levelCount+=1                

        if len(allNodesList)==noOfOfficers:
            allNodesList[noOfOfficers-1]=sorted(allNodesList[noOfOfficers-1],key=getTotal,reverse=True)
            if maxPoints<allNodesList[noOfOfficers-1][0].total:
                maxPoints=allNodesList[noOfOfficers-1][0].total

        otherPathCheck=[]
        length=len(allNodesList)-1
        while length>=0:
            allNodesList[length]=sorted(allNodesList[length],key=getTotal,reverse=True)
            if allNodesList[length][0].total>maxPoints:
                for i in allNodesList[length]:
                    if i.total>maxPoints:
                        otherPathCheck.append(i)
            length-=1                

        xList=[]
        yList=[]
        i=0
        while i<gridSize:
            xList.append(i)
            yList.append(i)
            i+=1

        otherPathCheck=sorted(otherPathCheck,key=getTotal,reverse=True)
        for n in otherPathCheck:
            xList=[]
            yList=[]
            i=0
            while i<gridSize:
                xList.append(i)
                yList.append(i)
                i+=1
            if checkPath(n,startNode,noOfOfficers,xList,yList):
                maxPoints=n.total
                break     
  

fout=open("output.txt","w")
fout.write(str(maxPoints))
fin.close()
fout.close()
