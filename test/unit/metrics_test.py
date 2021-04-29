from msa.metrics import MSAMetrics
from datetime import datetime
from mock import (
    Mock, patch, MagicMock
)


class TestMSAMetrics:
    @patch('requests.get')
    @patch('msa.metrics.datetime')
    def setup(self, mock_datetime, mock_request_get):
        mock_datetime.utcnow = Mock(
            return_value=datetime.strptime(
                '29/04/21 01:55:19', '%d/%m/%y %H:%M:%S'
            )
        )
        self.response = MagicMock()
        self.response.content = 'some artificial content'
        mock_request_get.return_value = self.response
        self.metrics = MSAMetrics(url="some-uri")

    def test_get_status_code(self):
        assert self.metrics.get_status_code() == self.response.status_code

    def test_get_response_time(self):
        assert self.metrics.get_response_time() == \
            self.response.elapsed.total_seconds.return_value

    def test_get_response_date(self):
        assert self.metrics.get_response_date() == '2021-04-29T01:55:19+00:00'

    def test_get_flag_status(self):
        assert self.metrics.get_flag_status('.*artificial') == \
            "'.*artificial' : True"
        assert self.metrics.get_flag_status('XXX') == \
            "'XXX' : False"
