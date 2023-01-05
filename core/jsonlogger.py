import logging
import json_log_formatter
import django


class CeleryLogger(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra['message'] = message

        # Include builtins
        extra['level'] = record.levelname
        extra['name'] = record.name

        if 'time' not in extra:
            extra['time'] = django.utils.timezone.now()

        return extra
