import string

from numpy import character
from .TransitionTable import TransitionTable
from .symbol_token import TableOfSymbols

def cathegorizeChar(character):
    if(character == " " or character == "\n" or character == "\0"):
        return "blank"
    elif(character in list(string.digits)):
        return "digit"
    elif(character in list(string.ascii_letters)):#if current character is in the alphabet
        return "alpha"
    elif character in ['.',';','=','<','>','(',')',':','+','-','*','{','}']:
        return character

    else: return "NOT_RECOGNIZED"

class Lexer:
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
            readStr += i
            character = cathegorizeChar(i)

            try:
                self.currentState = self.tableForTransitions.transition(self.currentState, character)
            except:
                return [readStr , "ERROR_"]

            tokenToReturn = self.tableForTransitions.isFinal(self.currentState) #if current state isn t final token = '-'
            if(tokenToReturn != "-"):
                #return to stream
                if(self.tableForTransitions.returnToStream(self.currentState)):
                    readStr = readStr[:-1] #slicing the last character
                    print(readStr)

                #se id, buscar na tabela
                if(tokenToReturn == "IDENTIFIER"):
                    if(self.tableForSymbols.inTableOfSymbols(readStr)):
                        tokenToReturn = self.tableForSymbols.inTableOfSymbols(readStr)
                
                return [readStr, tokenToReturn]
        
        return [readStr , "ERROR"]