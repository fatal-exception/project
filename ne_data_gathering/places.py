#!/usr/bin/env python
import util


def main() -> None:
    def conll2003eng():
        conll_places = util.process_conll_file(util.conll_file, 'LOC')
        util.write_to_data_file(conll_places, "places", "conll_2003.txt")

    conll2003eng()


if __name__ == "__main__":
    main()
