from keras.models import load_model, Sequential  # type: ignore
import numpy as np  # type: ignore
from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from typing import Callable, Dict
from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet


def model_predict_file(model_path, file_path: str):
    """
    Take a saved Keras model, load it and use it to predict the named entities in a file of text.
    The file can be any text - it doesn't need to be a debate file.
    :param model_path: Path to a Keras h5 model saved with model.save()
    :param file_path: path to a text file to predict
    :return:
    """
    custom_objects: Dict[str, Callable] = {
        'non_null_label_accuracy': CharacterBasedLSTMModel.non_null_label_accuracy
    }
    model: Sequential = load_model(model_path, custom_objects=custom_objects)

    with open(file_path) as f:
        file_contents = f.read()

    # Reworked from model.py and dataset.py. If time, this repetition should be refactored.
    alph: CharBasedNERAlphabet = unpickle_large_file("keras_character_based_ner/src/alphabet.p")
    x = np.zeros(len(file_contents))
    for c, char in enumerate(file_contents):
        x[c] = alph.get_char_index(char)

    x = x.reshape((-1, len(file_contents)))

    predicted_classes = model.predict(x, batch_size=1)

    chars = [[alph.num_to_char[i] for i in row] for row in x]

    def y_to_labels(y):
        new_y = []
        for row in y:
            new_y.append([np.argmax(one_hot_labels) for one_hot_labels in row])
        return new_y

    labels = y_to_labels(predicted_classes)

    return list(zip(chars[0], labels[0]))
