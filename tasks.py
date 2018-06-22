from __future__ import print_function
from hansard_preprocessing import driver
from invoke import task

@task
def print_debate_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "Debates")]

@task
def print_wms_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "WMS")]

@task
def print_wrans_titles(ctx, datestring):
    [print(title) for title in driver.get_hansard_titles(datestring, "Wrans")]

@task
def enable_venv(ctx):
    ctx.run("source ./venv/bin/activate && pip install -r requirements.txt")

@task
def test(ctx):
    ctx.run("pytest test")

@task
def compile(ctx):
    ctx.run("find . -name '*.py' | grep -v masters_venv | xargs python -m py_compile")
