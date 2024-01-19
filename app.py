from flask import Flask, render_template, request, redirect, session
import pandas as pd
import json
import random

app = Flask(__name__)
app.secret_key = "2144146"

article = pd.read_csv('data/wiki.csv')
with open('data/td.json', 'r') as file:
    td = json.load(file)

# uncomment the below code only if running for the first time
human_eval = []
human_eval = [[] for _ in range(3000)]
with open('data/human_eval.json', "w") as outfile:
    json.dump(human_eval, outfile, indent=2)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/eval')
def eval():
    idx = random.randint(0, 2999)
    session['idx'] = idx
    text = article.text[idx]
    topics = list(td[idx].keys())
    values = list(td[idx].values())
    return render_template('eval.html', article_text=text, topics_list=topics, chart_data=values)


@app.route('/submit', methods=['POST'])
def submit():
    idx = session.get('idx')
    with open('data/human_eval.json', "r") as file:
        human_eval = json.load(file)
    if request.method == 'POST':
        human_eval[idx].append(int(request.form['rating']))
        with open('data/human_eval.json', "w") as outfile:
            json.dump(human_eval, outfile, indent=1)
            print(f"Successfully wrote at {idx}")
        return redirect('/')
    else:
        return "failure"


if __name__ == '__main__':
    app.run(debug=True)
