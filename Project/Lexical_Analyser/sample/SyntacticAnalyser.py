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
        if len(self.strProgram) <= 1: 
            return True
        return False

    def getCurrentToken(self) -> str:
        return self.symb[1]
    
    def getCurrentSymbol(self) -> str:
        return self.symb[0]
    
    ### Returns: true, if 
    def isCurrentToken(self, expectedToken) -> bool:
        return (self.getCurrentToken() in expectedToken)

    def loadNextSymbol(self):
        if not self.programIsProcessed():
            self.symb = self.lexer.lexicalAnalyzer(self.strProgram)# = (symbol,token)
            self.strProgram = self.strProgram[len(self.symb[0]):]#slicing the already processed part of string

            if self.getCurrentToken() == 'BLANK_SPACE':
                if '\n' in self.symb[0]:
                    self.currentLine += 1
                self.loadNextSymbol()

            if self.isCurrentToken("COMMENT_LINE"):
                self.loadNextSymbol()

            if self.isCurrentToken("UNCLOSED_COMMENT"):
                self.errors.append(f"Erro léxico na linha {self.currentLine}: {self.symb}.")    
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

        while (not self.programIsProcessed()) and self.getCurrentToken() not in productionNext:
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
    
    def prod_Body(self):

        #-----DECLARATIONS
        while True:
            self.prod_dc_c()
            while self.isCurrentToken("CONST_SYMB"):
                self.prod_dc_c()
                
            self.prod_dc_v()
            while self.isCurrentToken("VAR_SYMB"):
                self.prod_dc_v()

            self.prod_dc_p()
            while self.isCurrentToken("PROCEDURE_SYMB"):
                self.prod_dc_p()

            if self.getCurrentToken() not in ["CONST_SYMB","VAR_SYMB","PROCEDURE_SYMB"]:
                break
            #-----DECLARATIONS END

        if self.isCurrentToken("BEGIN_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("begin esperado.", currentNext= ["WRITE_SYMB", "WHILE_SYMB", "IF_SYMB", "IDENTIFIER", "BEGIN","END_SYMB"], productionNext= "DOT_SYMB") == False:
                return

        self.prod_Commands()

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
        productionNext = ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]
        if self.isCurrentToken("VAR_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("var esperado.", currentNext= "IDENTIFIER", productionNext= productionNext) == False:
                self.errors.pop()
                return

        #<variaveis>
        if not self.prod_Variables(["COLON_SYMB"]+productionNext):
            return
            
        if self.isCurrentToken("COLON_SYMB"):
            self.loadNextSymbol()
        else:
            if not self.error("Dois pontos esperado.", currentNext= "TYPE_SYMB", productionNext= productionNext):
                return
        
        if self.isCurrentToken("TYPE_SYMB"):
            self.loadNextSymbol()
        else:
            if not self.error("Tipo esperado.", currentNext= "SEMICOLON_SYMB", productionNext= productionNext):
                return
        
        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if not self.error("; esperado.", currentNext= productionNext, productionNext= productionNext):
                return

    def prod_dc_p(self):
        thisRulesNextSymbol  = ["CONST_SYMB","VAR_SYMB", "PROCEDURE_SYMB", "BEGIN_SYMB"]
        if self.isCurrentToken("PROCEDURE_SYMB"):
            self.loadNextSymbol()
        else:
            if not self.error("procedure esperado.", currentNext= "IDENTIFIER", productionNext = thisRulesNextSymbol):
                self.errors.pop()
                return

        if self.isCurrentToken("IDENTIFIER"):
                self.loadNextSymbol()
        else:
            if not self.error("Identificador da funcao esperado.", currentNext= ["LEFT_PARENTHESIS", "SEMICOLON_SYMB"], productionNext = thisRulesNextSymbol):
                return
        
        self.prod_Procedure_Parameters()

        if self.isCurrentToken("SEMICOLON_SYMB"):
            self.loadNextSymbol()
        else:
            if not self.error("; esperado.", currentNext= ["VAR_SYMB", "BEGIN_SYMB"], productionNext = thisRulesNextSymbol):
                return

        #self.prod_Procedure_Body()
    
    def prod_Variables(self, originNextSymbols)-> bool:
        tokenNextSymbols = list(originNextSymbols).append("COMMA_SYMB")
        while True:
            if not self.verifyNecessaryToken("IDENTIFIER", "Identificador da variável esperado.", tokenNextSymbols, originNextSymbols):
                return False


            if self.isCurrentToken("COMMA_SYMB"):
                self.loadNextSymbol()
            else:
                break
        return True

    def prod_Procedure_Parameters(self):
        ruleNext = ["SEMICOLON_SYMB"]
        if not self.verifyPossibleToken("LEFT_PARENTHESIS", "'(' esperado.", "IDENTIFIER", ruleNext):
            return
        
        #Parameters list
        while True:
            self.prod_Variables(ruleNext + ["COLON_SYMB"])
            
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
    
    def prod_Commands(self):
        ruleNext = ["END_SYMB", "DOT_SYMB"]
        cmdTokens = ["IDENTIFIER", "READ_SYMB", "WRITE_SYMB", "READ_SYMB", "FOR_SYMB", "IF_SYMB", "BEGIN_SYMB"]
        allNexts = ruleNext + cmdTokens + ["SEMICOLON_SYMB"]
        
        while True:
            if self.isCurrentToken(ruleNext):
                return

            self.prod_CMD(allNexts)

            self.verifyNecessaryToken("SEMICOLON_SYMB", "';' esperado.", cmdTokens, cmdTokens + ruleNext)

            if self.getCurrentToken() not in cmdTokens:#mudar o not in p/ todos pq se o comportamento for inesperado, para
                if self.programIsProcessed():
                    return

    def prod_CMD(self, productionNext):

        if self.isCurrentToken("WRITE_SYMB") or self.isCurrentToken("READ_SYMB"):
            self.loadNextSymbol()

            if not self.verifyNecessaryToken("LEFT_PARENTHESIS", "'(' esperado.", "IDENTIFIER", productionNext):
                return
            
            self.prod_Variables2(productionNext + ["RIGHT_PARENTHESIS"])

            if not self.verifyNecessaryToken("RIGHT_PARENTHESIS", "')' esperado.", productionNext, productionNext):
                return
        

        elif self.isCurrentToken("IDENTIFIER"):
            self.loadNextSymbol()

            if self.getCurrentToken() == "ATTR_SYMB":
                self.loadNextSymbol()

                self.prod_Expression(productionNext)
            
            elif self.isCurrentToken("LEFT_PARENTHESIS"):
                self.loadNextSymbol()

                if self.isCurrentToken("IDENTIFIER"):
                    while True:
                        if not self.verifyNecessaryToken("IDENTIFIER", "Parametro esperado.", ["SEMICOLON_SYMB", "RIGHT_PARENTHESIS"], productionNext):
                            return
                        
                        if not self.isCurrentToken("SEMICOLON_SYMB"):
                            break
                        self.loadNextSymbol()

                if not self.verifyNecessaryToken("RIGHT_PARENTHESIS", "')' esperado.", "DO_SYMB", productionNext):
                    return
        
        elif self.isCurrentToken("BEGIN_SYMB"):#begin <comandos> end
            self.prod_Begin(productionNext)

        elif self.isCurrentToken("WHILE_SYMB"):
            self.loadNextSymbol()

            CMDFirst = ["IDENTIFIER", "READ_SYMB", "WRITE_SYMB", "READ_SYMB", "FOR_SYMB", "IF_SYMB", "BEGIN_SYMB"]

            if not self.verifyNecessaryToken("LEFT_PARENTHESIS", "'(' esperado.", ["ADD_SIGN", "SUB_SIGN", "IDENTIFIER","UNSIGNED_INTEGER", "UNSIGNED_FLOAT", "LEFT_PARENTHESIS"], productionNext):
                return
            
            self.prod_Condition(productionNext + ["RIGHT_PARENTHESIS"])

            if not self.verifyNecessaryToken("RIGHT_PARENTHESIS", "')' esperado.", "DO_SYMB", productionNext):
                return

            if not self.verifyNecessaryToken("DO_SYMB", "while necessita do.", CMDFirst, productionNext):
                return
            self.prod_CMD(productionNext)
        
        elif self.isCurrentToken("IF_SYMB"):
            self.loadNextSymbol()

            CMDFirst = ["IDENTIFIER", "READ_SYMB", "WRITE_SYMB", "READ_SYMB", "FOR_SYMB", "IF_SYMB", "BEGIN_SYMB"]

            self.prod_Condition(productionNext + ["THEN_SYMB"])

            if not self.verifyNecessaryToken("THEN_SYMB", "then esperado.", CMDFirst, productionNext):
                return

            self.prod_CMD(productionNext + ["ELSE_SYMB"])
            
            if self.isCurrentToken("ELSE_SYMB"):
                self.prod_CMD()

        elif self.isCurrentToken("FOR_SYMB"):
            ExpressionFirst = ["ADD_SIGN", "SUB_SIGN", "IDENTIFIER","UNSIGNED_INTEGER", "UNSIGNED_FLOAT", "LEFT_PARENTHESIS"]
            CMDFirst = ["IDENTIFIER", "READ_SYMB", "WRITE_SYMB", "READ_SYMB", "FOR_SYMB", "IF_SYMB", "BEGIN_SYMB"]

            self.loadNextSymbol()

            if not self.verifyNecessaryToken("IDENTIFIER", "Iterador esperado.", "ATTR_SYMB", productionNext):
                return

            if not self.verifyNecessaryToken("ATTR_SYMB", "':=' esperado.", ExpressionFirst, productionNext):
                return
            
            self.prod_Expression(productionNext + ["SEMICOLON_SYMB"])

            if not self.verifyNecessaryToken("TO_SYMB", "'to' esperado.", ExpressionFirst, productionNext):
                return
            
            self.prod_Expression(productionNext + ["SEMICOLON_SYMB"])

            if not self.verifyNecessaryToken("DO_SYMB", "'do' esperado.", CMDFirst, productionNext):
                return

            self.prod_CMD(productionNext)
        else:
            self.error("Comando esperado.", productionNext, productionNext+["SEMICOLON_SYMB"])

    def prod_Condition(self, productionNext):
        ExpressionFirst = ["ADD_SIGN", "SUB_SIGN", "IDENTIFIER","UNSIGNED_INTEGER", "UNSIGNED_FLOAT", "LEFT_PARENTHESIS"]
        self.prod_Expression(productionNext + ExpressionFirst)


        if self.getCurrentToken() in ["EQUAL_SIGN", "DIFF_SIGN", "LESS_SIGN", "LESS_EQUAL_SIGN", "GREATER_SIGN", "GREATER_EQUAL_SIGN"]:
            self.loadNextSymbol()
        else:
            if not self.error("Operador relacional esperado.", ExpressionFirst, productionNext):
                return
        
        self.prod_Expression(productionNext)

    def prod_Begin(self, productionNext):
        CMDFirst = ["IDENTIFIER", "READ_SYMB", "WRITE_SYMB", "READ_SYMB", "FOR_SYMB", "IF_SYMB", "BEGIN_SYMB"]

        if self.isCurrentToken("BEGIN_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("begin esperado.", currentNext= CMDFirst + ["END_SYMB"], productionNext= ["DOT_SYMB", "END_SYMB"]) == False:
                return
        
        self.prod_Commands()

        if self.isCurrentToken("END_SYMB"):
            self.loadNextSymbol()
        else:
            if self.error("End; esperado.", currentNext= productionNext, productionNext= productionNext) == False:
                return

    def prod_Expression(self, productionNext):
        if self.getCurrentToken() in ["ADD_SIGN", "SUB_SIGN"]:
            self.loadNextSymbol()
        while True:
            self.prod_Factor(productionNext)

            self.prod_Other_Factors(productionNext)

            if self.getCurrentToken() not in ["ADD_SIGN", "SUB_SIGN"]:
                return

            self.loadNextSymbol()
        

    def prod_Factor(self, productionNext):
        if self.getCurrentToken() in ["IDENTIFIER", "UNSIGNED_INTEGER", "UNSIGNED_FLOAT"]:
            self.loadNextSymbol()

        elif self.isCurrentToken("LEFT_PARENTHESIS"):
            self.loadNextSymbol()

            self.prod_Expression(productionNext)

            if not self.verifyNecessaryToken("RIGHT_PARENTHESIS", "')' esperado.", productionNext, productionNext):
                return           
        
        else:
            self.error("Fator da expressão esperado.", productionNext, productionNext)

    def prod_Other_Factors(self, productionNext):
        if self.getCurrentToken() in ["MULTIPLY_SIGN", "DIVIDE_SIGN"]:#criar divide
            self.loadNextSymbol()
            self.prod_Factor(productionNext)

    def prod_Variables2(self, productionNext):
        while True:

            if self.isCurrentToken("IDENTIFIER"):
                self.loadNextSymbol()
                if self.getCurrentToken() != "COMMA_SYMB":
                    return
            else:
                if not self.error("Variável esperada", "COMMA_SYMB", productionNext):
                    return

            self.loadNextSymbol()

