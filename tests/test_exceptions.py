from pybuzzsprout.exceptions import BuzzsproutError, AuthError, NotFoundError, APIError


def test_buzzsprout_error_is_base():
    err = BuzzsproutError("something broke")
    assert str(err) == "something broke"
    assert isinstance(err, Exception)


def test_auth_error_inherits():
    err = AuthError("no key")
    assert isinstance(err, BuzzsproutError)


def test_not_found_error_inherits():
    err = NotFoundError("404")
    assert isinstance(err, BuzzsproutError)


def test_api_error_has_status_and_body():
    err = APIError(status_code=500, body="internal server error")
    assert isinstance(err, BuzzsproutError)
    assert err.status_code == 500
    assert err.body == "internal server error"
    assert "500" in str(err)
