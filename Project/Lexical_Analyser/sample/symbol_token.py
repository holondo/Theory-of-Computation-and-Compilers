import pandas as pd

class TableOfSymbols:
    fileName = "symbols.csv"
    def __init__(self):
        self.table = pd.read_csv(self.fileName, index_col = 'Nome')

    def inTableOfSymbols(self, strToVerify):
        try:            
            toReturn = self.table.loc[strToVerify]['Retorno']
        except:
            toReturn = ""
        
        return toReturn
