import csv
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.io.parsers import read_csv


class TransitionTable:

    fileName = "TTable.csv"
    state = []  # List of dictionary shaped states

    def __init__(self):
        stateTransitions = {}

        with open(self.fileName, 'r') as fp:
            CSVReader = csv.reader(fp)
            lines = list(CSVReader)

            for i in range(1, len(lines)):  # For each line in csv, make a dictionary
                for j in range(len(lines[0])):
                    stateTransitions[lines[0][j]] = lines[i][j]

                self.state.append(stateTransitions.copy())
                stateTransitions.clear()

    def transition(self, currentState, symbol):
        toReturn = self.state[currentState][symbol]
        return toReturn


class TransitionPd:
    def __init__(self):
        self.df = pd.read_csv('TTable.csv')

    def transition(self, currentState, symbol):
        match = self.df.iloc[currentState][symbol]
        return match
