import os
import numpy as np
#import pip
#pip.main(['install', '--upgrade', 'numpy'])
import argparse

parser = argparse.ArgumentParser(description="Process some arguments.")
parser.add_argument('--bpop', type=str, required=False, help='Breed Population')
parser.add_argument('--mr', type=int, required=False, help='Mutation Rate')
parser.add_argument('--mpop', type=int, required=False, help='Max Population')
parser.add_argument('--part', type=int, required=False, help='Number of Parts')

args = vars(parser.parse_args())

shortFlag = 0

def readFromFile():
    code_location = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(code_location, 'input.txt')
    i = 0
    totalCities = 0
    with open(input_file, 'r') as file:
        for line in file:
            if(totalCities == 0):
                totalCities = int(line.strip())
                cityList = np.zeros((totalCities, 3), dtype=int)
                if(totalCities <= 5):
                    shortFlag = 1
            else:
                x, y, z = map(int, line.split())
                cityList[i] = np.array([x, y, z])
                i += 1

    return totalCities, cityList 

totalBreedingPopulation = 100
MutationRate = 4 # 10% mutation rate
TotalGenerations = 200
howManyParts = 2

totalCities, cityList = readFromFile()
halfGenePool = totalCities // howManyParts
distance_lookup = {}

if shortFlag == 1:
    for i in range(len(cityList)):
        for j in range(i + 1, len(cityList)):  
            point1 = tuple(cityList[i])  
            point2 = tuple(cityList[j]) 
            distance = np.linalg.norm(cityList[i] - cityList[j])
            forward_key = point1 + point2
            backward_key = point2 + point1
            distance_lookup[forward_key] = distance
            distance_lookup[backward_key] = distance
    

def tuningParameters():
    global totalBreedingPopulation, MutationRate, TotalGenerations, howManyParts
    if args['bpop']:
        totalBreedingPopulation = int(args['bpop'])
    if args['mr']:
        MutationRate = int(args['mr'])
    if args['mpop']:
        TotalGenerations = int(args['mpop'])
    if args['part']:
        howManyParts = int(args['part'])

tuningParameters()

bestRank = 0
bestPath = np.zeros((totalCities, 3), dtype=int)

def debugging(integer, listOfPaths=None):
    for j in range(totalBreedingPopulation):
        if np.array_equal(np.sort(cityList.flat), np.sort(listOfPaths[j].flat)) == False:
            print("False", integer)
            break

def debugging2(integer, specificPath=None):
    if np.array_equal(np.sort(cityList.flat), np.sort(specificPath.flat)) == False:
        print("False", integer)

for i in range(len(cityList)):
    for j in range(i + 1, len(cityList)):  
        point1 = tuple(cityList[i])  
        point2 = tuple(cityList[j]) 
        distance = np.linalg.norm(cityList[i] - cityList[j])
        forward_key = point1 + point2
        backward_key = point2 + point1
        distance_lookup[forward_key] = distance
        distance_lookup[backward_key] = distance

def CreateInitialPopulation(cityList):
    initial_population = np.zeros((totalBreedingPopulation, len(cityList), cityList.shape[1]), dtype=cityList.dtype)
    initial_population[0] = np.array([cityList])

    sorted_indices = np.lexsort((cityList[:, 2], cityList[:, 1], cityList[:, 0]))
    cityList = cityList[sorted_indices]
    initial_population[1] = np.array([cityList])
    
    sorted_indices = np.lexsort((cityList[:, 2], cityList[:, 0], cityList[:, 1]))
    cityList = cityList[sorted_indices]
    initial_population[2] = np.array([cityList])
    
    sorted_indices = np.lexsort((cityList[:, 1], cityList[:, 0], cityList[:, 2]))
    cityList = cityList[sorted_indices]
    initial_population[3] = np.array([cityList])
    
    sorted_indices = np.lexsort((cityList[:, 1], cityList[:, 2], cityList[:, 0])) 
    cityList = cityList[sorted_indices]
    initial_population[4] = np.array([cityList])
    
    sorted_indices = np.lexsort((cityList[:, 0], cityList[:, 2], cityList[:, 1])) 
    cityList = cityList[sorted_indices]
    initial_population[5] = np.array([cityList])
    
    sorted_indices = np.lexsort((cityList[:, 0], cityList[:, 1], cityList[:, 2])) 
    cityList = cityList[sorted_indices]
    initial_population[6] = np.array([cityList])

    for i in range(totalBreedingPopulation-7):
        cityList = np.random.permutation(cityList)
        initial_population[i+7] = np.array([cityList])

    return initial_population

