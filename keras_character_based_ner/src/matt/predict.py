from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.matt.persist import LoadedToyModel, LoadedMiniModel
from keras_character_based_ner.src.dataset import CharBasedNERDataset


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

    return lm.predict_long_str(file_contents)


def model_toy_predict_str(string: str):
    """
    Take saved toy Keras model, load it and use it to predict the named entities in a file of text.
    The file can be any text - it doesn't need to be a debate file.
    :param string: The string to predict NEs for
    :return:
    """

    config = Config()
    dataset = CharBasedNERDataset()
    lm = LoadedToyModel(config=config, dataset=dataset)

    return lm.predict_long_str(string)


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

    return lm.predict_long_str(file_contents)
