class InternalException(Exception):
    """
    Class to handle internal exceptions
    """
    def __init__(self, message=None):
        self.message = message


class EmailAlreadySentTo(InternalException):
    def __init__(self, email: str):
        message = f"Email Already Sent To {email}"
        super().__init__(message)


class BilletAlreadyGenerated(InternalException):
    def __init__(self, id: str):
        message = f"Billet already generated ${id}"
        super().__init__(message)


class GovernmentIdIDCannotBeNull(InternalException):
    def __init__(self, gorvementId: str):
        message = f"Billet already generated ${gorvementId}"
        super().__init__(message)
