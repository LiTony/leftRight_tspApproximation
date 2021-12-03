#generate all combinations of 0 thru n [0,n] for example.
#generate a random weight to go with that combination
import sys
import itertools
import random
import math

largestInd = -1;

eKWV = {
    }

graph = {
    'Vertices': {
        
        },
    'Edges': {
        
        }
    }

directedGraph = {
    'Vertices': {
        
        },
    'Edges': {
        
        }
    }

verticeAdjacency = {
    }

def main(argv):
    random.seed()
    #for arg in argv:
    #    print(arg)
    if len(argv) != 2:
        print("incorrect argument formatting, closing")
        print("python3 program filename")
        return
    vertCap = -1
    minWt = -1
    maxWt = -math.inf;
    while vertCap < 2:
        vertCap = int(input("How many vertices? "))
    while minWt < 1:
        minWt = int(input("What minimum weight (integer)? "))
    while maxWt < minWt:
        maxWt = int(input("What maximum weight (integer)? "))

    if len(argv) == 2:
        fileDest = open(argv[1], 'w')
    
    vertArray = [integer for integer in range(0,vertCap)]
    #print(vertArray)
    generateAll(vertArray,minWt,maxWt, fileDest)
    fileDest.close()
    PARSEINPUT(argv[1])
    createSortedMinimumAdjacency(graph)
    printSortedAdjacency()
    #for eKW in eKWV:
    #    print(eKW, ": ", eKWV[eKW])
    #getNearest(0, [1,4,3,0])

    for i in range(0, vertCap):
        nearestNeighbor = produceNearestFrom(i, vertCap - 1)
        neighborCycle = nearestNeighbor + [nearestNeighbor[0]]
        print(neighborCycle)
    
    return

def produceNearestFrom(start, size):
    i = 0
    array = [start]
    node = start
    while i < size:
        pairing = getNearest(node,array)
        #print(node)
        #print(pairing)
        array.append(pairing[1])
        node = pairing[1]
        i += 1
    return array

def getNearest(node, array):
    weight_node = None
    i = 0
    thing = verticeAdjacency[node]
    nearest = None
    while i < len(thing):
        nearest = thing[i]
        if(nearest[1] in array):
            i += 1
        else:
            #print(thing)
            #thing.remove(thing[i])
            break
    
    #print(nearest)
    #print(thing)
    return nearest

def generateAll(vertices, lowerWT, upperWT, fileDest):
    combos = itertools.combinations(vertices, 2)
    for combo in combos:
        #print(combo)
        thing = list(combo)
        #print(thing)
        weight = random.randrange(lowerWT, upperWT, 1)
        thing.append(weight)
        #print("new: ", thing)
        string_ints = [str(integer) for integer in thing]
        string = ", ".join(string_ints)
        #print(string)
        fileDest.write(string + '\n');
    return

def createSortedMinimumAdjacency(inGraph):
    global verticeAdjacency;
    for vert in inGraph['Vertices']:
        verticeAdjacency[vert] = [];
        for adjacent in inGraph['Vertices'][vert]['adjacent']:
            #edge = (vert, adjacent);
            foundWeight = getWeight((vert, adjacent));
            verticeAdjacency[vert].append((foundWeight, adjacent));
        verticeAdjacency[vert].sort();

def getWeight(thing):
    alt = thing;
    if alt not in eKWV:
        alt = (alt[1], alt[0]);
    return eKWV[alt];

def printSortedAdjacency():
    global verticeAdjacency;
    for vert in verticeAdjacency:
        print(vert, ": ", verticeAdjacency[vert]);
    
    return;
        
def PARSEINPUT(file):
    global largestInd
    graph['Edges'] = [];
    directedGraph['Edges'] = [];
    with open(file) as f:
        for line in f:
            vertexInfo = {};
            vertexInfo2 = {};
            vertexInfo_drc = {};
            vertexInfo_drc2 = {};
#            print(line, end='');
            lineSplit = line.strip();
            lineSplit = line.split(',');
            lineSplit[1] = lineSplit[1].strip();
            lineSplit[2] = lineSplit[2].strip();
            lineSplit[0], lineSplit[1], lineSplit[2] = int(lineSplit[0]), int(lineSplit[1]), int(lineSplit[2]);
            graph['Edges'].append(lineSplit);
            directedGraph['Edges'].append(lineSplit);
            eKWV[(lineSplit[0],lineSplit[1])] = lineSplit[2];
            if(lineSplit[0] not in graph['Vertices']):
                vertexInfo['explore'] = False;
                vertexInfo['adjacent'] = [];
                graph['Vertices'][lineSplit[0]] = vertexInfo;
                vertexInfo_drc['explore'] = False;
                vertexInfo_drc['adjacent'] = [];
                directedGraph['Vertices'][lineSplit[0]] = vertexInfo_drc;
            if(lineSplit[1] not in graph['Vertices']):
                vertexInfo2['explore'] = False;
                vertexInfo2['adjacent'] = [];
                graph['Vertices'][lineSplit[1]] = vertexInfo2;
                vertexInfo_drc2['explore'] = False;
                vertexInfo_drc2['adjacent'] = [];
                directedGraph['Vertices'][lineSplit[1]] = vertexInfo_drc2;
            #if(lineSplit[0] not in graph['Vertices'][lineSplit[1]]['adjacent']):
            graph['Vertices'][lineSplit[1]]['adjacent'].append(lineSplit[0]);
            #if(lineSplit[1] not in graph['Vertices'][lineSplit[0]]['adjacent']):
            graph['Vertices'][lineSplit[0]]['adjacent'].append(lineSplit[1]);
            directedGraph['Vertices'][lineSplit[0]]['adjacent'].append(lineSplit[1]);                         
    for vert in graph['Vertices']:
        graph['Vertices'][vert]['adjacent'].sort();
        if(vert > largestInd):
            largestInd = vert;

if __name__ == "__main__":
    main(sys.argv)
