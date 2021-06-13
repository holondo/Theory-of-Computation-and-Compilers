from .lexer import Lexer

def sourceToLexer(strProgram):
    show = []
    lex = Lexer()

    strProgram = strProgram.split()

    for section in strProgram:
        section += ' ' #end symbol

        while section != "":
            strToken = lex.lexicalAnalyzer(section)
            section = section[len(strToken[0]):]#slicing the already processed part of string
            if strToken[1] == 'BLANK_SPACE': continue
            show.append(strToken)
    return show