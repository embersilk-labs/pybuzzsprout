class BuzzsproutError(Exception):
    pass


class AuthError(BuzzsproutError):
    pass


class NotFoundError(BuzzsproutError):
    pass


class APIError(BuzzsproutError):
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"Buzzsprout API error {status_code}: {body}")
