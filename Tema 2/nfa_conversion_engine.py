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
            if (len(lista_state) == 1):
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

transitions_matrix = [[None for i in range(len(states))] for j in range(len(states))]

for i in range(len(transitions)):
    if valid_NFA == True:
        a, b, c = transitions[i].split(",")
        b = b.strip(" ")
        c = c.strip(" ")
        if a not in states or c not in states or b not in sigma:
            valid_NFA = False
        else:
            x = states.index(a)
            y = states.index(c)
            transitions_matrix[x][y] = b

myhillnerode_transitions = [[[] for j in range(len(sigma))] for i in range(len(states))]

for i in range(len(transitions_matrix)):
    for j in range(len(transitions_matrix)):
        if transitions_matrix[i][j] :
            for k in range(len(transitions_matrix[i][j])):
                x = sigma.index(transitions_matrix[i][j][k])
                myhillnerode_transitions[i][x].append(j+1)



    #continutul este practic start state, va trebui sa iau ala minus 1
dic={}
ls=[]
for i in range(len(myhillnerode_transitions)):
      ls.append([i+1,myhillnerode_transitions[i]])

ls_nusterge=[]
lista_afostdeja=[]
contor=len(states)
dictionar_indici={}
for linie in ls:

    for element in linie[1]:
        if (len(element) > 1):
                 contor+=1
                 dictionar_indici[tuple(element)]=contor
                 ls_nusterge.append(linie[0])
                 x=[[] for i in range(len(sigma))]
                 for ab in element:
                     for ac in range(len(sigma)):
                         x[ac]+=myhillnerode_transitions[ab-1][ac]
                 ls.append([tuple(element),x])

                 for y in element:
                     lista_afostdeja.append(y)

for linie in ls:
    ok=0
    for x in lista_afostdeja:
        if linie[0]==x:
            ok+=1
    if ok==0:
        dic[linie[0]]=linie[1]
ultimalista=[]
for lista in dic:

    if type(lista) is tuple:
       ultimalista.append((lista,[x for x in lista]))

for lista in dic:
    for i in range (len(dic[lista])):

        for j in range(len(ultimalista)):
            for element in ultimalista[j][1]:
              for elem in dic[lista][i]:
                if elem==element:

                   dic[lista][i]=ultimalista[i][0]

final_states1=[]
lista_starifinale=[]
for i in range(len(final_states)):
    final_states[i]=int(final_states[i][1])
for x in dictionar_indici:

    if type(x) is tuple:
        for xx in x:
           for y in final_states:

              if y==xx:

                final_states1.append(dictionar_indici[x])
    elif x in final_states:
        final_states1.append(x)



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
for i in dic:
        if (i==int(start_state[0][1])):
          print(space + "q"+str(i) + ' ,S')
        elif(i in final_states1 or dictionar_indici[i] in final_states1):
            print(space + "q" + str(dictionar_indici[i]) + ' ,F')
        elif i in dictionar_indici:
            print(space + "q"+str(dictionar_indici[i]))
        else:
            print(space + "q"+str(i))
        # elif
        # print(space + str(i) + ' ,F')
print("End")
print("#")
print("# comment lines (skip them)")
print("#")
print("Transitions:")

for i in dic:
    if type(i) is not tuple:
       for j in range(len(sigma)):
           if dic[i][j]:
               if type((dic[i][j])) is tuple:
                   print(space + "q" + str(i),sigma[j],"q"+str(dictionar_indici[dic[i][j]]))

               else:
                   print(space + "q" + str(i) ,sigma[j] , "q"+str(i))

    else:
        if type(i) is tuple:
            for j in range(len(dic[i])):
                if dic[i][j]:
                    if type((dic[i][j])) is tuple:
                        print(space + "q" + str(dictionar_indici[dic[i][j]]) ,sigma[j] , "q"+str(dictionar_indici[dic[i][j]]))

                    else:
                        print(space + "q" + str(dictionar_indici[dic[i][j]]) ,sigma[j] , "q"+str(i))