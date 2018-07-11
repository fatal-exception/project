from __future__ import print_function
from hansard_gathering import driver
from hansard_gathering import preprocessing
from hansard_gathering import chunk
from invoke import task

@task
def print_debate_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "Debates", "commons")]
    [print(title) for title in driver.get_hansard_titles(datestring, "Debates", "lords")]

@task
# Written Ministerial Statements
def print_wms_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "WMS")]

@task
# Written Answers
def print_wrans_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "Wrans")]

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
    chunk.chunk_hansard_debate_file_textblob(filepath)

@task
def enable_venv(ctx):
    ctx.run("source ./masters_venv/bin/activate && pip install -r requirements.txt")

@task(pre=[enable_venv])
def hansard_max_sentence_length(ctx):
    ctx.run("python keras_character_based_ner/src/matt.py max-sentence-length")

@task
def test(ctx):
    ctx.run("pytest test")

@task
def compile(ctx):
    ctx.run("find . -name '*.py' | grep -v masters_venv | xargs python -m py_compile")

@task
def ne_data_companies(ctx):
    ctx.run("cd ne_data_gathering && python companies.py")

@task
def ne_data_people(ctx):
    ctx.run("cd ne_data_gathering && python people.py")

@task
def ne_data_places(ctx):
    ctx.run("cd ne_data_gathering && python places.py")

@task
def char_ner_get_alphabet(ctx):
    ctx.run("python keras_character_based_ner/src/matt.py get-alphabet")
