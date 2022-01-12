def generate_activation_code():
    import datetime
    result = str(datetime.datetime.now().time()) + str(datetime.datetime.now().timestamp())
    result = result.replace(':', '')
    return result
