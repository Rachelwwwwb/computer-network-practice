from collections import defaultdict
from heapq import *

def readFile(fileName):

    f = open(fileName, "r")
    text = f.readlines()
    lineNum = int(text[0])
    
    # adjacency matrix
    graph = []

    for i in range(lineNum):
        line = text[i + 1]
        source = line[0].upper()

        for x in range(len(line)):
            # find a edge
            if line[x] == '[':
                dest = line[x+1].upper()
                valueString = ""
                digitals = 1
                while line[x+2+digitals] != "]":
                    valueString += line[x+2+digitals]
                    digitals += 1

                value = int(valueString)
                x += 2 + digitals
                graph.append([source, dest, value])

    # for s in range(len(graph)): 
    #     print(graph[s]) 

    sn = text[lineNum + 1][0]
    dn = text[lineNum + 2][0]
   
    return graph, sn, dn

def run_dijkstra(graph, sn, dn):
    dic = defaultdict(list)
    for left, right, cost in graph:
        dic[left].append((cost, right))
    retval = ()

    queue, seen, mins = [(0,sn,())], set(), {sn: 0}

    while queue:
        (cost,v1,path) = heappop(queue)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == dn: 
                retval = (cost, path)
                break

            for singleCost, v2 in dic.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + singleCost
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(queue, (next, v2, path))

    totalCost = retval[0]
    tmp = retval[1]
    result = []
    num = []

    while True:
        result.append(tmp[0])
        if not tmp[1]:
            break
        tmp = tmp[1]

    result.reverse()
    l = result[0]
    for i in range(len(result)):
        r = result[i]
        for c, v2 in dic.get(l,()):
            if v2 == r:
                num.append(c)
        l = r
    
    printString = ""
    for i in range(len(result) - 1):
        printString += result[i] + "-"
        printString += str(num[i]) + "->"
    printString += result[len(result) - 1]
    printString += "\n" + str(totalCost)
    return printString

def print_output(result, filename):
    filel = open(filename,"w")
    filel.write(result)

    #Write strings as mentioned in 'expected output' seciton in the assignment

def start_dijkstra():
    graph, sn, dn = readFile('input.txt')
    result = run_dijkstra(graph, sn, dn)
    print_output(result, 'output.txt')

if __name__ == "__main__":
    start_dijkstra()
