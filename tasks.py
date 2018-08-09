from __future__ import print_function
from hansard_gathering import driver
from hansard_gathering import preprocessing
from hansard_gathering import chunk
from hansard_gathering import interpolate
from hansard_gathering import numerify
from ne_data_gathering import places
from ne_data_gathering import people
from ne_data_gathering import companies
from ne_data_gathering import util
from invoke import task, call
from keras_character_based_ner.src.matt import alphabet_management, file_management, model_integration, dataset_hashing, train, minify_dataset, history, predict
from keras_character_based_ner.src.config import Config
import pickle


@task
def print_debate_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "Debates", "commons")]
    [print(title) for title in driver.get_hansard_titles(datestring, "Debates", "lords")]


@task
def hansard_download_all(ctx, year=1919, month=1, day=1):
    driver.get_all_hansards(year, month, day)


@task
def hansard_process_one(ctx, filepath):
    preprocessing.process_hansard_file(filepath)


@task
def hansard_process_all(ctx):
    preprocessing.process_all_hansard_files()


@task
def hansard_chunk_one(ctx, filepath):
    tokenizer = chunk.nltk_get_tokenizer()
    chunk.chunk_hansard_debate_file_nltk(filepath, tokenizer)


@task
def hansard_chunk_all(ctx, starting_date):
    # e.g. --starting-date 1919-01-01
    chunk.chunk_all_hansard_files(starting_date)


@task
def hansard_display_chunked(ctx, filepath):

    chunk.display_chunked_hansard(filepath)


@task
def hansard_display_interpolated_file(ctx, filepath):
    interpolate.display_one_file_with_interpolations(filepath)


@task
def hansard_interpolate_one(ctx, filepath):
    ne = interpolate.NamedEntityData()
    interpolate.interpolate_one_wrapper(filepath, ne, "processed")


@task
def hansard_interpolate_all(ctx, starting_date):
    interpolate.interpolate_all_hansard_files(starting_date)


@task
def hansard_fix_uninterpolated(ctx, starting_date):
    interpolate.fix_uninterpolated_hansards(starting_date)


@task
def hansard_numerify_one_to_file(cdx, filepath):
    with open("keras_character_based_ner/src/alphabet.p", "rb") as f:
        alph = pickle.load(f)
    numerify.numerify_one_to_file(filepath, alph, maxlen=Config.sentence_max_length)


@task
def enable_venv(ctx):
    ctx.run("echo enabling venv...")
    ctx.run("source ./masters_venv/bin/activate && pip install -r requirements.txt >/dev/null")


@task
def hansard_write_total_number_of_sentences_to_file(ctx, dataset_name):
    file_management.write_total_number_of_hansard_sentences_to_file(dataset_name)


@task
def compile(ctx):
    ctx.run("find . -name '*.py' | grep -v masters_venv | xargs python -m py_compile")


@task
def ne_data_companies_download_process(ctx):
    companies.download_and_process("raw_ne_data", "/companies/dbpedia.txt")
    ctx.run("cd ne_data_gathering/processed_ne_data/companies && cat * | sort > ALL.txt")


@task
def ne_data_companies_process(ctx):
    util.dbpedia_post_processing(
        "{}{}".format("raw_ne_data", "/companies/dbpedia.txt"), "processed_ne_data{}".format(
            "/companies/dbpedia.txt"))
    ctx.run("cd ne_data_gathering/processed_ne_data/companies && cat * | sort > ALL.txt")


@task
def ne_data_people_download_process(ctx):
    people.download_and_process("raw_ne_data", "/people/dbpedia.txt")
    ctx.run("cd ne_data_gathering/processed_ne_data/people && cat * | sort > ALL.txt")


@task
def ne_data_people_process(ctx):
    util.dbpedia_post_processing(
        "{}{}".format("raw_ne_data", "/people/dbpedia.txt"), "processed_ne_data{}".format(
            "/people/dbpedia.txt"))
    ctx.run("cd ne_data_gathering/processed_ne_data/people && cat * | sort > ALL.txt")


@task
def ne_data_places_download_process(ctx):
    places.download_and_process("raw_ne_data", "/places/dbpedia.txt")
    ctx.run("cd ne_data_gathering/processed_ne_data/places && cat * | sort > ALL.txt")


@task
def ne_data_places_process(ctx):
    util.dbpedia_post_processing(
        "{}{}".format("raw_ne_data", "/places/dbpedia.txt"), "processed_ne_data{}".format(
            "/places/dbpedia.txt"))
    ctx.run("cd ne_data_gathering/processed_ne_data/places && cat * | sort > ALL.txt")


@task
def char_ner_pickle_alphabet(ctx):
    alphabet_management.pickle_alphabet()


@task
def char_ner_display_pickled_alphabet(ctx):
    alphabet_management.display_pickled_alphabet()


@task(post=[call(hansard_write_total_number_of_sentences_to_file, "train"),
            call(hansard_write_total_number_of_sentences_to_file, "dev"),
            call(hansard_write_total_number_of_sentences_to_file, "test"),
            call(hansard_write_total_number_of_sentences_to_file, "alphabet-sample"),
            call(hansard_write_total_number_of_sentences_to_file, "ALL"),
            ])
def char_ner_rehash_datasets(ctx):
    dataset_hashing.rehash_datasets()


@task
def char_ner_create_x_toy(ctx, dataset_name):
    model_integration.create_x_toy(Config.sentence_max_length, dataset_name)


@task
def char_ner_create_y_toy(ctx, dataset_name):
    model_integration.create_y_toy(Config.sentence_max_length, dataset_name)


@task
def char_ner_display_median_sentence_length(ctx, dataset_name):
    print(model_integration.get_median_sentence_length(dataset_name))


@task(enable_venv)
def python_type_check(ctx):
    ctx.run("echo mypy: checking Python static types...")
    ctx.run("mypy hansard_gathering")
    ctx.run("mypy ne_data_gathering")
    ctx.run("mypy keras_character_based_ner/src/matt")
    ctx.run("mypy test")


@task(python_type_check)
def test(ctx):
    ctx.run("echo pytest: running tests...")
    ctx.run("pytest test")


@task
def model_minify_toy(ctx):
    minify_dataset.minify_all()


@task
def model_train_toy(ctx, regenerate_tensors=False):
    if regenerate_tensors:
        call(char_ner_create_x_toy, "train")
        call(char_ner_create_x_toy, "test")
        call(char_ner_create_x_toy, "dev")
        call(char_ner_create_y_toy, "train")
        call(char_ner_create_y_toy, "test")
        call(char_ner_create_y_toy, "dev")
    train.toy_dataset_fit()


@task
def model_train_mini(ctx):
    train.mini_dataset_fit()


@task
def model_history_mini(ctx):
    history.graph_model_history("keras_character_based_ner/src/mini_dataset.history.p", "mini")


@task
def model_history_toy(ctx):
    history.graph_model_history("keras_character_based_ner/src/toy_dataset.history.p", "toy")


@task
def model_predict_file(ctx, model, file):
    print(predict.model_predict_file(model, file))
