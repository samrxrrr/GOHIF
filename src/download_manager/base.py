"""
GOHIF Download Manager
Base downloader interface

Author: GOHIF
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseDownloader(ABC):
    """
    Abstract base class for all GOHIF download backends.
    """

    def __init__(self):
        self.backend_name = self.__class__.__name__

    @abstractmethod
    def download(self, row) -> Dict[str, Any]:
        """
        Download one dataset described by a manifest row.

        Parameters
        ----------
        row : pandas.Series

        Returns
        -------
        dict
            Metadata describing the completed download.
        """
        raise NotImplementedError

    def info(self) -> str:
        return self.backend_name
