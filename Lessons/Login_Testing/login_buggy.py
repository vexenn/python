def login_check(username, password):
    # BUG: ignores password!
    if username == 'admin':
        return True
    return False