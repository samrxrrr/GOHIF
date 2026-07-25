from pydantic import BaseModel
from typing import List


class Workflow(BaseModel):

    name: str

    manifests: List[str]
