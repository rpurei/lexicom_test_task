class UserNotFound(Exception):
    """Raised when User not found"""
    pass


class PhoneFormatWrong(Exception):
    """Raised when phone number contains wrong characters"""
    pass


class UserExists(Exception):
    """Raised when User exists while trying to add new one"""
    pass
