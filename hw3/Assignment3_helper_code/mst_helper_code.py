import operator

nodeSet = set()

class Node:
    def __init__(self, v):
        self.s = set()
        self.v = v

class Edge:
    def __init__(self, a, b, cost):
        self.a = a
        self.b = b
        self.cost = cost

def readFile(fileName):
    graph = []
    f = open(fileName, "r")
    text = f.readlines()
    lineNum = int(text[0])

    for i in range(lineNum):
        line = text[i + 1]
        leftIndex = line[0].upper()
        nodeSet.__format__
        left = Node(line[0].upper())

        for x in range(len(line)):
            # find a edge
            if line[x] == '[':
                rightIndex = line[x+1].upper()
                right = Node(line[x+1].upper())
                for a in nodeSet:
                    if a.v == rightIndex:
                        right = a
                    if a.v == leftIndex:
                        left = a
                if right not in nodeSet:
                    nodeSet.add(right)
                if left not in nodeSet:
                    nodeSet.add(left)                    
                valueString = ""
                digitals = 1
                while line[x+2+digitals] != "]":
                    valueString += line[x+2+digitals]
                    digitals += 1

                value = int(valueString)
                x += 2 + digitals
                edge = Edge(left,right,value)
                graph.append(edge)

    return graph 

def run_mst(graph):
    result = []
    # sort the edges first
    # graph.sort(key=operator.attrgetter('cost'))
    graph.sort(key=lambda edge: (edge.cost,edge.a.v))

    for e in graph:
        # check if the edge will form a cycle
        if e.a in e.b.s or e.b in e.a.s:
            continue
        # if the edge does not form a cycle
        e.b.s.add(e.a)
        for x in e.a.s:
            e.b.s.add(x)
        e.a.s.add(e.b)
        for x in e.b.s:
            e.a.s.add(x)
        result.append(e)

    return result

def print_output(result, filename):
    filel = open(filename,"w")
    for x in result:
        line = str(x.cost) + " " + x.a.v + " " + x.b.v + "\n"
        filel.write(line)

def start_mst():
    graph = readFile('input.txt')
    result = run_mst(graph)
    print_output(result, 'output.txt')

if __name__ == "__main__":
    start_mst()