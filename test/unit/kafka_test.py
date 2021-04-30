from mock import (
    Mock, patch
)
from pytest import raises
from collections import namedtuple
from msa.kafka import MSAKafka
from msa.exceptions import MSAConfigFileNotFoundError


class TestMSAKafka:
    def setup(self):
        self.kafka = MSAKafka('../data/kafka.yml')

    def test_config_file_not_found(self):
        with raises(MSAConfigFileNotFoundError):
            MSAKafka('../data/foo')

    @patch('msa.kafka.KafkaProducer')
    def test_send(self, mock_KafkaProducer):
        metrics = Mock()
        message_broker = Mock()
        mock_KafkaProducer.return_value = message_broker
        metrics.get_page.return_value = 'http://example.com'
        metrics.get_response_date.return_value = 'date'
        metrics.get_status_code.return_value = 42
        metrics.get_response_time.return_value = 'time'
        metrics.get_tag.return_value = None
        self.kafka.send(metrics)

        mock_KafkaProducer.assert_called_once_with(
            security_protocol='SSL',
            bootstrap_servers='kafka-example.com:12345',
            ssl_cafile='ca.pem',
            ssl_certfile='service.cert',
            ssl_keyfile='service.key'
        )
        message_broker.send.assert_called_once_with(
            'ms-intro',
            b'date: date\npage: http://example.com\nrtime: '
            b'time\nstatus: 42\ntag: null\n'
        )

    @patch('msa.kafka.KafkaConsumer')
    def test_read(self, mock_KafkaConsumer):
        message_consumer = Mock()
        message_type = namedtuple(
            'message_type', ['value']
        )

        # Simulate poll structure from KafkaConsumer
        poll_data = [
            {
                'topic_partition': [
                    message_type(value=b'date: date\npage: http://example.com')
                ]
            },
            {}
        ]

        def poll(timeout_ms):
            return poll_data.pop()

        message_consumer.poll.side_effect = poll
        mock_KafkaConsumer.return_value = message_consumer

        assert self.kafka.read() == [
            {'date': 'date', 'page': 'http://example.com'}
        ]

        mock_KafkaConsumer.assert_called_once_with(
            'ms-intro',
            auto_offset_reset='earliest',
            bootstrap_servers='kafka-example.com:12345',
            client_id='msa-client',
            group_id='msa-group',
            security_protocol='SSL',
            ssl_cafile='ca.pem',
            ssl_certfile='service.cert',
            ssl_keyfile='service.key'
        )
