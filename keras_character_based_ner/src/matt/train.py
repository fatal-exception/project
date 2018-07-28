from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.dataset import CharBasedNERDataset
from keras_character_based_ner.src.model import CharacterBasedLSTMModel


def toy_dataset_fit():
    config = Config()
    dataset = CharBasedNERDataset()
    model = CharacterBasedLSTMModel(config, dataset)

    model.fit()
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
