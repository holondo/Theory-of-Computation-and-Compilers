import pandas as pd


class TransitionTable:
    def __init__(self):
        self.df = pd.read_csv('TTable.csv')

    def transition(self, currentState, symbol):
        match = self.df.iloc[currentState][symbol]
        return match
