from xml.etree.ElementTree import ElementTree

from sqlalchemy import true


file_name, input_name = map(str, input().split())

f = open(input_name, "r")

counter = 0
terminals = []
nonterminals = []
final_states = []
start_state = []
P = []

transitions = []

valid_CFG = True

CFG = {}

f.readline()
f.readline()
f.readline()

for line in f:
    line = line.strip("\n")
    if line == "Terminals:":
        letter = f.readline().strip("\n")
        letter = letter.strip(" ")
        while letter != "End":
            terminals.append(letter)
            letter = f.readline().strip("\n")
            letter = letter.strip(" ")
        counter = counter + 1
        if counter != 4:
            f.readline()
            f.readline()
            f.readline()
    elif line == "Non-Terminals:":
        letter = f.readline().strip("\n")
        letter = letter.strip(" ")
        while letter != "End":
            nonterminals.append(letter)
            letter = f.readline().strip("\n")
            letter = letter.strip(" ")
        counter = counter + 1
        if counter != 4:
            f.readline()
            f.readline()
            f.readline()
    elif line == "P:":
        command = f.readline().strip("\n")
        command = command.strip(" ")
        while command != "End":
            P.append(command)
            test = command.split("->")
            if(len(test[0]) == 1):
                comanda = test[1].split("|")
                CFG[test[0]] = comanda
            command = f.readline().strip("\n")
            command = command.strip(" ")
        counter = counter + 1
        if counter != 4:
            f.readline()
            f.readline()
            f.readline()
    elif line == "Start:":
        letter = f.readline().strip("\n")
        letter = letter.strip(" ")
        while letter != "End":
            start_state.append(letter)
            letter = f.readline().strip("\n")
            letter = letter.strip(" ")

if(len(start_state) != 1):
    valid_CFG = False
else:
    for key in CFG.keys():
        if key not in nonterminals:
            valid_CFG = False
    for element in CFG:
        for i in CFG[element]:
            for j in i:
                if (j not in terminals) and (j not in nonterminals):
                    valid_CFG = False
if valid_CFG == True:
    print("Valid CFG")
else:
    print("Invalid CFG")