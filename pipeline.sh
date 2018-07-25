#!/usr/bin/env bash
# Pipeline:
# ne_data_companies ne_data_people ne_data_places
# hansard_download_all
# hansard_process_all
# char-ner-pickle-some-alphabet
# hansard_chunk_all
# hansard-interpolate-all --> gives y
# hansard-numerify-all --> gives x


# Due to chunking exploding-space problem, propose new ordering:
# ne_data_companies ne_data_people ne_data_places
# hansard_download_all
# hansard_process_all
# char-ner-pickle-some-alphabet
# Chunk by adding sentence-span files to processing directory
# Split into datasets - charn-ner-rehash-dataset
# hansard-interpolate-all --> gives y
# hansard-numerify-all --> gives x
