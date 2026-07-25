from __future__ import annotations

import hashlib
from pathlib import Path


class ChecksumValidator:

    def sha256(
        self,
        filename: Path,
    ):

        h = hashlib.sha256()

        with open(filename,"rb") as f:

            while True:

                block = f.read(1024*1024)

                if not block:
                    break

                h.update(block)

        return h.hexdigest()

    def validate(
        self,
        filename: Path,
        expected: str,
    ):

        if expected is None:
            return True

        return self.sha256(filename) == expected
