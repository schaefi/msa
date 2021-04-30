# Copyright (c) 2021 Marcus Schäfer.  All rights reserved.
#
# This file is part of MSA.
#
# MSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MSA.  If not, see <http://www.gnu.org/licenses/>
#
from datetime import datetime
from typing import Optional
from msa.logger import MSALogger
import requests
import re


class MSAMetrics:
    def __init__(
        self, url: str, matches: str = '', timeout: int = 30
    ) -> None:
        log = MSALogger.get_logger()
        self.url = url
        self.expression = matches
        self.response_date = datetime.utcnow()
        self.response_content = b''
        self.response_status_code = -1
        self.response_elapsed_total_seconds = -1.0
        try:
            response = requests.get(url, timeout=timeout)
            self.response_status_code = response.status_code
            self.response_elapsed_total_seconds = \
                response.elapsed.total_seconds()
            self.response_content = response.content
        except requests.exceptions.RequestException as issue:
            log.error(f'Request failed with: {issue!r}')

        if self.expression and self.response_content:
            self.content_matches_expression = bool(
                re.match(f'{self.expression}', format(self.response_content))
            )

    def get_page(self) -> str:
        return self.url

    def get_status_code(self) -> int:
        return self.response_status_code

    def get_response_time(self) -> float:
        # NOTE: This is the time until we get the return header.
        # This is not the time which would include download of
        # the response content
        return self.response_elapsed_total_seconds

    def get_response_date(self) -> str:
        return self.response_date.strftime(
            '%Y-%m-%dT%H:%M:%S+00:00'
        )

    def get_tag(self) -> Optional[str]:
        if self.expression:
            return f'{self.expression!r} : {self.content_matches_expression}'
        return None
