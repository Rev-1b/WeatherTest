from datetime import datetime

import pytz


def get_current_time(offset_seconds):
    offset_hours = offset_seconds // 3600
    tz = pytz.FixedOffset(offset_hours * 60)
    current_time = datetime.now(tz)
    return current_time.strftime('%H:%M:%S')


def convert_unix_to_local(unix_timestamp, offset_seconds):
    offset_hours = offset_seconds // 3600
    tz = pytz.FixedOffset(offset_hours * 60)

    local_time = datetime.fromtimestamp(unix_timestamp, tz=tz)
    return local_time.strftime('%H:%M:%S')
