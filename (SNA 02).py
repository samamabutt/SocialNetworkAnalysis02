import snap 
import random as random
import matplotlib as plt


def main():
    #Loading the graph
    epinions = snap.LoadEdgeList(snap.PNGraph,"soc-Epinions1.txt",0,1)
    pr = PageRank(epinions, 0.8, 0.001)
   
    #calling page rank function
    #print pr
    #getting number of strongly connected components in the graph
    scc = snap.GetMxScc(epinions)
    
    #Storing SCC nodes id's in an array
    sccNodes = []
    for nodes in scc.Nodes():
        sccNodes.append(nodes.GetId())
    #storing total nodes
    nodeList = []
    for node in epinions.Nodes():
        nodeList.append(node.GetId())
    
    rankDesc = []
    rankIds = []
    #Computing top rank nodes
    for index,element in enumerate(pr):
        b,c = element
        rankDesc.append(b)
        rankIds.append(nodeList[index])
    
    rankDesc.sort(reverse=True)
    rankIds.sort(reverse=True)
    
    topRankNodes = rankDesc[0:10]
    topIds = rankIds[0:10]
    print "Top Rank Nodes: ",topRankNodes
    # Number of incoming edges (indegree of x) 
    #Ranks of all the source pages having hyperlinks toward x 
    for index, element in enumerate(topIds):
        
         currentNode = epinions.GetNI(topIds[index])
         x = currentNode.GetInDeg()
         
         for i in range(x):
            innerNode = currentNode.GetInNId(i)
            indi = nodeList.index(innerNode)
            ele = pr[indi]
            print "In Degree: ",innerNode, "w.r.t. node: ",x,"Rank: ",ele
  
    
    #printing number of strongly connected components in the graph    
    print "Number of nodes in SCC: ",scc.GetNodes()
    
    #Applying a BFS to get the Out Set from node 1  
    BfsOutSet = snap.GetBfsTree(epinions, sccNodes[0], True, False)
    #storing Out Set nodes in an array
    bfsOutNodes = []
    for nodes in BfsOutSet.Nodes():
        if (nodes.GetId() not in sccNodes):
            bfsOutNodes.append(nodes.GetId())
    #removing the SCC to get the Out Set Nodes
    for outNode in BfsOutSet.Nodes():
        if outNode.GetId() in sccNodes:
           BfsOutSet.DelNode(outNode.GetId()) 
    print "Number of OutSet Nodes: ", BfsOutSet.GetNodes()
    #applying BFS search to find the tendrils in Out Set
    outSetTen = snap.GetBfsTree(BfsOutSet, bfsOutNodes[0], False, True)
    print  "Tendrils in OutSet: ",outSetTen.GetNodes()
    #storing out set tendrils in an array to use it later
    outTendrils = []
    for node in outSetTen.Nodes():
        outTendrils.append(node.GetId())
    #applying BFS to get in set nodes
    BfsInSet = snap.GetBfsTree(epinions, sccNodes[0], False, True)
    #storing In Set nodes in an array 
    bfsInNodes = []
    for nodes in BfsInSet.Nodes():
        if (nodes.GetId() not in sccNodes):
            bfsInNodes.append(nodes.GetId())
    #removing the SCC to get the Out Set Nodes
    for inNode in BfsInSet.Nodes():
        if inNode.GetId() in sccNodes:
           BfsInSet.DelNode(inNode.GetId()) 
    print "Number of InSet Nodes: ", BfsInSet.GetNodes(),"clone:",len(bfsInNodes)
    #applying BFS search to find the tendrils in Out Set
    inSetTen = snap.GetBfsTree(BfsInSet, bfsInNodes[0], False, True)
    print  "Tendrils in InSet: ",inSetTen.GetNodes()
    #storing out set tendrils in an array to use it later
    inTendrils = []
    for node in inSetTen.Nodes():
        inTendrils.append(node.GetId())
    #tubes in a SCC
    tubeNodes = []
    for nodes in inSetTen.Nodes():
        if nodes in outSetTen.Nodes():
            tubeNodes.append(nodes.GetId())        
    print "Tubes in SCC: ",len(tubeNodes)
    #storing disconnected region in an array
    disComp = []
    for nodes in epinions.Nodes():
        if (nodes.GetId() not in sccNodes) and (nodes.GetId() not in bfsOutNodes) and (nodes.GetId() not in bfsInNodes) and (nodes.GetId() not in inTendrils) and (nodes.GetId() not in outTendrils):
            disComp.append(nodes.GetId())
    print "Number of Disconnected Components: ",len(disComp)
    probabilities = Random(epinions,5)
    probabilities, nodes = Random(epinions,5)
    plt.plot()
    plt.plot(nodes, probabilities)
    plt.xlabel('No of Nodes')
    plt.ylablel('Probability that path exists')
    plt.show()




def Random(G, x):
  
    
     nodeList = []
     for node in G.Nodes():
         nodeList.append(node.GetId())
         
    
    
     length = len(nodeList)
     
     randomNodes = 10
     
     probs = []
     
     for i in range(x):
        print(i)
         
        localPairs = []
        
        for pair_range in range(randomNodes):
             rand_one = random.randint(0,length)
             rand_two = random.randint(1,length - 1)
             localPairs.append((nodeList[rand_one],nodeList[rand_two]))
         
        pairExist = 0
        
        for item in localPairs:
            
            a, b = item
            NIdToDistH = snap.TIntH()
            
            snap.GetShortPath(G, a, NIdToDistH, True)
            
            if b in NIdToDistH and NIdToDistH[b] > 0:
                 pairExist = pairExist + 1
            
           
        #print(len(localPairs))
        val = float(pairExist) / float(len(localPairs))
        probs.append(val)
        
        randomNodes = randomNodes * 2
    
    
     #print(probs)
     return probs
         
         
     
     
     
     






def PageRank(G, B, E):
    
    
    
    nodeArray = []
    
    ids = []
    
    
    totalNodes = float(float(1)/float(G.GetNodes()))
    
    
    for node in G.Nodes():
         
         nodeId = node.GetId()
         ids.append(nodeId)
         clone = totalNodes
         c = node.GetOutDeg()
         nodeArray.append((clone,c))
         
    
    while(True):
        
        temp = nodeArray
    
        for index, element in enumerate(temp):
            
            nodeId = ids[index]
            clone,c = temp[index]
            
            nodeNow = G.GetNI(nodeId)
            x = nodeNow.GetInDeg()
            
            if x != 0:
                sum = 0
                for i in range(x):
                    inNode = nodeNow.GetInNId(i)
                    outDeg = G.GetNI(inNode).GetOutDeg()
                    nodeIndex = ids.index(inNode)
                    innerElement, inner_element_c = temp[nodeIndex]
                    sum = sum + float(float(innerElement)/float(outDeg))
                
                sum = sum * B
                temp[index] = (sum,c)
                
            else:
                temp[index] = (0,c)
            
        totalDifference = 0
            
        for index,element in enumerate(nodeArray):
            first, c = nodeArray[index]
            second, d = temp[index]
            difference = second - first
            totalDifference = totalDifference + difference
            
            
        if (totalDifference > E):  
            print(totalDifference)
            nodeArray = temp 
        else: 
            break
    return nodeArray

   
    
main()