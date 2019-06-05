import numpy as np

TESTSETPASSWORD = "KI2019Erdbeere"

def get_texts_by_category(texts, categories, choose_category):
    """

    :param texts:
    :param category:
    :return:
    """
    text_chosen = []
    for i in range(len(texts)):
        if categories[i] == choose_category:
            text_chosen += [texts[i]]

    return text_chosen


def get_boolean_array_from_categories(categories, choose_category):
    """

    :param categories:
    :param choose_category:
    :return:
    """

    n_cat = len(categories)
    bool_cat = np.zeros((n_cat, ), dtype=np.bool_)

    for i in range(n_cat):
        bool_cat[i] = True if categories[i] == choose_category else False

    return bool_cat


def check_password(password):
    """

    :param password:
    :return:
    """

    if password == TESTSETPASSWORD:
        return "test"
    else:
        raise ValueError("Das Passwort ist leider falsch!")