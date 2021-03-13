import mysql.connector

def validateRecord(request):  # request:dict -> str|None
    text = request["text"]
    if type(text) != str:
        return 'The value for "text" must be of type string'
    if not text:
        return 'The value for "text" must not be an empty string'
    
    categories = request["categories"]
    if type(categories) != list:
        return 'The value for "categories" must be an array'
    for i in categories:
        if not _categoryExist(i):
            return i + 'is invalid as a value for the "categories" array'

    return None

def _categoryExist(category):   # category:int|str -> bool
    if type(category) == str:

def saveRecord(request):

def idCheck(id):

def deleteRecord(id):