listOfPaths = CreateInitialPopulation(cityList)

def CalculateFitness(listOfPaths, start=0, RankedScore=None):
    if RankedScore is None:
        RankedScore = np.zeros((totalBreedingPopulation, 1))
    else:
        RankedScore[start:] = 0

    for i in range(start, totalBreedingPopulation):
        sum = 0
        for j in range(2, totalCities):
            point1 = tuple(listOfPaths[i][j])  
            point2 = tuple(listOfPaths[i][j-1]) 
            sum += distance_lookup[point1 + point2]
        point1 = tuple(listOfPaths[i][totalCities-1])  
        point2 = tuple(listOfPaths[i][0]) 
        sum += distance_lookup[point1 + point2]

        RankedScore[i] = sum

    sorted_indices = np.argsort(RankedScore, axis=None)
    sorted_RankList = RankedScore[sorted_indices]
    sorted_listOfPaths = listOfPaths[sorted_indices]  

    return sorted_RankList, sorted_listOfPaths

RankedScoreOfDistances, listOfPaths = CalculateFitness(listOfPaths)

ElitePopulation = totalBreedingPopulation // 2

bestPath = listOfPaths[0]
bestRank = RankedScoreOfDistances[0]

def reproduction(firstParent, secondParent, childStart, childEnd):  
    createdChild = np.zeros((totalCities, 3), dtype=cityList.dtype)

    for i in range(childStart, childEnd):
        createdChild[i] = firstParent[i]  
    
    parent_city_tuples = [tuple(city) for city in secondParent]  
    child_city_tuples = [tuple(city) for city in createdChild[childStart:childEnd]]

    leftOver = [city for city in parent_city_tuples if city not in child_city_tuples]

    indexLeftover = 0
    for i in range(totalCities):
        if i < childStart or i >= childEnd:
            createdChild[i] = leftOver[indexLeftover]
            indexLeftover += 1

    return createdChild

def mutation(selectedPath, mutationRate):
    for i in range(totalCities-1):
        if np.random.randint(100) < mutationRate:
            selectedPath[[i, i+1]] = selectedPath[[i+1,i] ]
    #debugging2(69, selectedPath)    
    if np.random.randint(20)%19 == 0:
        selectedPath[[0,totalCities-1]] = selectedPath[[totalCities-1,0]]
    #debugging2(70, selectedPath)
    return selectedPath

def NextGeneration():
    New_Population = np.zeros((totalBreedingPopulation, len(cityList), cityList.shape[1]), dtype=cityList.dtype)

    for i in range(ElitePopulation):
        New_Population[i] = listOfPaths[i]

    for i in range(ElitePopulation, totalBreedingPopulation):
        firstParent, secondParent = sorted(np.random.choice(range(ElitePopulation), 2, replace=False))
        firstSelected = New_Population[firstParent]  
        secondSelected = New_Population[secondParent]  

        childStart = np.random.randint(0, halfGenePool-1)
        childEnd = childStart + halfGenePool

        createdChild = reproduction(firstSelected, secondSelected, childStart, childEnd)    
        New_Population[i] = createdChild   

    for i in range(ElitePopulation, totalBreedingPopulation):
        New_Population[i] = mutation(New_Population[i], MutationRate)
    return New_Population

score = 0

for i in range(TotalGenerations):
    listOfPaths = NextGeneration()
    RankedScoreOfDistances, listOfPaths = CalculateFitness(listOfPaths, ElitePopulation, RankedScoreOfDistances)

    if RankedScoreOfDistances[0] < bestRank:
        bestRank = RankedScoreOfDistances[0]
        bestPath = listOfPaths[0]

def write_output_to_file(bestRank, bestPath):
    code_location = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(code_location, 'output.txt')

    with open(output_file, 'w') as file:
        file.write(f"{int(bestRank[0])}\n")
        
        for city in bestPath:
            file.write(f"{city[0]} {city[1]} {city[2]}\n")
        
        start_city = bestPath[0]
        file.write(f"{start_city[0]} {start_city[1]} {start_city[2]}\n")

write_output_to_file(bestRank, bestPath)

print(bestRank)

code_location = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(code_location, 'log.txt')

with open(output_file, 'a+') as file:
    file.write(f"{int(bestRank[0])} - ")
    if args['bpop']:
        file.write(f"BPop:{totalBreedingPopulation}")
    if args['mr']:
        file.write(f"MRate:{MutationRate}")
    if args['mpop']:
        file.write(f"Generations:{TotalGenerations}")
    if args['part']:
        file.write(f"Divisions:{howManyParts}")

    file.write(f"\n")

