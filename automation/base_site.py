from abc import ABC, abstractmethod


class BaseSite(ABC):

    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def attach(self):
        """Attach to an already-open browser tab."""
        pass

    @abstractmethod
    def search(self, control_number):
        pass
