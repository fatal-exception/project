from keras.models import load_model, Sequential  # type: ignore
from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from typing import Callable, Dict
from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.dataset import CharBasedNERDataset


class LoadedToyModel(CharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Toy dataset")
        model_path = "keras_character_based_ner/src/toy_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': CharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)


class LoadedMiniModel(CharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Mini dataset")
        model_path = "keras_character_based_ner/src/mini_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': CharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)


def model_toy_predict_file(file_path: str):
    """
    Take saved toy Keras model, load it and use it to predict the named entities in a file of text.
    The file can be any text - it doesn't need to be a debate file.
    :param file_path: path to a text file to predict
    :return:
    """

    with open(file_path) as f:
        file_contents = f.read()

    config = Config()
    dataset = CharBasedNERDataset()
    lm = LoadedToyModel(config=config, dataset=dataset)

    return lm.predict_str(file_contents)


def model_mini_predict_file(file_path: str):
    """
    Take saved mini Keras model, load it and use it to predict the named entities in a file of text.
    The file can be any text - it doesn't need to be a debate file.
    :param file_path: path to a text file to predict
    :return:
    """

    with open(file_path) as f:
        file_contents = f.read()

    config = Config()
    dataset = CharBasedNERDataset()
    lm = LoadedMiniModel(config=config, dataset=dataset)

    return lm.predict_str(file_contents)
