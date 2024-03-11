__all__ = [
    "Message",
    "State",
]

import dataclasses
import time

from typing import (
    Any,
    Dict,
    Optional,
)

from redis_device_state.base import Model


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
        ts = time.time()

        return Meta(
            updated_at=ts,
        )


@dataclasses.dataclass
class Message(Model):
    device_id: str
    event: str
    state: State
