from flask import Flask, render_template, request
from sample.lexerDeliver import sourceToLexer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        show = sourceToLexer(request.form["txtProgram"])
        return render_template("home2.html", boolResult=True, strProgram=show)

    else:
        return render_template("home2.html", boolResult=False, strProgram=[])

if (__name__ == "__main__"):
    app.run()
