def seperate_col_val(list):
    cols = []
    vals = []
    for i in range(len(list)):
        list[i] = list[i].split(':', 1)

    for i in range(len(list)):
        vals.append(list[i][1])
        cols.append(list[i][0])

    return cols, vals

def create_dictionaries(cols, vals):
    dictionary = dict.fromkeys(cols[:])
    for i in range(len(cols)):
        dictionary[cols[i]] = vals[i]

    return dictionary

def data_dict(list):
    cols, vals = seperate_col_val(list)
    dictionary = create_dictionaries(cols, vals)
    return dictionary, cols

