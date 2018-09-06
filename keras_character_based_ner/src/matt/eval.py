"""
Evaluate the trained Keras model
"""
from sklearn.model_selection import KFold  # type: ignore
from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.matt.persist import AlphabetPreloadedCharBasedNERDataset,\
    LoadedToyModel, SavedCharacterBasedLSTMModel
from typing import List
import numpy as np  # type: ignore


def init_config_dataset():
    """
    Create a vanilla Config and CharBasedNERDataset object, required for constructing a model.
    We don't actually use the dataset at all in evaluation - we just use the model weights.
    :return:
    """
    config = Config()
    dataset = AlphabetPreloadedCharBasedNERDataset()
    return config, dataset


def k_fold_cross_validation():
    """
    Train and validate a new model using k-fold cross validation.
    With thanks to
    https://datascience.stackexchange.com/questions/27212/stratifiedkfold-valueerror-supported-target-types-are-binary-multiclass
    for the guide on implementing k-fold in keras
    :return:
    """
    x = unpickle_large_file("keras_character_based_ner/src/x_np-train-toy.p")
    y = unpickle_large_file("keras_character_based_ner/src/y_np-train-toy.p")
    loss_scores: List = []
    categorical_accuracy_scores: List = []
    non_null_label_accuracy_scores: List = []
    # Use a new CharBasedLSTMModel with saving capabilities, and manual evaluation and fit methods
    kf = KFold(n_splits=10)
    for train, test in kf.split(x):
        model = SavedCharacterBasedLSTMModel(*init_config_dataset())
        model.manual_fit(x_train=x[train], y_train=y[train], batch_size=Config.batch_size,
                         epochs=3)
        loss, categorical_accuracy, non_null_label_accuracy = model.manual_evaluate(
            x_test=x[test], y_test=y[test], batch_size=Config.batch_size)
        loss_scores.append(loss)
        categorical_accuracy_scores.append(categorical_accuracy)
        non_null_label_accuracy_scores.append(non_null_label_accuracy)

        print("loss_scores are: {}, categorical_accuracy_scores are: {}, non_null_label_accuracy scores are:{} "
              .format(loss_scores,
                      categorical_accuracy_scores,
                      non_null_label_accuracy_scores))

    scores_dict = {
        "loss_scores": loss_scores,
        "categorical_accuracy_scores": categorical_accuracy_scores,
        "non_null_label_accuracy": non_null_label_accuracy_scores,
    }

    print(scores_dict)

    for title, scores in scores_dict.items():
        # With thanks to
        # https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/
        print("Mean for {} is {}".format(title, np.mean(scores)))
        print("Standard deviation for {} is {}".format(title, np.std(scores)))


def model_data_validation(dataset_name, dataset_size):
    """
    Validate toy model on a bucket of text it hasn't been trained on (train) or validated on (dev) yet.
    This is because the 'test' dataset used to train the model gave NaN for validation loss.
    :param dataset_name: train, test, dev
    :param dataset_size: toy or mini
    :return:
    """
    x = unpickle_large_file("keras_character_based_ner/src/x_np-{}-{}.p".format(
        dataset_name, dataset_size))
    y = unpickle_large_file("keras_character_based_ner/src/y_np-{}-{}.p".format(
        dataset_name, dataset_size))
    # Load in the pre-trained Toy model off disk
    model = LoadedToyModel(*init_config_dataset())
    metrics = model.manual_evaluate(x, y, Config.batch_size)
    print("On dataset {dataset_size}-{dataset_name}; ".format(
        dataset_size=dataset_size, dataset_name=dataset_name))
    print("loss: {}".format(metrics[0]))
    print("categorical accuracy: {}".format(metrics[1]))
    print("non null label accuracy: {}".format(metrics[2]))
    if len(metrics) > 3:  # If extended metrics have been added...
        print("precision_null: {}".format(metrics[3]))
        print("precision_loc: {}".format(metrics[4]))
        print("precision_org: {}".format(metrics[5]))
        print("precision_per: {}".format(metrics[6]))
        print("recall_null: {}".format(metrics[7]))
        print("recall_loc: {}".format(metrics[8]))
        print("recall_org: {}".format(metrics[9]))
        print("recall_per: {}".format(metrics[10]))
        print("f1_null: {}".format(metrics[11]))
        print("f1_loc: {}".format(metrics[12]))
        print("f1_org: {}".format(metrics[13]))
        print("f1_per: {}".format(metrics[14]))


def calc_eval_baseline(dataset_name, dataset_size, baseline_label=0):
    """
    Calculate a basic evaluation baseline, of assuming all labels are NULL
    :param dataset_name: train, test or dev
    :param dataset_size: toy or mini
    :param baseline_label: the label the baseline should always try to guess
    :return:
    """
    def all_zeros(_char_onehot):
        return all(elem == 0 for elem in _char_onehot)

    def not_null(_char_onehot):
        return _char_onehot[0] == 0 and 1 in _char_onehot[1:]

    def un_one_hot(_char_onehot):
        for pos, val in enumerate(_char_onehot):
            if val == 1:
                return pos

    y = unpickle_large_file("keras_character_based_ner/src/y_np-{}-{}.p".format(
        dataset_name, dataset_size))

    num_of_chars = 0
    num_of_not_nulls = 0
    num_correctly_guessed = 0
    for sample in y:
        for char_onehot in sample:
            if all_zeros(char_onehot):
                pass  # This is padding, ignore
            else:
                num_of_chars += 1
                if not_null(char_onehot):
                    num_of_not_nulls += 1
                if un_one_hot(char_onehot) == baseline_label:
                    num_correctly_guessed += 1

    # The baseline will be wrong for every not-null in the chars
    baseline_inaccuracy = float(num_of_not_nulls) / float(num_of_chars)
    baseline_accuracy = 1 - baseline_inaccuracy
    baseline_guessed_accuracy = float(num_correctly_guessed) / float(num_of_chars)
    print(baseline_accuracy)
    print(baseline_guessed_accuracy)
