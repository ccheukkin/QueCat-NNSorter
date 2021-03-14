def validateText(json):  # json:dict -> str|None
    text = json.get("text")

    if type(text) != str:
        return f'The value for "text" must be of type string. However, {text} is received instead.'

    if not text:
        return f'The value for "text" must not be an empty string. However, {text} is received instead.'

    return None


def validateCategories(json, database):  # json:dict, database: Database -> str|None
    categories = json.get("categories")

    if type(categories) != list:
        return f'The value for "categories" must be an array. However, {categories} is received instead.'

    allCat = list(map(lambda x: x.id, database.categoryGetAll()))
    for i in categories:
        if not (database.toCategoryId(i) in allCat):
            return f'The category {i} does not exist'

    return None


def validateRecord(json, database):  # json: dict, database: Database -> str|None
    textCheck = validateText(json)
    if textCheck == None:
        return validateCategories(json, database)
    else:
        return textCheck


def validateRecords(json, database):  # req: [dict], database: Database -> str|None
    records = json.get("records")

    if type(records) != list:
        return f'The value for "records" must be an array. However, {records} is received instead.'

    for j in records:
        v = validateRecord(j, database)
        if v != None:
            return v

    return None


def validateRecordIds(json, database):   # json: dict, database: Database -> str|None
    ids = json.get("ids")

    if type(ids) != list:
        return f'The value for "ids" must be an array. However, {ids} is received instead.'

    for i in ids:
        if type(i) != int:
            return f'The value for elements in the "ids" array must be of type int. However, {i} is received instead.'

    idsExist = list(map(lambda x: x.id, database.recordGetAll()))
    for id in ids:
        if not (id in idsExist):
            return f"The record with an id of {id} does not exist"

    return None