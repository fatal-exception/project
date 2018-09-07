from typing import List, Tuple
from flask import Flask, render_template, request
from hansard_gathering import filesystem
from keras_character_based_ner.src.matt.persist import LoadedToyModel
from keras_character_based_ner.src.matt.eval import init_config_dataset
from simple_gui.util import format_prediction_string
import tensorflow as tf

app = Flask(__name__)

cache = {}

# Tensorflow default graph has to be captured to avoid a TF threading bug
# when running with Flask:
# https://github.com/keras-team/keras/issues/2397
graph = None


def initialize_keras_model():
    global graph
    cache["model"] = LoadedToyModel(*init_config_dataset())
    # Set Tensorflow graph as soon as model is set
    graph = tf.get_default_graph()


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
    global graph
    with graph.as_default():
        model = cache['model']
        data: str = request.get_data().decode(encoding='UTF-8')
        prediction: List[Tuple[str]] = model.predict_long_str(data)
        gui_prediction: str = format_prediction_string(prediction)
        return gui_prediction


def main():
    initialize_keras_model()
    app.run(host='0.0.0.0', load_dotenv=False, debug=True, port=5000, threaded=True)
