from .lexer import Lexer

def sourceToLexer(strProgram):
    show = []
    lex = Lexer()

    strProgram = strProgram.split()

    #(section.append('\0') for section in strProgram)
    
    #while(strProgram != ""):
    for section in strProgram:
        section += ' '

        while section != "":
            strToken = lex.lexicalAnalyzer(section)
            section = section[len(strToken[0]):]#slicing the read part of string
            if strToken[1] == 'BLANK_SPACE': continue
            show.append(strToken)
    return show