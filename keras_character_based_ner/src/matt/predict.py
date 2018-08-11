from keras.models import load_model, Sequential  # type: ignore
import numpy as np  # type: ignore
from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from typing import Callable, Dict
from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet


class LoadedModel:
    """
    A CharacterBasedLSTMModel keras model loaded in off disk
    """
    def __init__(self, model_path):
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': CharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)
        self.alph: CharBasedNERAlphabet = unpickle_large_file("keras_character_based_ner/src/alphabet.p")

    @staticmethod
    def y_to_labels(y):
        new_y = []
        for row in y:
            new_y.append([np.argmax(one_hot_labels) for one_hot_labels in row])
        return new_y

    def predict_str(self, string_data):
        # Reworked from model.py and dataset.py. If time, this repetition should be refactored.
        x = np.zeros(len(string_data))
        for c, char in enumerate(string_data):
            x[c] = self.alph.get_char_index(char)
        x = x.reshape((-1, len(string_data)))

        predicted_classes = self.model.predict(x, batch_size=1)

        chars = [[self.alph.num_to_char[i] for i in row] for row in x]
        labels = self.y_to_labels(predicted_classes)
        return list(zip(chars[0], labels[0]))


def model_predict_file(model_path, file_path: str):
    """
    Take a saved Keras model, load it and use it to predict the named entities in a file of text.
    The file can be any text - it doesn't need to be a debate file.
    :param model_path: Path to a Keras h5 model saved with model.save()
    :param file_path: path to a text file to predict
    :return:
    """

    with open(file_path) as f:
        file_contents = f.read()

    lm = LoadedModel(model_path)

    return lm.predict_str(file_contents)
