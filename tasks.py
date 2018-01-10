from __future__ import print_function
from invoke import task
from invoke import call

from driver import driver


@task
def get_hansard_debate_list(ctx, datestring):
    driver.get_hansard_debate_list(datestring)


@task
def print_hansard_titles(ctx, datestring):
    get_hansard_debate_list(ctx, datestring)
    [print(title) for title in driver.get_hansard_titles()]


@task
def enable_venv(ctx):
    ctx.run("source ./venv/bin/activate && pip install -r requirements.txt")


@task
def test(ctx):
    ctx.run("pytest test/test.py")


