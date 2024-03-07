__all__ = [
    "Device",
]

from typing import Optional

from redis import Redis

from redis_device_state import pubsub
from redis_device_state.exceptions import (
    StateExistsError,
    StateNotFoundError,
)
from redis_device_state.models import (
    Message,
    State,
)


class Device:

    def __init__(
        self,
        id: str,
        redis: Redis,
    ):
        self._id = id
        self._redis = redis

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return f"<{self.__class__.__name__} #{self.id}>"

    def register(self):
        if self._has_state():
            raise StateExistsError("Device already exists")

        state = State.create()
        self._set_state(state)
        self._publish(
            event=pubsub.CREATED,
            state=state,
        )

        return state

    def get_state(self) -> State:
        self._check_state()
        state = self._fetch_state()

        state = State.load(state)

        return state

    def set_state(self, **kwargs):
        state = self.get_state()
        state = state.update(**kwargs)

        self._set_state(state)
        self._publish(
            event=pubsub.UPDATED,
            state=state,
        )

        return state

    def delete(self):
        state = self.get_state()

        self._publish(
            event=pubsub.DELETED,
            state=state,
        )
        self._delete_state()

        return state

    def _has_state(self) -> State:
        return self._fetch_state() is not None

    def _check_state(self):
        if not self._has_state():
            raise StateNotFoundError("Device does not exist")

    def _fetch_state(self) -> Optional[bytes]:
        return self._redis.get(self.id)

    def _set_state(self, state: State):
        self._redis.set(self.id, state.dump())

    def _delete_state(self):
        self._redis.delete(self.id)

    def _publish(
        self,
        event: str,
        state: State,
    ):
        message = Message(
            device_id=self.id,
            event=event,
            state=state,
        )
        topic = pubsub.format_topic(
            device_id=message.device_id,
            event=message.event,
        )

        self._redis.publish(topic, message.dump())
