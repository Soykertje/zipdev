"""Base class for services."""


class BaseService:
    def execute(self, *args, **kwargs):
        """
        This method should be overridden in each service class to execute the desired logic.
        """
        raise NotImplementedError("Subclasses must implement the `execute` method.")
