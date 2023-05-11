FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"
FILE_LL = "ll.txt"

f = open(FILE_LR, "r")
data = f.readline()
data = data.strip()
data = data.split(";")

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


f3 = open(FILE_INPUT, "r")
inputs = f3.readlines()
f3.close()


for i in range(len(inputs)):
    currentInputLine = inputs[i].split()
    if currentInputLine[0] == "LR":
        currentInput = currentInputLine[1]
        currentInput = currentInput[1:]
        loopBool = True
    else:
        loopBool = False
    if loopBool:
        print("\nProcessing input string", currentInput, "for LR(1) parsing table.")
        print("NO    |    STATE STACK    |    READ    |    INPUT    |    ACTION")
    indexer = 0

    stateStack = [1]
    counter = 1
    loopVar = 0
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
        if currentState[selector][0] == ' ':
            print("REJECTED (", currentState[0], "does not have action/step for", currentVariable, ")")
            loopBool = False
        else:

            if currentState[selector].rfind("_") != -1:
                currentState[selector] = currentState[selector][currentState[selector].rfind("_") + 1:]
                loopVar = int(currentState[selector]) - 1

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
                        stateStack.pop()
                    else:
                        for i in rightSide:
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

def parseOperators(FILE_LL):
    llFile = open(FILE_LL, "r")
    llData = llFile.readlines()
    llFile.close()
    ops = llData[0].rstrip().split(";")
    operators = []
    for i in range(1, len(ops)):
        operator = ops[i].replace(" ", "")
        operators.append(operator)

    return operators

def parseActions(FILE_LL):
    llFile = open(FILE_LL, "r")
    llData = llFile.readlines()
    llFile.close()
    actions = []
    for i in range(1, len(llData)):
        actions.append(llData[i].split(";")[0].replace(" ", ""))
    return actions


def parseTable(FILE_LL):
    tableDict = {}
    llFile = open(FILE_LL, "r")
    llData = llFile.readlines()
    llFile.close()
    for i in range(len(llData)):
        llData[i] = llData[i].rstrip()
        llData[i] = llData[i].split(";")

    operatorList = []
    # prepare table as dict e.g. Eid = E -> TA 
    for i in range(1, len(llData)):
        for j in range(1, len(llData[0])):
            if((not llData[i][j].isspace()) and llData[i][j] != ""):
                tableDict[(llData[i][0] + llData[0][j]).replace(" ", "")] = llData[i][j].strip()

    return tableDict


def derivate(tableDict, inputs, operators, actions):
    for i in range(len(inputs)):
        if(inputs[i][:2] == "LL"):
            input = inputs[i].split(";")[1]
            print("\nProcessing input string", input, "for LL(1) parsing table.")
            ll(tableDict, input, operators, actions)

def compare(smaller, bigger, numberOfChar):
    for i in range(numberOfChar):
        if(smaller[i] != bigger[i]):
            return False
    return True


def ll(tableDict, input, operators, actions):
    no = 0
    stack = []
    stack.append('$')


    maxOperatorLength = 0
    for i in range(len(operators)):
        if((currentOpLen := len(operators[i])) > maxOperatorLength):
            maxOperatorLength = currentOpLen

    loopBool = True
    print()
    print("NO    |          STACK          |    INPUT    |    ACTION")
    while loopBool:
        no += 1
        print(no, "    |", stack, (" " * (20 - (len(stack) * 5))), "|     ", input,(" " * (4 - (len(input)))), "  | ", end=" ")


        # checking input value to validate
        while True:
            if (no != 1):
                stackV = stack.pop()
            else:
                stackV = actions[0]
            inpV = input[0]
            if(inpV == "$" and stackV == "$"):
                print("ACCEPTED")
                loopBool = False
                break
            if(stackV == "$" and inpV != "$"):
                print("REJECTED STACK IS EMPTY BUT INPUT IS NOT")
                loopBool = False
                break
            while (inpV not in operators):
                i = 1
                if(len(inpV) == maxOperatorLength and inpV not in operators):
                    print("REJECTED INPUT IS NOT VALID")
                    return
                else:
                    inpV += input[i]
            # checking stack value to validate
            while True:
                if(stackV in actions):
                    break
                elif(stackV == inpV):
                    break
                elif(stackV > inpV and stackV not in actions):
                    print("REJECTED STACK IS NOT VALID")
                    return
                else:
                    stackV += stack.pop()

            if(inpV in operators and stackV in operators):
                input = input[len(inpV):]
            else:
                break


        if(inpV in operators and stackV in operators and inpV != stackV):
            print("REJECTED STACK AND INPUT ARE DIFFERENT AND BOTH ARE OPERATORS")
            return


        if(inpV in operators and stackV in actions):
            dictKey = stackV + inpV
            if(dictKey not in list(tableDict.keys())):
                print("REJECTED INVALID TABLE INPUT")
                break
            action = tableDict[dictKey]

            print(action)
            actionD = action.split("->")[1]
            if(actionD != "ϵ"):

                actionList = []
                for i in range(len(actionD)):
                    if(actionD[i] in actions or actionD[i] in operators):
                        actionList.append(actionD[i])
                    else:
                        for j in range(1, maxOperatorLength):
                            if(isOp := actionD[0:i + j]) in operators:
                                actionList.append(isOp)
                for i in range((actionListLen := len(actionList))):
                    stack.append(actionList[actionListLen - i - 1])

postProcessInput = processInput(inputs)
operators = parseOperators(FILE_LL)
actions = parseActions(FILE_LL)
# actionname + operator = action
tableDict = parseTable(FILE_LL)
derivate(tableDict, inputs, operators, actions)

