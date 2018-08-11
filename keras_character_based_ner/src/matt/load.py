from keras_character_based_ner.src.matt.train import SavedCharacterBasedLSTMModel
from typing import Callable, Dict
from keras.models import load_model, Sequential  # type: ignore


class LoadedToyModel(SavedCharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Toy dataset")
        model_path = "keras_character_based_ner/src/toy_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': SavedCharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)


class LoadedMiniModel(SavedCharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Mini dataset")
        model_path = "keras_character_based_ner/src/mini_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': SavedCharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)

