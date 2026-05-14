from login_buggy import login_check
def test_valid_credentials():
    assert login_check('admin', 'secret') == True


def test_wrong_password():
    assert login_check('admin', 'wrongpass') == False


def test_empty_password():
    assert login_check('admin', '') == False


def test_wrong_username():
    assert login_check('user', 'secret') == False


def test_wrong_username_and_password():
    assert login_check('user', 'wrong') == False


def test_empty_username():
    assert login_check('', 'secret') == False


def test_empty_username_and_password():
    assert login_check('', '') == False


def test_case_sensitive_username():
    assert login_check('Admin', 'secret') == False


def test_case_sensitive_password():
    assert login_check('admin', 'Secret') == False