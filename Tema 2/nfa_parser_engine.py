file_name, input_name = map(str, input().split())

f = open(input_name, "r")

counter = 0
sigma = []
states = []
final_states = []
start_state = []

transitions = []

valid_NFA = True

f.readline()
f.readline()
f.readline()

for line in f:
    line = line.strip("\n")
    if line == "Sigma:":
        letter = f.readline().strip("\n")
        letter = letter.strip(" ")
        while letter != "End":
            sigma.append(letter)
            letter = f.readline().strip("\n")
            letter = letter.strip(" ")
        counter = counter + 1
        if counter != 3:
            f.readline()
            f.readline()
            f.readline()
    elif line == "States:":
        state = f.readline().strip("\n")
        state = state.strip(" ")
        while state != "End":
            lista_state = state.split(",")
            if(len(lista_state) == 1):
                states.append(state)
            else:
                lista_state[0] = lista_state[0].strip(" ")
                if len(lista_state[1]) > 1:
                    final_states.append(lista_state[0])
                    start_state.append(lista_state[0])
                elif lista_state[1] == "F":
                    final_states.append(lista_state[0])
                else:
                    start_state.append(lista_state[0])
                states.append(lista_state[0])
            state = f.readline().strip("\n")
            state = state.strip(" ")
        counter = counter + 1
        if counter != 3:
            f.readline()
            f.readline()
            f.readline()
    elif line == "Transitions:":
        transition = f.readline().strip("\n")
        transition = transition.strip(" ")
        while transition != "End":
            transitions.append(transition)
            transition = f.readline().strip("\n")
            transition = transition.strip(" ")
        counter = counter + 1
        if counter != 3:
            f.readline()
            f.readline()
            f.readline()

transitions_matrix = [[[] for i in range(len(states))] for j in range(len(states))]

for i in range(len(transitions)):
    if valid_NFA == True:
        a,b,c = transitions[i].split(",")
        b = b.strip(" ")
        c = c.strip(" ")
        if a not in states or c not in states or b not in sigma:
            valid_NFA = False
        else:
            x = states.index(a)
            y = states.index(c)
            transitions_matrix[x][y].append(b)

if len(start_state) != 1:
    valid_NFA = False
elif len(final_states) == 0:
    valid_NFA = False
elif start_state[0] not in states:
    valid_NFA = False   

if valid_NFA == False:
    print("Invalid NFA")
else:
    print("Valid NFA")