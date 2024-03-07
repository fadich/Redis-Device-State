__all__ = [
    "Device",
]

from typing import Optional

from redis import Redis

from redis_device_state import pubsub
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

    def get_state(self) -> State:
        state = self._fetch_state()
        if state is None:
            state = State.create()
            self._save_state(state)
            self._publish(
                event=pubsub.CREATED,
                state=state,
            )

            return state

        state = State.load(state)

        return state

    def set_state(self, **kwargs):
        state = self.get_state()
        state = state.update(**kwargs)

        self._save_state(state)
        self._publish(
            event=pubsub.UPDATED,
            state=state,
        )

        return state

    def __repr__(self):
        return f"<{self.__class__.__name__} #{self.id}>"

    def _save_state(self, state: State):
        self._redis.set(self.id, state.dump())

    def _fetch_state(self) -> Optional[bytes]:
        return self._redis.get(self.id)

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

        print(topic, event)

        self._redis.publish(topic, message.dump())
