import pandas as pd
import os

class TableOfSymbols:
    fileName = "symbols.csv"
    def __init__(self):
        filePath = os.path.join(os.path.dirname(__file__), self.fileName)
        self.table = pd.read_csv(filePath, index_col = 'Name')

    def inTableOfSymbols(self, strToVerify):
        try:            
            toReturn = self.table.loc[strToVerify]['Token']
        except:
            toReturn = ""
        
        return toReturn
