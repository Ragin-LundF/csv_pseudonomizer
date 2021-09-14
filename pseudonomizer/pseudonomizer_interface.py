from faker import Faker


class PseudonomizerInterface:
    """
    Interface for pseudonomizer.
    Each implementation of a new pseudonomizer should use this interface to be
    callable from the row_processor.
    """
    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        pass
