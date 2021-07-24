import os
from flask import Flask, render_template, request, redirect
from sample.lexerDeliver import sourceToLexer
from sample.SyntacticAnalyser import SyntacticAnalyser

UPLOAD_FOLDER = "./uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    #In the homepage, if the button send a POST method
    if(request.method == "POST"):
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filePath)        
        file = open(filePath, 'r')
        strProgram = file.read()
        # show = sourceToLexer(strProgram) #Sends txtProgram's content to the "Parser" who returns Lexer's work
        analyser = SyntacticAnalyser()
        show = analyser.analyse(strProgram)

        return render_template("home.html", boolResult=True, strProgram=strProgram.split('\n'), messages= show)

    #If the app receives a GET method
    else:
        return render_template("home.html", boolResult=False, strProgram=[])

if (__name__ == "__main__"):
    app.run()
