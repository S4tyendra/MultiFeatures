

class BaseError(Exception):
    message = "An error occurred"

    def __init__(self, error=None):
        self.success = False
        self.error_message = error or self.message

    def __str__(self):
        return self.message
class NotAValidTrainNumber(BaseError):
    message = "Not a valid train number"