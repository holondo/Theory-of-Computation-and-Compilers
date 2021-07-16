from numpy import equal
from .lexer import Lexer

FILE_END = " "

class SyntacticAnalyser:
    symb = None
    def __init__(self):
        self.currentLine = 1;
        self.__originalProgram__ = ""
        self.errors = list()
        self.strProgram = ""
        self.lexer = Lexer()
    
    def programIsProcessed(self) -> bool:
        if self.strProgram == "": 
            return True
        return False

    def getCurrentToken(self) -> str:
        return self.symb[1]
    
    def getCurrentSymbol(self) -> str:
        return self.symb[0]
    
    ### Returns: true, if 
    def isCurrentToken(self, expectedToken) -> bool:
        return (self.getCurrentToken() == expectedToken)

    def loadNextSymbol(self):
        if not self.programIsProcessed():
            self.symb = self.lexer.lexicalAnalyzer(self.strProgram)# = (symbol,token)
            self.strProgram = self.strProgram[len(self.symb[0]):]#slicing the already processed part of string

            if self.getCurrentToken() == 'BLANK_SPACE':
                if '\n' in self.symb[0]:
                    self.currentLine += 1
                self.loadNextSymbol()
        
    def analyse(self,strProgram) -> list:
        if not isinstance(strProgram, str):
            self.errors.append("Arquivo com problemas.\n")
            return 

        self.__originalProgram__ = strProgram
        self.strProgram = strProgram
        self.strProgram += FILE_END

        self.loadNextSymbol()

        self.prod_Program()#primeira regra de producao

        if self.strProgram == FILE_END and len(self.errors) == 0:
            self.errors.append("Compilação terminada com sucesso")
        
        return self.errors

    
    def error(self, errorMessage, currentNext, productionNext) -> bool:
        if self.isCurrentToken("INCOMPLETE_FLOAT_ERROR"):
                self.errors.append(f"Erro léxico na linha {self.currentLine}: {self.symb}.")
        
        self.errors.append(f"Erro sintático na linha {self.currentLine}: {errorMessage}")

        if self.getCurrentToken() in currentNext:
            return True
        
        if self.getCurrentToken() in productionNext:
            return False

        while not self.programIsProcessed() and self.getCurrentToken() not in productionNext:
            if productionNext == FILE_END and self.getCurrentSymbol() == FILE_END:
                return False
            self.loadNextSymbol()
        
        return False
    
    def verifyNecessaryToken(self,expectedToken, errorMessage, tokenNext, ruleNext)-> bool:
        if self.getCurrentToken() in expectedToken:
                self.loadNextSymbol()
        else:
            if self.error(errorMessage, currentNext= tokenNext, productionNext= ruleNext) == False:
                return False
        return True
    
    def verifyPossibleToken(self,expectedToken, errorMessage, tokenNext, ruleNext)-> bool:
        if self.getCurrentToken() in expectedToken:
                self.loadNextSymbol()
        else:
            if self.error(errorMessage, currentNext= tokenNext, productionNext= ruleNext) == False:
                self.errors.pop()
                return False
        return True


    #|/|/|/|/|/|/| Production Rulez

    def prod_Program(self):
        if self.isCurrentToken("PROGRAM_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("Program esperado.", currentNext= "IDENTIFIER", productionNext= FILE_END) == False:
                return
        
        if self.isCurrentToken("IDENTIFIER"):
            self.loadNextSymbol()
        else:
            if self.error("Identificador do programa esperado.", currentNext= "SEMICOLON_SYMB", productionNext= FILE_END) == False:
                return
            
        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("; esperado.", currentNext= ["CONST_SYMB", "VAR_SYMB", "PROCEDURE_SYMB"], productionNext= FILE_END) == False:
                return

        self.prod_Body()

        if self.verifyNecessaryToken("DOT_SYMB", "Ponto final esperado.", FILE_END, FILE_END): return
        # if self.isCurrentToken("DOT_SYMB"):
        #     self.loadNextSymbol()
        # else:
        #     if self.error("Ponto final esperado.", currentNext= FILE_END, productionNext= FILE_END) == False:
        #         return
    
    def prod_Body(self):

        #-----DECLARATIONS
        self.prod_dc_c()
        while self.isCurrentToken("CONST_SYMB"):
            self.prod_dc_c()
            
        self.prod_dc_v()
        while self.isCurrentToken("VAR_SYMB"):
            self.prod_dc_v()

        self.prod_dc_p()
        while self.isCurrentToken("PROCEDURE_SYMB"):
            self.prod_dc_p()
        #-----DECLARATIONS END

        if self.isCurrentToken("BEGIN_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("begin esperado.", currentNext= ["WRITE_SYMB", "WHILE_SYMB", "IF_SYMB", "IDENTIFIER", "BEGIN","END_SYMB"], productionNext= "DOT_SYMB") == False:
                return

        #####TODO <COMANDOS>

        if self.isCurrentToken("END_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("End esperado.", currentNext= "DOT_SYMB", productionNext= "DOT_SYMB") == False:
                return
        
    def prod_dc_c(self):
        if self.isCurrentToken("CONST_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("const esperado.", currentNext= "IDENTIFIER", productionNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]) == False:
                self.errors.pop()
                return

        if self.isCurrentToken("IDENTIFIER"):
            self.loadNextSymbol()
        else:
            if self.error("Identificador de constante esperado.", currentNext= "EQUAL_SIGN", productionNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]) == False:
                return

        if self.isCurrentToken("EQUAL_SIGN"):
            self.loadNextSymbol()
        else:
            if self.error("Simbolo '=' esperado.", currentNext= ["UNSIGNED_INTEGER", "UNSIGNED_FLOAT"], productionNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]) == False:
                return
        
        if self.isCurrentToken("UNSIGNED_INTEGER") or self.isCurrentToken("UNSIGNED_FLOAT"):
            self.loadNextSymbol()
        else:
            if self.error("Valor numérico esperado.", currentNext= "SEMICOLON_SYMB", productionNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]) == False:
                return

        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("; esperado.", currentNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"], productionNext= ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]) == False:
                return
        
    
    def prod_dc_v(self):
        productionNext = ["VAR_SYMB","PROCEDURE_SYMB", "BEGIN_SYMB"]
        if self.isCurrentToken("VAR_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("var esperado.", currentNext= "IDENTIFIER", productionNext= productionNext) == False:
                self.errors.pop()
                return

        #<variaveis>
        if not self.prod_Variables(["COLON_SYMB"],productionNext):
            return
            
        if self.isCurrentToken("COLON_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("Dois pontos esperado.", currentNext= "TYPE_SYMB", productionNext= productionNext) == False:
                return
        
        if self.isCurrentToken("TYPE_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("Tipo esperado.", currentNext= "SEMICOLON_SYMB", productionNext= productionNext) == False:
                return
        
        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("; esperado.", currentNext= productionNext, productionNext= productionNext) == False:
                return

    def prod_dc_p(self):
        thisRulesNextSymbol  = ["PROCEDURE_SYMB", "BEGIN_SYMB"]
        if self.isCurrentToken("PROCEDURE_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("procedure esperado.", currentNext= "IDENTIFIER", productionNext = thisRulesNextSymbol) == False:
                self.errors.pop()
                return

        if self.isCurrentToken("IDENTIFIER"):
                self.loadNextSymbol()
        else:
            if self.error("Identificador da funcao esperado.", currentNext= ["LEFT_PARENTHESIS", "SEMICOLON_SYMB"], productionNext = thisRulesNextSymbol) == False:
                return
        
        self.prod_Procedure_Parameters()
        
        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("; esperado.", currentNext= ["VAR_SYMB", "BEGIN_SYMB"], productionNext = thisRulesNextSymbol) == False:
                return

        #self.prod_Procedure_Body()
    
    def prod_Variables(self, tokenNextSymbols, originNextSymbols)-> bool:
        tokenNextSymbols.append("COMMA_SYMB")
        while True:
            if not self.verifyNecessaryToken("IDENTIFIER", "Identificador da variável esperado.", tokenNextSymbols, originNextSymbols):
                return False


            if self.isCurrentToken("COMMA_SYMB"):
                self.loadNextSymbol()
            else:
                break
        return True

    def prod_Procedure_Parameters(self):
        ruleNext = "SEMICOLON_SYMB"
        if not self.verifyPossibleToken("LEFT_PARENTHESIS", "'(' esperado.", "IDENTIFIER", ruleNext):
            return
        
        #Parameters list
        while True:
            if not self.prod_Variables(["SEMICOLON_SYMB"], ruleNext):
                return
            
            if not self.verifyNecessaryToken("COLON_SYMB", "':' esperado.", "TYPE_SYMB", ruleNext):
                return
            
            if not self.verifyNecessaryToken("TYPE_SYMB", "Tipo esperado.", ["RIGHT_PARENTHESIS","SEMICOLON_SYMB"], ruleNext):
                return
            
            if self.isCurrentToken("SEMICOLON_SYMB"):
                self.loadNextSymbol()
            else:
                break
        
        if not self.verifyNecessaryToken("RIGHT_PARENTHESIS", "')' esperado.", ruleNext, ruleNext):        
            return