import json
from pydantic import BaseModel

class CustomBaseModel(BaseModel):
    @classmethod
    def get_json_schema(cls) -> str:
        return json.dumps(cls.model_json_schema())["properties"]