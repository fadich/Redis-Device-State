__all__ = [
    "RedisDeviceStateError",
    "StateNotFoundError",
    "StateExistsError",
]


class RedisDeviceStateError(Exception):
    pass


class StateNotFoundError(RedisDeviceStateError):
    pass


class StateExistsError(RedisDeviceStateError):
    pass
