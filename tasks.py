from __future__ import print_function
from hansard_gathering import driver
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
def hansard_download_all(ctx):
    ctx.run("cd hansard_gathering && python hansard_download.py")

@task
def enable_venv(ctx):
    ctx.run("source ./venv/bin/activate && pip install -r requirements.txt")

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
