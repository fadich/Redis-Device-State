TOPIC_NAME = "devices"

ALL = "*"
CREATED = "$created"
UPDATED = "$updated"
DELETED = "$deleted"


def format_topic(device_id: str, event: str):
    return f"{TOPIC_NAME}/{device_id}/{event}"
