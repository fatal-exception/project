import csv

from util import capitalise_text, write_to_data_file


def main():
    nyc_baby_names = process_kaggle_nyc_baby_names()
    write_to_data_file(nyc_baby_names, "people", "nyc_baby_names.txt")


def process_kaggle_nyc_baby_names():
    with open('Most_Most_Popular_Baby_Names_by_Sex_and_Mother_s_Ethnic_Group__New_York_City.csv') as f:
        data = f.readlines()
        for row in csv.reader(data):
            yield capitalise_text(row[3])

