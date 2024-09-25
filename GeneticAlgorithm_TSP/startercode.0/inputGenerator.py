import random
import os
import argparse

parser = argparse.ArgumentParser(description="Process some arguments.")

parser.add_argument('--fixedQuant', type=int, required=False, help='Fix Max Cities')
parser.add_argument('--maxValue', type=int, required=False, help='Max Value of the Coordinates')
parser.add_argument('--maxQuant', type=int, required=False, help='Max amount of cities')

args = vars(parser.parse_args())

MaxInputs = 5000
MaxCoordinate = 10000
initialCoordinate = 1000

if args['maxValue']:
    MaxCoordinate = args['maxValue']

if args['maxQuant']:
    MaxInputs = args['maxQuant']

#Input generator of the form where the first line is a random positive integer N between 1 - the 32 bit integer limit and the next N lines are the 3d coordinates of the cities seperated by a space
def inputGenerator():
    N = random.randint(1, MaxInputs)
    return N

#Code to output this to a file and call it input.txt

def write_output_to_file():
    code_location = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(code_location, 'input.txt')
    if args['fixedQuant']:
        N = args['fixedQuant']
    else:
        N = inputGenerator()

    with open(output_file, 'w') as file:
        file.write(f"{int(N)}\n")
        for _ in range(N):
            file.write(f"{random.randint(initialCoordinate, MaxCoordinate)} {random.randint(initialCoordinate, MaxCoordinate)} {random.randint(initialCoordinate, MaxCoordinate)}\n")

write_output_to_file()

code_location = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(code_location, 'log.txt')

with open(output_file, 'a+') as file:
    file.write(f"New Set Generated \n")
