import logging
from mock import (
    Mock, patch
)
from pytest import (
    raises, fixture
)
from collections import namedtuple
from msa.kafka import MSAKafka
from msa.exceptions import (
    MSAConfigFileNotFoundError,
    MSAKafkaProducerException,
    MSAKafkaConsumerException
)


class TestMSAKafka:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def setup(self):
        self.kafka = MSAKafka('../data/kafka.yml')

    def test_config_file_not_found(self):
        with raises(MSAConfigFileNotFoundError):
            MSAKafka('../data/foo')

    @patch('msa.kafka.KafkaConsumer')
    def test_kafka_consumer_raises(self, mock_KafkaConsumer):
        mock_KafkaConsumer.side_effect = Exception
        with raises(MSAKafkaConsumerException):
            self.kafka.read()

    @patch('msa.kafka.KafkaProducer')
    def test_kafka_producer_raises(self, mock_KafkaProducer):
        mock_KafkaProducer.side_effect = Exception
        with raises(MSAKafkaProducerException):
            self.kafka.send(Mock())

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
            b'time\nstatus: 42\ntag: null\nversion: 0.1\n'
        )

    @patch('msa.kafka.KafkaConsumer')
    def test_read_invalid_yaml(self, mock_KafkaConsumer):
        message_consumer = Mock()
        message_type = namedtuple(
            'message_type', ['value']
        )

        # Simulate poll structure from KafkaConsumer
        # Message includes invalid YAML
        poll_data = [
            {
                'topic_partition': [
                    message_type(value=b'{this is invalid')
                ]
            },
            {}
        ]

        def poll(timeout_ms):
            return poll_data.pop()

        message_consumer.poll.side_effect = poll
        mock_KafkaConsumer.return_value = message_consumer

        with self._caplog.at_level(logging.ERROR):
            self.kafka.read()
            assert "ParserError('while parsing a flow mapping" in \
                self._caplog.text

    @patch('msa.kafka.KafkaConsumer')
    def test_read_invalid_for_transport_schema(self, mock_KafkaConsumer):
        message_consumer = Mock()
        message_type = namedtuple(
            'message_type', ['value']
        )

        # Simulate poll structure from KafkaConsumer
        # Message includes valid yaml but invalid schema
        poll_data = [
            {
                'topic_partition': [
                    message_type(value=b'page: http://example.com')
                ]
            },
            {}
        ]

        def poll(timeout_ms):
            return poll_data.pop()

        message_consumer.poll.side_effect = poll
        mock_KafkaConsumer.return_value = message_consumer

        with self._caplog.at_level(logging.ERROR):
            self.kafka.read()
            assert "{'date': ['required field']" in self._caplog.text

    @patch('msa.kafka.KafkaConsumer')
    def test_read(self, mock_KafkaConsumer):
        message_consumer = Mock()
        message_type = namedtuple(
            'message_type', ['value']
        )

        # Simulate poll structure from KafkaConsumer
        # Message includes good data
        poll_data = [
            {
                'topic_partition': [
                    message_type(
                        value=b'page: http://example.com\n'
                        b'date: date\nstatus: 42\nrtime: 42\ntag: tag\n'
                        b'version: 0.1\n'
                    )
                ]
            },
            {}
        ]

        def poll(timeout_ms):
            return poll_data.pop()

        message_consumer.poll.side_effect = poll
        mock_KafkaConsumer.return_value = message_consumer

        assert self.kafka.read() == [
            {
                'version': 0.1,
                'page': 'http://example.com',
                'date': 'date',
                'status': 42,
                'rtime': 42,
                'tag': 'tag'
            }
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
