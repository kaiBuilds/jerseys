"""Custom exceptions."""


class RegexNotFound(Exception):
    """
    Exception raised when a regular expression is not found.

    Attributes:
        message (str): The error message.
        value (object): The value associated with the error.
    """

    def __init__(self, message, value, *args: object) -> None:
        super().__init__(*args)
        self.message = message
        self.value = value


class ResponseExtractionError(Exception):
    """Custom exception for errors in extracting and validating JSON from GPT response."""

    def __init__(self, message="Error in extracting or validating JSON from response"):
        self.message = message
        super().__init__(self.message)
