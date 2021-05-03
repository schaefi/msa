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
import socket
from urllib.request import Request
from datetime import datetime
from typing import Optional
from msa.logger import MSALogger
import requests
import re


class MSAMetrics:
    """
    Implements reading of request metrics
    """
    def __init__(
        self, url: str, matches: str = '', timeout: int = 30
    ) -> None:
        """
        Create new instance of MSAMetrics

        At creation time the request is issued and all data collected

        :param str url: URL
        :param str matches: regexp to match against request content
        :param int timeout: request timeout in seconds
        """
        log = MSALogger.get_logger()
        self.url = url
        self.expression = matches
        self.response_date = datetime.utcnow()
        self.response_status_code = -1
        self.response_elapsed_total_seconds = -1.0
        self.content_matches_expression = False
        self.geolocation = {}
        try:
            response = requests.get(url, timeout=timeout)
            self.response_status_code = response.status_code
            self.response_elapsed_total_seconds = \
                response.elapsed.total_seconds()
            if self.expression:
                self.content_matches_expression = bool(
                    re.match(f'{self.expression}', format(response.content))
                )
            source_ip = socket.gethostbyname(Request(url).host)
            self.geolocation = requests.get(
                f'https://geolocation-db.com/json/{source_ip}&position=true'
            ).json()
        except requests.exceptions.RequestException as issue:
            log.error(f'Request failed with: {issue!r}')

    def get_geolocation(self) -> str:
        """
        Return request geolocation details

        :return: The geolocation dictionary as provided by geolocation-db.com

        :rtype: Dict
        """
        return f'{self.geolocation}'

    def get_page(self) -> str:
        """
        Return request url

        :return: The url param from the constructor

        :rtype: str
        """
        return self.url

    def get_status_code(self) -> int:
        """
        Return request status code

        On a failed request -1 is returned

        :return: status code

        :rtype: int
        """
        return self.response_status_code

    def get_response_time(self) -> float:
        """
        Return request response time in seconds

        This is the time until we get the return header.
        This is not the time which would include download of
        the response content

        On a failed request -1.0 is returned

        :return: Number of seconds

        :rtype: float
        """
        return self.response_elapsed_total_seconds

    def get_response_date(self) -> str:
        """
        Return date of request in the format %Y-%m-%dT%H:%M:%S+00:00

        :return: Date string

        :rtype: str
        """
        return self.response_date.strftime(
            '%Y-%m-%dT%H:%M:%S+00:00'
        )

    def get_tag(self) -> Optional[str]:
        """
        Return tag string depending on the regular expression
        provided in the constructor. The tag consists out of
        the expression and the bool value if it matches the
        request content or not

        :return: A tag string or None

        :rtype: str | None
        """
        if self.expression:
            return f'{self.expression!r} : {self.content_matches_expression}'
        return None
