from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from typing import Dict

# Examples in this file taken from
# Deep Learning with Python
# by François Chollet
# Published by Manning Publications, 2017
# Chapter 6 'Deep learning for text and sequences'


def graph_model_history(filepath, dest_file_name):
    """
    Open a pickled `history` object created by a train (fit() invocation),
    and graph out the non-null-label accuracy, categorical accuracy, and loss
    on both training and validation datasets.
    :param filepath: path to the pickled history file.
    :param dest_file_name: a destination file name for the files. This name will
    be used 3 times, with words added to indicate which metric is shown in its graph.
    e.g. 'toy-model'
    :return:
    """
    import matplotlib  # type: ignore
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt # type: ignore
    history_dict = unpickle_large_file(filepath)

    cat_acc = history_dict['categorical_accuracy']
    non_null_label_acc = history_dict['non_null_label_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    val_cat_acc = history_dict['val_categorical_accuracy']
    val_non_null_label_acc = history_dict['val_non_null_label_accuracy']

    epochs = range(1, len(cat_acc) + 1)

    plt.figure(1)

    plt.plot(epochs, cat_acc, 'bo', label='Training acc')
    plt.plot(epochs, val_cat_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.savefig('keras_character_based_ner/graphs/{}-acc.png'.format(dest_file_name))

    plt.figure(2)

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.savefig('keras_character_based_ner/graphs/{}-loss.png'.format(dest_file_name))

    plt.figure(3)

    plt.plot(epochs, non_null_label_acc, 'bo', label='Non null label accuracy')
    plt.plot(epochs, val_non_null_label_acc, 'b', label='Validation Non null label accuracy')
    plt.title('Training and validation non null label accuracy')
    plt.legend()

    plt.savefig('keras_character_based_ner/graphs/{}-non-null-label-acc.png'.format(dest_file_name))
