__all__ = [
    "DeviceStorage",
]

from typing import (
    Iterable,
    Optional,
)

from redis import Redis

from redis_device_state.device import Device


class DeviceStorage:

    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: Optional[str] = None,
        **redis_params,
    ):
        self._redis = Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            **redis_params,
        )

    def init_device(self, id: str):
        device = Device(
            id=id,
            redis=self._redis,
        )
        self._register_device(device)

        return device

    def get_devices(self) -> Iterable[Device]:
        for key in self._redis.keys():
            yield self.init_device(key.decode())

    def remove_device(self, id: str):
        self._redis.delete(id)

    def _register_device(self, device: Device):
        device.get_state()
