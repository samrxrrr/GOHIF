from abc import ABC, abstractmethod

class MetadataExtractor(ABC):

    @abstractmethod
    def supports(self, path):
        pass

    @abstractmethod
    def extract(self, path):
        pass
