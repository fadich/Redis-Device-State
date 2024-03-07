__all__ = [
    "Model",
]

import dataclasses
import json
from typing import (
    Any,
    Dict,
    Union,
)


class Model:

    def to_dict(self):
        dct = {}
        for field in self.__annotations__.keys():
            value = getattr(self, field)
            if isinstance(value, Model):
                dct[field] = value.to_dict()
            else:
                dct[field] = value

        return dct

    def dump(self):
        return json.dumps(self.to_dict())

    @classmethod
    def load(cls, data: Union[str, bytes]):
        dct = json.loads(data)

        return cls.load_dict(dct)

    @classmethod
    def load_dict(cls, data: Dict[str, Any]):
        dct = {}
        for field, type_ in cls.__annotations__.items():
            value = data[field]
            if dataclasses.is_dataclass(type_):
                dct[field] = type_.load_dict(value)
            else:
                dct[field] = value

        return cls(**dct)

    def __str__(self):
        return self.dump()
