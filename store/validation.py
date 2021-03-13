def validateText(req):  # req:dict -> str|None
    text = req["text"]
    if type(text) != str:
        return 'The value for "text" must be of type string'
    if not text:
        return 'The value for "text" must not be an empty string'
    return None


def validateCategories(req, database):  # req:dict, database: Database -> str|None
    categories = req["categories"]
    if type(categories) != list:
        return 'The value for "categories" must be an array'
    for i in categories:
        if not database.categoryExist(i):
            return i + 'is invalid as a value for the "categories" array'
    return None


def validateRecord(req, database):  # req: dict, database: Database -> str|None
    textCheck = validateText(req)
    if textCheck == None:
        return validateCategories(req, database)
    else:
        return textCheck