"""
Evaluate the trained Keras model
"""
from sklearn.model_selection import StratifiedKFold
from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.dataset import CharBasedNERDataset
from keras_character_based_ner.src.matt.persist import LoadedToyModel


def init_config_dataset():
    """
    Create a vanilla Config and CharBasedNERDataset object, required for constructing a model.
    We don't actually use the dataset at all in evaluation - we just use the model weights.
    :return:
    """
    config = Config()
    dataset = CharBasedNERDataset()
    return config, dataset


def k_fold_cross_validation():
    """
    Train and validate a new model using k-fold cross validation.
    With thanks to https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/
    for the guide on implementing k-fold in keras
    :return:
    """
    seed = 7
    x = unpickle_large_file("keras_character_based_ner/src/x_np-train-toy.p")
    y = unpickle_large_file("keras_character_based_ner/src/y_np-train-toy.p")
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    cross_validation_scores = []
    model = LoadedToyModel(*init_config_dataset())
    for train, test in kfold.split(x, y):
        model.manual_fit(x_train=x[train], y_train=y[train], batch_size=Config.batch_size,
                         epochs=3)
        scores = model.manual_evaluate(x_test=x[test], y_test=y[test], batch_size=Config.batch_size)


def toy_data_validation(dataset_name):
    """
    Validate toy model on a bucket of text it hasn't been trained on or validated on yet -
    the 'eval' dataset.
    This is because the 'test' dataset used to train the model gave NaN for validation loss.
    :param dataset_name: "mini", the mini-test dataset, or "eval" a one-bucket dataset
    that the toy model has not seen before.
    :return:
    """
    x = unpickle_large_file("keras_character_based_ner/src/x_np-{}-mini.p".format(dataset_name))
    y = unpickle_large_file("keras_character_based_ner/src/y_np-{}-mini.p".format(dataset_name))
    model = LoadedToyModel(*init_config_dataset())
    evaluation = model.manual_evaluate(x, y, Config.batch_size)
