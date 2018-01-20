# coding: utf-8
from __future__ import print_function
from textblob import TextBlob
from collections import defaultdict
import codecs


def read_data(file_path):
    return codecs.open(file_path, encoding='utf-8').read()


# Get average word length
def average_word_length(text):
    words = TextBlob(text).words
    return sum([len(w) for w in words])/len(words)


def get_ch_windows(text, window_length):
    """
    Return a list of sets, representing a sliding window over the text
    TODO the list should have, alongside its set, the position in the text where
    it starts
    :param text:
    :param window_length:
    :return:
    """
    # for n-grams of win length, we want a count of how many of each of them appear
    chars = [ch for ch in text]
    clusters = []

    # TODO use this to calculate frequency. sets are unhashable :(
    counts = defaultdict(int)

    # Textual processing
    for i in range(0, len(chars) - window_length):
        cluster = set(chars[i:i + window_length])
        clusters.append(cluster)

    return clusters


def avg_len(s1, s2):
    """
    Average length of 2 sets
    :param s1:
    :param s2:
    :return:
    """
    return len(s1) + len(s2) / 2


def percentage_similar(set1, set2):
    """
    Similarity of elements in tuples, regardless of order
    :param tup1:
    :param tup2:
    :return:
    """
    similarity = float(len(set1 & set2)) / float(avg_len(set1, set2))
    return similarity


def compare_blocks_similarity(block1, block2):
    score = 0
    # This looks suspiciously O(n squared), maybe revisit?
    for set1 in block1:
        for set2 in block2:
                score += percentage_similar(set1, set2)

    # normalise
    return float(score) / float(len(block1) + len(block2))


def get_candidate_topic_divisions(ch_windows):

    # clusters has len of 5522, grouping into 100s gives us 50 dividing places
    blocks_len = 100
    sample_score = compare_blocks_similarity(ch_windows[:1 * blocks_len], ch_windows[1 * blocks_len: 2 * blocks_len])
    print(sample_score)


def main():
    text = read_data('./data/Remarks_at_opening_of_the_Centre_for_Humanitarian_Data-Antonio_Guterres.txt')
    window_length = average_word_length(text) + 2
    ch_windows = get_ch_windows(text, window_length)
    candidate_topic_divisions = get_candidate_topic_divisions(ch_windows)


if __name__ == "__main__":
    main()
