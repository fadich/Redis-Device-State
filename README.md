# Redis Device Storage

```python

from redis_device_state import DeviceStorage


storage = DeviceStorage(
    redis_host="0.0.0.0",
    redis_password="my-password",
)

# Get or create a device
test_device = storage.init_device("test")
test_device.set_state(
    Hello="World!",
)
test_device.set_state(
    Hello="World!", 
    And="Something else...",
)

# Get the device from list
the_test_device = list(storage.get_devices())[0]
print(the_test_device.id)
print(the_test_device.get_state())
```
