# Redis Device State

```python

from redis_device_state import DeviceStateManager

manager = DeviceStateManager(
    redis_host="0.0.0.0",
    redis_password="my-password",
)

# Get or create a device
test_device = manager.get_or_create_device("test")
test_device.set_state(
    Hello="World!",
)
test_device.set_state(
    Hello="World!",
    And="Something else...",
)

# Get the device from list
some_device = list(manager.list_devices())[0]
print(some_device.id)
print(some_device.get_state())
```
