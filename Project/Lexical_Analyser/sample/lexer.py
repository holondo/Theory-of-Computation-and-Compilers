import string
from TransitionTable import TransitionTable
from symbol_token import TableOfSymbols

class lexer:
    tableForTransitions = ""
    tableForSymbols = ""
    currentState = ""

    def __init__(self):
        self.tableForTransitions = TransitionTable()
        self.tableForSymbols = TableOfSymbols()
        self.currentState = '0'

    def lexicalAnalyzer(self, strToProcess):
        self.currentState = 0
        readStr = ""

        for i in strToProcess:
            character = i
            readStr += i
            if(i == " " or i == "\n" or i == "\t"):
                character = "blank"
            if(i.isnumeric()):
                character = "digit"
            else:
                if(i in list(string.ascii_lowercase) or i in list(string.ascii_uppercase)):#if current character is in the alphabet
                    character = "alpha"

            self.currentState = self.tableForTransitions.transition(self.currentState, str(character))
            
            if(self.currentState == '-'):
                return {readStr : "ERROR_"}

            tokenToReturn = self.tableForTransitions.isFinal(self.currentState)
            if(tokenToReturn != "-"):
                #return to stream
                if(self.tableForTransitions.returnToStream(self.currentState)):
                    readStr = readStr[:-1] #slicing the last character
                    print(readStr)
                #se id, buscar na tabela
                if(tokenToReturn == "IDENTIFIER"):
                    if(self.tableForSymbols.inTableOfSymbols(readStr)):
                        tokenToReturn = self.tableForSymbols.inTableOfSymbols(readStr)

                return {readStr : tokenToReturn}
        
        return {readStr : "ERROR"}