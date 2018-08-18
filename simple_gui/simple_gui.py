from typing import List, Tuple
from flask import Flask, render_template, request
from hansard_gathering import filesystem
from keras_character_based_ner.src.matt.persist import LoadedToyModel
from keras_character_based_ner.src.matt.eval import init_config_dataset

app = Flask(__name__)

cache = {}


def initialize_keras_model():
    cache["model"] = LoadedToyModel(*init_config_dataset())


@app.route('/')
def get_dates_list():
    dates = filesystem.get_dates_list()
    return render_template('index.html', dates=dates)


@app.route('/date/<date>/')
def get_hansards_by_date(date):
    debates: List[Tuple[int, str]] = list(filesystem.get_debates_by_date(date))
    return render_template('date.html', date=date, debates=debates)


@app.route('/date/<date>/<debate_title>')
def view_hansard(date, debate_title):
    debate = filesystem.view_hansard(date, debate_title)
    debate_paras = debate.split("\n")
    return render_template('debate.html', date=date, debate_title=debate_title, debate_paras=debate_paras)


# Add a 'predict' route for AJAX posting of content to be predicted
@app.route('/predict/', methods=['POST'])
def predict_text():
    model = cache['model']
    data = str(request.get_data())
    print(data)
    prediction = model.predict_long_str(data)
    return prediction


def main():
    initialize_keras_model()
    app.run(load_dotenv=False, debug=True, port=5000)
