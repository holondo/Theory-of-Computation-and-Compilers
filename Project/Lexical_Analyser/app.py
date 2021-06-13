from flask import Flask, render_template, request
from sample.lexerDeliver import sourceToLexer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    #In the homepage, if the button send a POST method
    if(request.method == "POST"):
        show = sourceToLexer(request.form["txtProgram"]) #Sends txtProgram's content to the "Parser" who returns Lexer's work 
        return render_template("home2.html", boolResult=True, strProgram=show)

    #If the app receives a GET method
    else:
        return render_template("home2.html", boolResult=False, strProgram=[])

if (__name__ == "__main__"):
    app.run()
