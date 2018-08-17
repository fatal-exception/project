from flask import Flask
from hansard_gathering import filesystem

app = Flask(__name__)


@app.route('/')
def get_dates_list():
    dates = filesystem.get_dates_list()
    return ",".join(dates)


@app.route('/<date>/')
def get_hansards_by_date(date):
    pass


@app.route('/<date>/<debate_id>')
def get_hansards_by_debate_id(date, debate_id):
    pass


def main():
    app.run(load_dotenv=False, debug=True, port=5000)
