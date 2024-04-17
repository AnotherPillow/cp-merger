
def default(obj, key, de):
    if obj and key in obj:
        return obj[key]
    else:
        return de
