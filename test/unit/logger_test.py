from mock import (
    Mock, patch
)
import logging
from msa.logger import MSALogger


class TestMSALogger:
    @patch('msa.logger.logging')
    def test_get_logger(self, mock_logging):
        log = Mock()
        mock_logging.getLogger.return_value = log
        MSALogger.get_logger()
        log.setLevel.assert_called_once_with(logging.INFO)

    @patch('msa.logger.logging')
    def test_activate_global_info_logging(self, mock_logging):
        MSALogger.activate_global_info_logging()
        mock_logging.basicConfig.assert_called_once_with(
            level=mock_logging.INFO
        )
