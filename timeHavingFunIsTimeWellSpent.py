#tsp alternate method

#goal #1
#create a ranking list of "best edges"

#a cycle begins and ends at the same vertex
#each vertex will have many [n-1] edges

#the top edges of each will be considered when creating
#starting points


#i.e., [0, 1 ..... 6, 0]
#then the program will work either beginning at the left
#and generating best edges for that side [top #1 first]
#once no more top#1 occur, then goes to the right and gets top #1 if possible
#going back and forth until all vertices are used.

#either at the left.... or at the right
#same steps.


#each vertex will have 3 "best edges"
#e.g., 1: A     2: B    3: C
#variations of two picked include
#therefore, for N number of vertices..
#there are 6*N paths to check.
#A C / C A
#A B / B A
#B C / C B

#implementation detail: make separate stored routes for starting left or right
#or just run a single set of starting edges twice and keep the better version

import sys;
import itertools;
import math;

largestInd = -1;
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

edgeKey_WeightValue = {
    }

verticeAdjacency = {
    }

min_weight = math.inf;
min_cycle = [];

cyclesBetter = [];

my_min = math.inf;
all_my_cyc_and_wt = [];
my_cyc = [];

tot = 0;
place = 1;

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
            edgeKey_WeightValue[(lineSplit[0],lineSplit[1])] = lineSplit[2];
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
            #print("Largest Index: ", largestInd);

#    for vert in graph['Vertices']:
#        print(vert, "|||", graph['Vertices'].get(vert));
    return;

def printEdgeKeyWeightValue(diction):
    for edge in diction:
        print(edge, ": ", diction[edge]);

def printVertsEdges(inGraph, on, off):
    if(on):
        for vert in inGraph['Vertices']:
            print(vert, ": ", inGraph['Vertices'][vert]);
    if(off):
        #print("\t-Edges-");
        for edge in inGraph['Edges']:
            print(edge);
        #print("\t-complete-");

def genAllPerms(sequence):
    i = 0;
    for perm in (list(itertools.permutations(sequence, len(sequence)))):
        cycle = list(perm);
        cycle.append(cycle[0]);
        calculateWeight(cycle, 1);
        i += 1;
        #print(cycle);

def calculateWeight(cycle, placeFlag=0, justPresent=0, postfix=0):
    global min_weight;
    global min_cycle;
    global place;
    global tot;
    weight = 0;
    i = 0;
    #print("weighing...: ", cycle);
    while(i < len(cycle) - 1):
        curr = cycle[i];
        nxt = cycle[i+1];
        thing = (curr,nxt);
        if((curr,nxt) not in edgeKey_WeightValue):
            #print( (curr,nxt), "not in");
            thing = (nxt,curr);
        weight += edgeKey_WeightValue[thing];
        i += 1;
    if(not placeFlag and postfix):
        all_my_cyc_and_wt.append((weight, cycle));
    if(placeFlag and my_min >= weight):
        if(my_min > weight):
            place += 1;
        if place <= 10:    
            cyclesBetter.append((weight, cycle));
    if(weight < min_weight):
        min_weight = weight;
        min_cycle = cycle;
    if(placeFlag):
        tot += 1;
    if(justPresent):
        return weight, cycle;
    return min_weight, min_cycle;
    #print(weight);

def getWeight(thing):
    alt = thing;
    if alt not in edgeKey_WeightValue:
        alt = (alt[1], alt[0]);
    return edgeKey_WeightValue[alt];

def isInEither(left, right, element):
    if element in left or element in right:
        return True
    return False

def createSortedMinimumAdjacency(inGraph):
    global verticeAdjacency;
    for vert in inGraph['Vertices']:
        verticeAdjacency[vert] = [];
        for adjacent in inGraph['Vertices'][vert]['adjacent']:
            #edge = (vert, adjacent);
            foundWeight = getWeight((vert, adjacent));
            verticeAdjacency[vert].append((foundWeight, adjacent));
        verticeAdjacency[vert].sort();
        
def printSortedAdjacency(verticeAdjacency):
    
    for vert in verticeAdjacency:
        print(vert, ": ", verticeAdjacency[vert]);
    
    return;

def getSortedAdjacencyLtd(cap):
    global verticeAdjacency;
    limitedAdjacency = {}
    thing = []
    i = 0
    for vert in verticeAdjacency:
        #print(vert, ": ", end="");
        limitedAdjacency
        for neighbor in verticeAdjacency[vert]:
            #if i + 1 < cap:
                #print(neighbor, end=", ")
            #else:
                
                #print(neighbor)
            thing.append(neighbor)
            
            i += 1
            if i >= cap:
                break
        limitedAdjacency[vert] = thing
        thing = []
        i = 0
    
    return limitedAdjacency

#goal #1
#create a ranking list of "best edges"

