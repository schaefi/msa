from msa.metrics import MSAMetrics
from datetime import datetime
from mock import (
    Mock, patch, MagicMock
)

from requests.exceptions import RequestException


class TestMSAMetrics:
    @patch('requests.get')
    @patch('msa.metrics.datetime')
    @patch('msa.metrics.Request')
    @patch('socket.gethostbyname')
    def setup(
        self, mock_gethostbyname, mock_Request, mock_datetime,
        mock_request_get
    ):
        mock_gethostbyname.return_value = '8.8.8.8'
        mock_datetime.utcnow = Mock(
            return_value=datetime.strptime(
                '29/04/21 01:55:19', '%d/%m/%y %H:%M:%S'
            )
        )
        self.response = MagicMock()
        self.response.json = Mock(
            return_value={'geolocation': 'geolocation'}
        )
        self.response.content = 'some artificial content'
        mock_request_get.return_value = self.response
        self.metrics_simple = MSAMetrics(url='https://simple')
        self.metrics_matches = MSAMetrics(
            url='https://smart', matches='.*artificial'
        )
        self.metrics_nomatch = MSAMetrics(
            url='https://smart', matches='XXX'
        )

    @patch('requests.get')
    def test_request_failed(self, mock_request_get):
        mock_request_get.side_effect = RequestException
        metrics = MSAMetrics(url='bogus')
        assert metrics.get_status_code() == -1

    def test_get_geolocation(self):
        assert self.metrics_simple.get_geolocation() == \
            "{'geolocation': 'geolocation'}"

    def test_get_status_code(self):
        assert self.metrics_simple.get_status_code() == \
            self.metrics_simple.response_status_code

    def test_get_response_time(self):
        assert self.metrics_simple.get_response_time() == \
            self.metrics_simple.response_elapsed_total_seconds

    def test_get_response_date(self):
        assert self.metrics_simple.get_response_date() == \
            '2021-04-29T01:55:19+00:00'

    def test_get_page(self):
        assert self.metrics_simple.get_page() == 'https://simple'

    def test_get_flag_status(self):
        assert self.metrics_simple.get_tag() is None
        assert self.metrics_matches.get_tag() == \
            "'.*artificial' : True"
        assert self.metrics_nomatch.get_tag() == \
            "'XXX' : False"
