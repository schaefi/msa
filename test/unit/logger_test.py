from mock import (
    Mock, patch, call
)
import logging
from msa.logger import MSALogger


class TestMSALogger:
    @patch('msa.logger.logging')
    def test_get_logger(self, mock_logging):
        log = Mock()
        log.hasHandlers.return_value = False
        mock_logging.getLogger.return_value = log
        MSALogger.get_logger()
        log.setLevel.assert_called_once_with(logging.INFO)

    @patch('msa.logger.logging')
    def test_set_logfile(self, mock_logging):
        log = Mock()
        log.hasHandlers.return_value = False
        mock_logging.getLogger.return_value = log
        MSALogger.set_logfile('logfile')
        log.addHandler.call_args_list == [
            call(mock_logging.StreamHandler.return_value),
            call(mock_logging.FileHandler.return_value)
        ]
        mock_logging.FileHandler.assert_called_once_with(
            filename='logfile', encoding='utf-8'
        )

    @patch('msa.logger.logging')
    def test_activate_global_info_logging(self, mock_logging):
        MSALogger.activate_global_info_logging()
        mock_logging.basicConfig.assert_called_once_with(
            level=mock_logging.INFO
        )
