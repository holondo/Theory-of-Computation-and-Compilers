from flask import Flask, request, render_template,jsonify
from transition_table import TransitionTable

app = Flask(__name__)

def do_something(text1,text2):
   combine = text1 + text2
   symbols_table = TransitionTable('symbols.csv')

   match = symbols_table.transition(int(text1),text2)

   return match

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text1 = request.form['text1']
    word = request.args.get('text1')
    text2 = request.form['text2']
    combine = do_something(text1,text2)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
