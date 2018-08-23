from typing import List, Tuple


def format_prediction_string(prediction: List[Tuple[str]]) -> str:
    """
    Take a prediction string returned by the Keras model.
    Make it nice to print in HTML, so it clearly indicates different NE types to a user.
    :param prediction: a list of tuples of strings which are characters of the text, zipped up with
    their NE prediction, e.g. [('A', 'LOC')], or '0' for the null label
    :return: a nicely formatted NE type for user to use. V1: ++ for loc, ** for org, __ for person
    """
    label_start_chars = {
        "0": "",
        "LOC": "<loc>",
        "ORG": "<org>",
        "PER": "<per>",
    }

    label_end_chars = {
        "0": "",
        "LOC": "</loc>",
        "ORG": "</org>",
        "PER": "</per>",
    }

    result: List[str] = []
    previous_label_state: str = "0"
    for char, label in prediction:
        # label-start
        if previous_label_state == "0" and label != "0":
            result.append(label_start_chars[label])
            result.append(char)
        # label-end
        elif previous_label_state != "0" and label == "0":
            result.append(label_end_chars[previous_label_state])
            result.append(char)
        # label-continue
        elif label == previous_label_state:
            result.append(char)
        else:
            raise RuntimeError("Unexpected state")

        previous_label_state = label

    return "".join(result)

