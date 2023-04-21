FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"
FILE_LL = "ll.txt"

f = open(FILE_LR, "r")
data = f.readline()
data = data.strip()
data = data.split(";")
multiplier = len(data) - 1
variables = f.readline()
variables = variables.split(";")
for i in range(len(variables)):
    variables[i] = variables[i].strip()

variables.pop(0)
stateNum = len(f.readlines())
f.close()
f2 = open(FILE_LR, "r")
f2.readline()
f2.readline()
states = f2.readlines()
f2.close()
loopBool = True
loopVar = 0
f3 = open(FILE_INPUT, "r")
inputs = f3.readlines()
f3.close()
currentInputLine = inputs[2].split()
currentInput = currentInputLine[1]
currentInput = currentInput[1:]
print("Processing input string", currentInput, "for LR(1) parsing table.")
print("NO    |    STATE STACK    |    READ    |    INPUT    |    ACTION")
indexer = 0
stateDict = {"blank": 1}
stateStack = [1]
counter = 1
while loopBool:
    currentState = states[loopVar].split(";")
    currentVariable = currentInput[indexer]
    print(counter,"    |", stateStack, (" " * (16 - (len(stateStack) * 3))), "|     ", currentVariable, "    |    ", currentInput,
          (" " * (4 - (len(currentInput)))), "  | ", end=" ")
    indexer += 1
    selector = -1
    counter += 1
    for i in range(len(variables)):
        if variables[i] == currentVariable:
            selector = i + 1
            break
    if currentState[selector] == "       ":
        print("REJECTED (", currentState[0], "does not have action/step for", currentVariable, ")")
        loopBool = False
    else:

        if currentState[selector].rfind("_") != -1:
            currentState[selector] = currentState[selector][currentState[selector].rfind("_") + 1:]
            loopVar = int(currentState[selector]) - 1
            stateDict[currentVariable] = loopVar + 1
            stateStack.append(loopVar + 1)
            print("Shift to", currentState[selector])
        elif currentState[selector] == "Accept":
            print("ACCEPTED")
            break
        else:
            rightSide = currentState[selector][currentState[selector].rfind("->") + 2:]
            rightSide = rightSide.strip()

            leftSide = currentState[selector][0:currentState[selector].rfind("->")]
            print("Reverse", leftSide, "->", rightSide)
            index = currentInput.rfind(rightSide)
            if index != -1:
                currentInput = currentInput.replace(rightSide, leftSide)
                if len(rightSide) == 1:
                    stateDict.pop(rightSide)
                    stateStack.pop()
                else:
                    for i in rightSide:
                        stateDict.pop(i)
                        stateStack.pop()

                indexer = currentInput.rfind(leftSide)

                loopVar = stateStack.pop() - 1
                stateStack.append(loopVar + 1)

            else:
                print("REJECTED (can't apply rule)")

                break
 

# LL part

def processInput(inputs):
    for i in range(len(inputs)):
        inputs[i] = inputs[i].replace(" ", "")
        inputs[i] = inputs[i].rstrip()
    return inputs

def parseTable(FILE_LL):
    tableDict = {}
    llFile = open(FILE_LL, "r")
    llData = llFile.readlines()
    llFile.close()
    for i in range(len(llData)):
        llData[i] = llData[i].rstrip()
        llData[i] = llData[i].split(";")
        
        
    # prepare table as dict e.g. Eid = E -> TA 
    for i in range(1, len(llData)):
        for j in range(1, len(llData[0])):
            if((not llData[i][j].isspace()) and llData[i][j] != ""):
                tableDict[(llData[i][0] + llData[0][j]).replace(" ", "")] = llData[i][j].strip()
    return tableDict



def ll(tableDict, inputs):
    for i in range(len(inputs)):
        if(inputs[i][:2] == "LL"):
            input = inputs[i].split(";")[1]
            # TODO : call LL function



postProcessInput = processInput(inputs)
tableDict = parseTable(FILE_LL)
ll(tableDict, inputs)
print(tableDict)


