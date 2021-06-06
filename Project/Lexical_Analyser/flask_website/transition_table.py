import pandas as pd 

class TransitionTable:
    def __init__(self,csvFile):
        self.df = pd.read_csv(csvFile)

    def transition(self,currentState, symbol):
        match = self.df.iloc[currentState][symbol]
        return match
