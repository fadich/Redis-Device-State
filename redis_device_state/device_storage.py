__all__ = [
    "DeviceStorage",
]

import logging
import threading
import time

from typing import (
    Callable,
    Iterable,
    Optional,
)

from redis import Redis

from redis_device_state import pubsub
from redis_device_state.device import Device
from redis_device_state.models import Message


logger = logging.getLogger()


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

    def remove_device(self, device: Device):
        message = Message(
            device_id=device.id,
            event=pubsub.DELETED,
            state=device.get_state().dump(),
        )
        topic = pubsub.format_topic(
            device_id=message.device_id,
            event=message.event,
        )

        self._redis.delete(device.id)

        self._redis.publish(topic, message.dump())

    def subscribe(
        self,
        callback: Callable,
        device_id: str = pubsub.ALL,
        event: str = pubsub.ALL,
    ):
        with self._redis.pubsub() as p:
            topic = pubsub.format_topic(device_id, event)
            p.psubscribe(topic)

            for msg in p.listen():
                if isinstance(msg, dict) and "message" in msg.get("type"):
                    try:
                        message = Message.load(msg.get("data"))

                        callback(message)

                    except Exception as e:
                        logger.error(e, exc_info=e)

                time.sleep(0.001)

    def subscribe_async(
        self,
        callback: Callable,
        device_id: str = pubsub.ALL,
        event: str = pubsub.ALL,
    ):
        thread = threading.Thread(
            target=self.subscribe,
            kwargs={
                "callback": callback,
                "device_id": device_id,
                "event": event,
            },
            daemon=True,
        )
        thread.start()

    def _register_device(self, device: Device):
        device.get_state()
