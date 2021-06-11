from flask import Flask, render_template, request, redirect
from sample.lexer import Lexer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        show = []
        strProgram = request.form["txtProgram"]
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

        return render_template("home2.html", boolResult=True, strProgram=show)
    else:
        return render_template("home2.html", boolResult=False, strProgram=[])

if (__name__ == "__main__"):
    app.run()
