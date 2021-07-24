import string

from .TransitionTable import TransitionTable
from .symbol_token import TableOfSymbols

def cathegorizeChar(character):
    # Defines character inside automaton's alphabet
    if(character == " "  or character == "\0" or character == "\t"):
        return "blank"
    if(character == "\n"):
        return "newLine"
    elif(character in list(string.digits)):
        return "digit"
    elif(character in (list(string.ascii_letters)) + ['_']):#if current character is in the alphabet
        return "alpha"
    elif character in ['.',';','=','<','>','(',')',':','+','-','*','{','}',',','/','\n']:
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

            self.currentState = self.tableForTransitions.transition(self.currentState, character)
            try:
                self.currentState = int(self.currentState)
            except:
                if(self.currentState == '-'):
                    return [readStr + self.currentState , "ERROR_"]
                else:
                    return [readStr , self.currentState]

            tokenToReturn = self.tableForTransitions.isFinal(self.currentState)#if current state isn t final token == '-'
            if(tokenToReturn != "-"):
                #return to stream
                if(self.tableForTransitions.returnToStream(self.currentState)):
                    readStr = readStr[:-1] #slicing the last character

                #se id, buscar na tabela
                if(tokenToReturn == "IDENTIFIER"):
                    if(self.tableForSymbols.inTableOfSymbols(readStr)):
                        tokenToReturn = self.tableForSymbols.inTableOfSymbols(readStr)
                
                return [readStr, tokenToReturn]
        
        return [readStr , "ERROR"]