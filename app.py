from flask import Flask, render_template, request, redirect, session
import pandas as pd
import json
import random
import gspread

app = Flask(__name__)
app.secret_key = '2144146'


# importing data
article = pd.read_csv('data/wiki.csv')
with open('data/td.json', 'r') as file:
    td = json.load(file)

# uncomment the below code only if running for the first time, this will create json file with empty lists
# human_eval = []
# human_eval = [[] for _ in range(3000)]
# with open('data/human_eval.json', "w") as outfile:
#     json.dump(human_eval, outfile, indent=2)


# Get the google sheet
# update the path of the credential file
Sheet_credential = gspread.service_account("creds.json")
spreadsheet = Sheet_credential.open_by_key(
    '1BXBPs8NoKxl5UVBM3aUSdxjqV8PkAmRw2IloTduhmRc')
worksheet = spreadsheet.get_worksheet(0)
rated_data = worksheet.get_all_values()
rated_data = [val[1] for val in rated_data]


# Home Page


@app.route('/')
def home():
    return render_template('index.html')

# Created to avoid randomly generating the already rated articles


def generate_idx():
    all_idxs = range(0, 2999)
    remaining_idx = list(set(all_idxs) - set(rated_data))

    return random.choice(remaining_idx)

# evaluation page


@app.route('/eval')
def eval():
    idx = generate_idx()
    session['idx'] = idx            # to pass idx to submit function below
    text = article.text[idx]
    topics = list(td[idx].keys())
    values = list(td[idx].values())
    return render_template('eval.html', article_text=text, topics_list=topics, chart_data=values)


# handle things after submit btn is pressed
@app.route('/submit', methods=['POST'])
def submit():
    idx = session.get('idx')
    '''
    #Commented the use of JSON file - Aaryan
    with open('data/human_eval.json', "r") as file:
        human_eval = json.load(file)'''
    if request.method == 'POST':
        # request.form['rating'] is the input value from user, range [1-5]
        # human_eval[idx].append(int(request.form['rating'])) Commented - Aaryan
        # with open('data/human_eval.json', "w") as outfile: Commented - Aaryan
        worksheet.append_row([request.form['rating'], idx])
        rated_data.append(idx)
        # json.dump(human_eval, outfile, indent=1) Commented - Aaryan
        return redirect('/')
    else:
        return "failure"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
