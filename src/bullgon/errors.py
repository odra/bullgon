"""
A module that contains all error classes/utilities
whithin the project.
"""
class BullgonError(Exception):
    """
    Base error class, any specialized error
    classes should inherit from this one.
    """
    def __init__(self, message: str, code: int = 1) -> None:
        """
        Creates a new BullgonError class to represent an error.

        It requires a error message and an optional error code
        which defaults to 1 if no value is provided.
        """
        super(BullgonError, self).__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        """
        User friendly string representation of an error.
        """
        return f'[{self.code}] {self.message}'
