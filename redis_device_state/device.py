__all__ = [
    "Device",
]

from typing import Optional

from redis import Redis

from redis_device_state.state import State


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

            return state

        state = State.load(state)

        return state

    def set_state(self, **kwargs):
        state = self.get_state()
        state = state.update(**kwargs)

        self._save_state(state)

        return state

    def _save_state(self, state: State):
        self._redis.set(self.id, state.dump())

    def _fetch_state(self) -> Optional[bytes]:
        return self._redis.get(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} #{self.id}>"
