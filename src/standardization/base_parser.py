"""
GOHIF Phase 3
Base Parser Interface
"""

from abc import ABC, abstractmethod
from pathlib import Path
import hashlib


class BaseParser(ABC):

    def sha256(self, path: Path):
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)

        return h.hexdigest()


    @abstractmethod
    def detect(self, path):
        pass


    @abstractmethod
    def extract_metadata(self, path):
        pass


    @abstractmethod
    def validate(self, path):
        pass


    @abstractmethod
    def standardize(self, path, output_dir):
        pass


    @abstractmethod
    def summarize(self, path):
        pass
