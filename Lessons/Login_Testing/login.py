def login_check(username, password):
    if username == 'admin' and password == 'secret':
        return True
    return False