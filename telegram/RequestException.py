class RequestException(Exception):
    def __init__(self, message):
        if message == "Invalid token.":
            message = "Invalid device token. Please set it again using /setAuthToken"

        super().__init__(message)
        self.message = message
