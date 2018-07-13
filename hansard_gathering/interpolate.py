from nltk.tokenize import TreebankWordTokenizer


def get_all_ne_data():
    with open("ne_data_gathering/processed_ne_data/places/ALL.txt") as f:
        all_places = f.read()
    with open("ne_data_gathering/processed_ne_data/companies/ALL.txt") as f:
        all_companies = f.read()
    with open("ne_data_gathering/processed_ne_data/people/ALL.txt") as f:
        all_people = f.read()

    return all_places, all_companies, all_people


def interpolate_one(file_path, tokenizer, all_places, all_companies, all_people):
    """
    file_path e.g. hansard_gathering/chunked_hansard_data/1943-09-21/Deaths of Members-chunk-1979.txt
    :param file_path: path to file to do interpolation on
    :param tokenizer: an NLTK tokenizer with span_tokenize method
    :param all_*: files with lists of _all_ collected examples of that NE type, \n-separated
    :return:
    """
    with open(file_path) as f:
        text = f.read()
        interpolated_text = "0" * len(text)

    for span_start, span_end in tokenizer.span_tokenize(text):
        span_length = span_end - span_start
        # TODO there is bias here. What if something is multiple NEs?
        if text[span_start:span_end] in all_places:
            interpolated_text[span_start:span_end] = '1' * span_length

        elif text[span_start:span_end] in all_companies:
            interpolated_text[span_start:span_end] = '2' * span_length

        elif text[span_start:span_end] in all_people:
            interpolated_text[span_start:span_end] = '3' * span_length

    interpolated_file_path = file_path.replace("chunked_hansard_data", "interpolated_hansard_data")
    with open(interpolated_file_path) as f:
        f.write(interpolated_text)


def interpolate_one_wrapper(file_path):
    t = TreebankWordTokenizer()
    interpolate_one(file_path, t, *get_all_ne_data())
