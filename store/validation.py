def validateText(json):  # json:dict -> str|None
    text = json["text"]
    if type(text) != str:
        return f'The value for "text" must be of type string. However, {text} is received instead.'
    if not text:
        return f'The value for "text" must not be an empty string. However, {text} is received instead.'
    return None


def validateCategories(json, database):  # json:dict, database: Database -> str|None
    categories = json["categories"]
    if type(categories) != list:
        return f'The value for "categories" must be an array. However, {categories} is received instead.'
    for i in categories:
        if not database.categoryExist(i):
            return f'{i} is invalid as a value for the "categories" array.'
    return None


def validateRecord(json, database):  # json: dict, database: Database -> str|None
    textCheck = validateText(json)
    if textCheck == None:
        return validateCategories(json, database)
    else:
        return textCheck

def validateRecords(req, database):
    for json in req:
        v = validateRecord(json, database)
        if v != None:
            return v
    return None