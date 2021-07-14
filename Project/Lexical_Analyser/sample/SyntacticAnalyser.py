from .lexer import Lexer

class SyntacticAnalyser:
    symb = None
    def __init__(self):
        self.currentLine = 1;
        self.__originalProgram__ = ""
        self.strProgram = ""
        self.lexer = Lexer()
        self.errors = list()
    
    def loadNextSymbol(self):
        self.symb = self.lexer.lexicalAnalyzer(self.strProgram)# = (symbol,token)
        self.strProgram = self.strProgram[len(self.symb[0]):]#slicing the already processed part of string

        if self.symb[1] == 'BLANK_SPACE':
            if self.symb[0] == "\n":
                self.currentLine += 1
            self.loadNextSymbol()
    
    def analyse(self,strProgram):
        if not isinstance(strProgram, str):
            self.errors.append("Arquivo com problemas.\n")
            return 

        self.__originalProgram__ = strProgram
        self.strProgram = strProgram

        self.loadNextSymbol()

        self.program_production()#primeira regra de producao

        if self.strProgram == "" and len(self.errors) == 0:
            self.errors.append("Compilação terminada com sucesso")