#a cycle begins and ends at the same vertex
#each vertex will have many [n-1] edges

#the top edges of each will be considered when creating
#starting points


#i.e., [0, 1 ..... 6, 0]
#then the program will work either beginning at the left
#and generating best edges for that side [top #1 first]
#once no more top#1 occur, then goes to the right and gets top #1 if possible
#going back and forth until all vertices are used.

#either at the left.... or at the right
#same steps.


#each vertex will have 3 "best edges"
#e.g., 1: A     2: B    3: C
#variations of two picked include
#therefore, for N number of vertices..
#there are 6*N paths to check.
#A C / C A
#A B / B A
#B C / C B

#implementation detail: make separate stored routes for starting left or right
#OR just run a single set of starting edges twice and keep the better version

def main(argv):
    global graph
    global my_min
    global my_cyc
    global tot
    global all_my_cyc_and_wt
    global verticeAdjacency
    PARSEINPUT(argv[1])
    #printVertsEdges(directedGraph, 0, 1);
    #print("undirected below:");
    #printVertsEdges(graph, 1, 0)
    #printEdgeKeyWeightValue(edgeKey_WeightValue);

    createSortedMinimumAdjacency(graph)
    #printSortedAdjacency(verticeAdjacency)
    alg = getSortedAdjacencyLtd(3)
    #printSortedAdjacency(alg)

    newLeftRightList = []


    print("\n\nspacer\n\n")
    for vert in alg:
        permCounter = 0
        for perm in (list(itertools.combinations(alg[vert], 2))):

            left = [vert, perm[0][1]]
            right = [perm[1][1], vert]

            worstLeft = 0
            worstRight = 0
            ctr = 0

            theLowest = 0
            permCounter += 1
            while len(left) + len(right) <= len(alg):
                #ctr += 1
                #if ctr > 20:
                #    break;
                while worstLeft <= worstRight:
                    for ver in verticeAdjacency[left[len(left)-1]]:
                        if not isInEither(left, right, ver[1]):
                            left.append(ver[1])
                            break;
                        worstLeft += 1
                        if worstLeft > worstRight:
                            break;
                    if worstLeft > worstRight:
                        break;
                    else:
                        worstLeft = 0
                    if len(left) + len(right) >= len(alg):
                        break;
                worstRight = 0
                while worstRight <= worstLeft:
                    for ver in verticeAdjacency[right[0]]:
                        if not isInEither(left, right, ver[1]):
                            right = [ver[1]] + right
                            break;
                        worstRight += 1
                        if worstRight > worstLeft:
                            break;
                    if worstRight > worstLeft:
                        break;
                    else:
                        worstRight = 0
                    if len(left) + len(right) >= len(alg):
                        break;
                worstLeft = 0

            combined = left + right

            #print(len(alg), ": ", len(left)+len(right))


            myWt = calculateWeight(combined, 0, 1, 0)

            newLeftRightList.append(myWt)

            left = [vert, perm[0][1]]
            right = [perm[1][1], vert]
            ctr = 0;
            worstLeft = 0
            worstRight = 0
            while len(left) + len(right) <= len(alg):
                #ctr += 1
                #if ctr > 20:
                #    break;
                
                while worstRight <= worstLeft:
                    for ver in verticeAdjacency[right[0]]:
                        if not isInEither(left, right, ver[1]):
                            right = [ver[1]] + right
                            break;
                        worstRight += 1
                        if worstRight > worstLeft:
                            break;
                    if worstRight > worstLeft:
                        break;
                    else:
                        worstRight = 0
                    if len(left) + len(right) >= len(alg):
                        break;
                worstLeft = 0
                while worstLeft <= worstRight:
                    for ver in verticeAdjacency[left[len(left)-1]]:
                        if not isInEither(left, right, ver[1]):
                            left.append(ver[1])
                            break;
                        worstLeft += 1
                        if worstLeft > worstRight:
                            break;
                    if worstLeft > worstRight:
                        break;
                    else:
                        worstLeft = 0
                    if len(left) + len(right) >= len(alg):
                        break;
                worstRight = 0


            combined = left + right
            #print(combined)


            myWt = calculateWeight(combined, 0, 1, 0)
            #print("my WeightRight_to_Left: ", myWt)


            newLeftRightList.append(myWt)

            #print(len(alg), ": ", len(left)+len(right))

    newLeftRightList.sort(reverse=True)
    for e in newLeftRightList:
        #break;
        print(e)
        #if(len(e[1]) < len(alg)):
        #    print("not valid length for total graph, e:", len(e), "---alg:", len(alg))
        #else:
        #    print("e:", len(e[1]), " > ", len(alg))
    print("how many cycles were made?: ", len(newLeftRightList))



    return;

if __name__ == "__main__":
    main(sys.argv);
