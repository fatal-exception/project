import numpy as np  # type: ignore
from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet
from keras_character_based_ner.src.matt.file_management import get_texts as matt_get_texts
from keras_character_based_ner.src.matt.model_integration import get_x_y as matt_get_x_y
from keras_character_based_ner.src.matt.model_integration import get_x_y_generator as matt_get_x_y_generator
from keras_character_based_ner.src.matt.model_integration import get_labels as matt_get_labels
from typing import List


class CharBasedNERDataset:
    NULL_LABEL = '0'
    BASE_LABELS = [NULL_LABEL]

    def __init__(self):
        self.texts: List[str] = self.get_texts()
        self.alphabet: CharBasedNERAlphabet = CharBasedNERAlphabet(self.texts)
        self.labels: List[int] = self.BASE_LABELS + self.get_labels()
        self.num_labels: int = len(self.labels)
        self.num_to_label: dict = {}
        self.label_to_num: dict = {}

        self.init_mappings()

    def get_texts(self) -> List[str]:
        """ Implement with own data source. """
        return list(matt_get_texts())

    def get_x_y(self, sentence_maxlen, dataset_name='all'):
        """ Implement with own data source.

        :param sentence_maxlen: maximum number of characters per sample
        :param dataset_name: 'all', 'train', 'dev' or 'test'
        :return: Tuple (x, y)
                x: Array of shape (batch_size, sentence_maxlen).
                Entries in dimension 1 are alphabet indices, index 0 is the padding symbol
                y: Array of shape (batch_size, sentence_maxlen, self.num_labels).
                Entries in dimension 2 are label indices, index 0 is the null label
        """
        # MIR x 1st dimension is for all samples,
        # 2nd dimension is for characters-string in each sample,
        # using ints to lookup the alphabet.
        # MIR y 1st dimension is for all samples,
        # 2nd dimension is for char-strings, 3rd dim is for streams of labels, by int
        return matt_get_x_y(dataset_name)

    def get_x_y_generator(self, sentence_maxlen, dataset_name='all'):
        """ Implement with own data source.

        :return: Generator object that yields tuples (x, y), same as in get_x_y()
        """
        return matt_get_x_y_generator()

    def get_labels(self):
        """ Implement with own data source.

        :return: List of labels (classes) to predict, e.g. 'PER', 'LOC', not including the null label '0'.
        """
        # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
        return matt_get_labels()

    def str_to_x(self, s: str, maxlen: int):
        x: np.ndarray = np.zeros(maxlen)
        c: int
        char: str
        for c, char in enumerate(s[:maxlen]):
            x[c] = self.alphabet.get_char_index(char)
        # -1 means infer the length
        return x.reshape((-1, maxlen))

    def x_to_str(self, x):
        return [[self.alphabet.num_to_char[i] for i in row] for row in x]

    def y_to_labels(self, y):
        Y = []
        for row in y:
            Y.append([self.num_to_label[np.argmax(one_hot_labels)] for one_hot_labels in row])
        return Y

    def init_mappings(self):
        for num, label in enumerate(self.labels):
            self.num_to_label[num] = label
            self.label_to_num[label] = num
