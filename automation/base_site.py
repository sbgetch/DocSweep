from abc import ABC, abstractmethod

class BaseSite(ABC):

    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def wait_until_ready(self):
        pass

    @abstractmethod
    def search(self, control_number):
        pass