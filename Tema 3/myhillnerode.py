from operator import ne
from sympy import false, true


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
    print("Invalid DFA")
else:
    
    matrix = [[0 for i in range(len(states))] for j in range(len(states))]
        
    for i in range(1,len(matrix)):
        for j in range(0, i):
            qi = 'q'+str(i)
            qj= 'q'+str(j)
            if (qi in final_states and qj not in final_states) or (qi not in final_states and qj in final_states):
                matrix[i][j] = 1
    
    myhillnerode_transitions = [[0 for j in range(len(sigma))] for i in range(len(states))]
    
    for i in range(len(transitions_matrix)):
        for j in range(len(transitions_matrix)):
            if len(transitions_matrix[i][j]) != 0:
                for k in range(len(transitions_matrix[i][j])):
                    x = sigma.index(transitions_matrix[i][j][k])
                    myhillnerode_transitions[i][x] = j

    ok = false
    while(ok == false):
        ok = true
        for i in range(1, len(matrix)):
            for j in range(0,i):
                if matrix[i][j] == 0:
                    x = myhillnerode_transitions[i][0]
                    y = myhillnerode_transitions[i][1]
                    z = myhillnerode_transitions[j][0]
                    w = myhillnerode_transitions[j][1]

                    if matrix[x][z] == 1 or matrix[y][w] == 1 or matrix[z][x] == 1 or matrix[w][y] == 1:
                        matrix[i][j] = 1
                        ok = false
    counter = int(states[len(states)-1][1]) + 1
    final_state_ok = false
    counter_final_state = -1
    counter_start_state = -1
    
    visited = [False for x in range(len(states))]
    
    dict_new_states = {}
    new_nodes = 0
    for i in range(1, len(matrix)):
        for j in range(0,i):
            if matrix[i][j] == 0:
                visited[i] = visited[j] = True
                x = 'q'+str(i)
                y = 'q'+str(j)
                if x in final_states or y in final_states:
                    if counter_final_state == -1:
                        dict_new_states['q'+str(counter)] = [(i,j)]
                        counter_final_state = counter
                        counter = counter + 1
                    else:
                        dict_new_states['q'+str(counter_final_state)].append((i,j))
                elif x in start_state or y in start_state:
                    if counter_start_state == -1:
                        dict_new_states['q'+str(counter)] = [(i,j)]
                        counter_start_state = counter
                        counter = counter + 1
                    else:
                        dict_new_states['q'+str(counter_start_state)].append((i,j))
                else:
                    dict_new_states['q'+str(counter)] = [(i,j)]
                    counter = counter + 1
    new_states = []
    old_states = []
    used_states = []
    for i in range(len(visited)):
        if visited[i] == False:
            new_states.append('q'+str(i))
            old_states.append('q' + str(i))
        else:
            used_states.append('q' + str(i))
    if counter_start_state == -1:
        x = start_state[0]
    else:
        x = 'q'+str(counter_start_state)
    if counter_final_state == -1:
        y = final_states[0]
    else:
        y = 'q'+str(counter_final_state)
    new_start_state = x
    new_final_state = y
    new_states.append(x)
    new_states.append(y)
    
    new_dfa = {}
    new_dfa[x] = []
    
    for i in dict_new_states.keys():
        if i != x and i != y:
            new_dfa[i] = []
    
    for i in new_states:
        if i != x and i != y:
            new_dfa[i] = []
    new_dfa[y] = []
    
    lista_stari_noi = []
    for i in dict_new_states.keys():
        lista_stari_noi.append(i)
    
    for i in range(len(visited)):
        if visited[i] == False:
            for j in range(len(myhillnerode_transitions[0])):
                x = 'q'+str(myhillnerode_transitions[i][j])
                if x in old_states:
                    new_dfa['q'+str(i)].append(x)
                else:
                    y = myhillnerode_transitions[i][j]
                    for key in dict_new_states:
                        for k in range(len(dict_new_states[key])):
                            if dict_new_states[key][k][0] == y or dict_new_states[key][k][1] == y:
                                cheie = key
                    new_dfa['q'+str(i)].append(cheie)

    for key in dict_new_states:
        new_set_list = []
        for j in range(len(sigma)):
            new_set_aux = set()
            x = myhillnerode_transitions[dict_new_states[key][0][0]][j]
            y = myhillnerode_transitions[dict_new_states[key][0][1]][j]
            if x == y:
                z = 'q'+str(x)
                if z in old_states:
                    new_dfa[key].append(z)
                else:
                    cheie = 0
                    for keyy in dict_new_states:
                        for k in range(len(dict_new_states[keyy])):
                            if (dict_new_states[keyy][k][0] == x or dict_new_states[keyy][k][1] == x):
                                cheie = keyy
                    new_dfa[key].append(cheie)
            else:
                cheie = 0
                for keyy in dict_new_states:
                    for k in range(len(dict_new_states[keyy])):
                        if (dict_new_states[keyy][k][0] == x and dict_new_states[keyy][k][1] == y)or(dict_new_states[keyy][k][0] == y and dict_new_states[keyy][k][1] == x):
                            cheie = keyy
                new_dfa[key].append(cheie)


space = "    "               
print("#")
print("# comment lines (skip them)")
print("#")
print("Sigma:")
for i in sigma:
    print(space + str(i))
print("End")
print("#")
print("# comment lines (skip them)")
print("#")
print("States:")
for i in new_states:
    if i == new_start_state:
        print(space+str(i)+ ' ,S')
    elif i == new_final_state:
        print(space+str(i)+ ' ,F')
    else:
        print(space+str(i))
print("End")
print("#")
print("# comment lines (skip them)")
print("#")
print("Transitions:")
for key in new_dfa:
    for i in range(len(new_dfa[key])):
        print(space+str(key) +", "+str(sigma[i])+", "+str(new_dfa[key][i]))
    