from hansard_gathering.chunk import chunk_hansard_debate_file_nltk
from hansard_gathering.chunk import nltk_get_tokenizer
import os

tokenizer = nltk_get_tokenizer()


def get_contents(fake_path: str) -> str:
    with open(fake_path, "r") as f:
        contents = f.read()

    return contents


def test_chunk_hansard_debate_file_nltk(fs):
    fake_path = "/a/b/longfile.txt"
    fake_spans_path = "/a/b/longfile-spans.txt"
    contents = "There once was a happy dog. He grew to an old age. The end."
    fs.create_file(fake_path, contents=contents)
    chunk_hansard_debate_file_nltk(fake_path, tokenizer)

    expected_spans = "(0,27)\n" +\
                     "(28,50)\n" +\
                     "(51,59)"

    assert get_contents(fake_spans_path) == expected_spans

    os.unlink(fake_path)

    contents2 = "My friend the hon. Gentleman will surely agree. This must end now."
    fs.create_file(fake_path, contents=contents2)
    chunk_hansard_debate_file_nltk(fake_path, tokenizer)

    expected_spans2 = "(0,47)\n" +\
                      "(48,66)"

    assert get_contents(fake_spans_path) == expected_spans2
