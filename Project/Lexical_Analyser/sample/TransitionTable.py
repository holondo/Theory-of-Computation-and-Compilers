import csv
import os

class TransitionTable:
    fileName = "TTable.csv"
    state = [] #List of dictionary shaped states

    def __init__(self):        
        stateTransitions = {}
        filePath = os.path.join(os.path.dirname(__file__), self.fileName) 
        with open(filePath, 'r') as fp:
            CSVReader = csv.reader(fp, delimiter='|')
            lines = list(CSVReader)

            for i in range(1, len(lines)): #For each state in csv, make a dictionary
                for j in range(len(lines[0])):
                    stateTransitions[lines[0][j]] = lines[i][j]

                self.state.append(stateTransitions.copy())
                stateTransitions.clear();
    
    def transition(self, currentState, symbol ):
        try:
            toReturn = self.state[currentState][symbol]
        except:
            toReturn = self.state[currentState]['blank']
        return toReturn

    def isFinal(self, currentState):
        return self.state[currentState]["isfinal"]

    def returnToStream(self, currentState):
        return self.state[currentState]["returnToStream"] == "true"