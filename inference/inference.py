def validate(req):
    text = req["text"]
    if type(text) != str:
        return 'The value for "text" must be of type string'
    if not text:
        return 'The value for "text" must not be an empty string'

    return None