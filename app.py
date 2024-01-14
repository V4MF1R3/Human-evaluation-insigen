from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
article = pd.read_csv('data/wiki.csv')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
