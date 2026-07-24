from __future__ import annotations

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


def retry_policy():

    return retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=30,
        ),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
