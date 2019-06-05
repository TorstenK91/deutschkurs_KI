

def parse_decision_rule(pdecision_rule):
    """

    :param ptext:
    :param pdecision_rule:
    :return:
    """

    rules = split_by(pdecision_rule)

    and_rules = []

    for rule in rules:
        strs, occurencies, greater_than_list = get_variables_from_statement(rule)

        and_rules += [(strs, occurencies, greater_than_list)]

    return and_rules


def classify(texts, string_rules):
    """

    :param texts:
    :param rules:
    :return:
    """
    rules = parse_decision_rule(string_rules)

    n_texts = len(texts)
    decisions = [None]*n_texts

    for i in range(n_texts):
        decisions[i] = classify_single(texts[i], rules)

    return decisions

def classify_single(text, rules):

    decision = False
    for rule in rules:
        decision_single_rule = True
        for (str, occ, greater_than) in zip(*rule):
            if not decide_single(text, str, occ, greater_than):
                decision_single_rule = False
                break

        if decision_single_rule: ## one of the subrules ( e.g. 'atom1 or atom2 or atom3') is false, hence decision is false
                                     ## since they are divided by 'and'
            decision = True
            break

    return decision




def decide_single(text, str, occ, greater_than):

    n_occ_text = text.upper().count(str.upper())
    decision = False

    if greater_than and n_occ_text > occ:
        decision = True
    elif not greater_than and n_occ_text < occ:
        decision = True

    return decision



def split_by(bool_string, str_chars= "oder", sanitize=True):
    """

    :param bool_string:
    :return:
    """
    statements = bool_string.split(str_chars)

    return statements

def sanitize_string(string):
    """

    :param string:
    :return:
    """
    string = string.strip()  # remove whitespaces at beginning and end

    return string


def get_variables_from_statement(decision_rule_string, str_split = "und"):
    """

    :param bool_string:
    :return:
    """

    atoms = decision_rule_string.split(str_split)

    strs = []
    vals = []
    greater_than_list = []

    for atom in atoms:
        atom = sanitize_string(atom)

        if ">" in atom:
            str_val = atom.split(">")
            operator = ">"
            great_than = True
        elif "<" in atom:
            str_val = atom.split("<")
            operator = "<"
            great_than = False
        else:
            raise ValueError(f"Die Regel '{atom}' muss entweder ein '<' oder ein '>' enthalten.")

        if len(str_val) > 2:
            raise ValueError(f"Zuviele '{operator}' in der Regel '{atom}'. Der Operator {operator} muss genau einmal vorkommen (z.B. Ball > 0) " )

        word = sanitize_string(str_val[0])

        try:
            num = int(sanitize_string(str_val[1]))
        except:
            raise ValueError(f"Die Regel '{atom}' muss rechts eine Zahl haben ( z.B. Ball > 0)")

        strs += [word]
        vals += [num]
        greater_than_list += [great_than]

    return strs, vals, greater_than_list