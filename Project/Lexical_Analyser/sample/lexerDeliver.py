from .lexer import Lexer

def sourceToLexer(strProgram):
    show = []
    lex = Lexer()
    strProgram += " " #final character
    while strProgram != "":
        strToken = lex.lexicalAnalyzer(strProgram)
        strProgram = strProgram[len(strToken[0]):]#slicing the already processed part of string
        if strToken[1] == 'BLANK_SPACE': continue
        show.append(strToken)
    return show