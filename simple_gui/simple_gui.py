from typing import List, Tuple
from flask import Flask, render_template
from hansard_gathering import filesystem

app = Flask(__name__)


@app.route('/')
def get_dates_list():
    dates = filesystem.get_dates_list()
    return render_template('index.html', dates=dates)


@app.route('/<date>/')
def get_hansards_by_date(date):
    debates: List[Tuple[int, str]] = list(filesystem.get_debates_by_date(date))
    return render_template('date.html', date=date, debates=debates)


@app.route('/<date>/<debate_title>')
def view_hansard(date, debate_title):
    pass
    debate = filesystem.view_hansard(date, debate_title)
    return render_template('debate.html', date=date, debate_title=debate_title, debate=debate)


def main():
    app.run(load_dotenv=False, debug=True, port=5000)
