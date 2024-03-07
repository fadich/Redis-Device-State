__all__ = [
    "State",
]

import dataclasses
import json
import time

from typing import (
    Any,
    Dict,
    Optional,
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


@dataclasses.dataclass
class Meta(Model):
    updated_at: float


@dataclasses.dataclass
class PreviousState(Model):
    meta: Meta
    data: Dict[Any, Any]


@dataclasses.dataclass
class State(Model):
    meta: Meta
    data: Dict[Any, Any]
    previous_state: Optional[PreviousState] = None

    @classmethod
    def create(
        cls,
        **kwargs,
    ):
        return cls(
            meta=cls._create_meta(),
            data=kwargs,
        )

    def update(self, **kwargs):
        self.previous_state = PreviousState(
            meta=self.meta,
            data=self.data,
        )
        self.meta = self._create_meta()
        self.data = kwargs

        return self

    @classmethod
    def _create_meta(cls):
        return Meta(
            updated_at=time.time(),
        )
