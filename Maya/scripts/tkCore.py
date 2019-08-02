def getFromDefaults(inDict, inKey, inLastDefault, *args):
    """
    Get a value from the first dictionary actually implementing the given key 

    :param inDict: The first dictionary to look into
    :type inDict: dict
    :param inKey: The key to look for
    :type inKey: object
    :param inLastDefault: The default value if key can't be found anywhere
    :type inLastDefault: object
    :param *args: a list of dictionaries to look for the key, in order
    :type *args: list(dict)
    :return: The value
    :rtype: object
    """

    if inKey in inDict:
        return inDict[inKey]

    for defaultDict in args:
        if inKey in defaultDict:
            return defaultDict[inKey]

    return inLastDefault