from nltk.tokenize import TreebankWordTokenizer

with open("ne_data_gathering/processed_ne_data/people/ALL.txt") as f:
    ALL_PEOPLE = f.read()
with open("ne_data_gathering/processed_ne_data/places/ALL.txt") as f:
    ALL_PLACES = f.read()
with open("ne_data_gathering/processed_ne_data/companies/ALL.txt") as f:
    ALL_COMPANIES = f.read()

t = TreebankWordTokenizer()


def interpolate_one(file_path):
    with open(file_path) as f:
        text = f.read()

    for span_start, span_end in t.span_tokenize(text):
        span_length = span_end - span_start
        if text[span_start:span_end] in ALL_PEOPLE:
            text[span_start:span_end] = 'P' * span_length
        elif text[span_start:span_end] in ALL_PLACES:
            text[span_start:span_end] = 'L' * span_length
        elif text[span_start:span_end] in ALL_COMPANIES:
            text[span_start:span_end] = 'O' * span_length

    with open(interpolated_file_path) as f:
        f.write(text)
