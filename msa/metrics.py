from datetime import datetime
import requests
import re


class MSAMetrics:
    def __init__(self, url: str, timeout: int = 30) -> None:
        self.response = requests.get(url, timeout=timeout)
        self.response_date = datetime.utcnow()

    def get_status_code(self) -> int:
        return self.response.status_code

    def get_response_time(self) -> float:
        # NOTE: This is the time until we get the return header.
        # This is not the time which would include download of
        # the response content
        return self.response.elapsed.total_seconds()

    def get_response_date(self) -> str:
        return self.response_date.strftime(
            '%Y-%m-%dT%H:%M:%S+00:00'
        )

    def get_flag_status(self, expression: str) -> str:
        content_matches = bool(
            re.match(f'{expression}', format(self.response.content))
        )
        return f'{expression!r} : {content_matches}'
