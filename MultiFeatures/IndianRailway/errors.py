class BaseError(Exception):
    message = "An error occurred"

    def __init__(self, error=None):
        self.success = False
        self.error_message = error or self.message

    def __str__(self):
        return self.error_message


class NotAValidTrainNumber(BaseError):
    message = "Not a valid train number"


class NotAValidStationCode(BaseError):
    message = "Not a valid Station Code"


class InternetUnreachable(BaseError):
    message = "Cannot connect to the internet"


class HTTPErr(BaseError):
    message = "Response status code is not 200"

    def __init__(self, status_code=None, error=None):
        self.success = False
        self.status_code = status_code
        self.error_message = error
