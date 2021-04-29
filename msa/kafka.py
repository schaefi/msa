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
from typing import List
import yaml
from kafka import KafkaConsumer
from kafka import KafkaProducer
from msa.metrics import MSAMetrics


class MSAKafka:
    def __init__(self, config_file: str) -> None:
        with open(config_file, 'r') as config:
            self.kafka_config = yaml.safe_load(config)
        self.kafka_host = self.kafka_config['host']
        self.kafka_topic = self.kafka_config['topic']
        self.kafka_ca = self.kafka_config['ssl_cafile']
        self.kafka_cert = self.kafka_config['ssl_certfile']
        self.kafka_key = self.kafka_config['ssl_keyfile']

    def send(self, metrics: MSAMetrics) -> None:
        message_broker = self.__create_ssl_broker()
        metrics_dict = {
            'page': metrics.get_page(),
            'date': metrics.get_response_date(),
            'status': metrics.get_status_code(),
            'rtime': metrics.get_response_time(),
            'tag': metrics.get_tag()
        }
        message_broker.send(
            self.kafka_topic, yaml.dump(metrics_dict).encode()
        )
        # We want this message to go out now
        message_broker.flush()

    def read(self, timeout_ms=1000) -> List:
        metrics_list = []
        message_consumer = self.__create_ssl_consumer()
        # Call poll twice. First call will just assign partitions
        # for the consumer without content. This information was
        # taken from the Aiven help center
        for _ in range(2):
            raw_messages = message_consumer.poll(timeout_ms=timeout_ms)
            for topic_partition, message_list in raw_messages.items():
                for message in message_list:
                    metrics_list.append(
                        yaml.safe_load(message.value)
                    )
        # Acknowledge message so we don't get it again for
        # this client/group
        message_consumer.commit()
        return metrics_list

    def __create_ssl_broker(self) -> KafkaProducer:
        return KafkaProducer(
            security_protocol='SSL',
            bootstrap_servers=self.kafka_host,
            ssl_cafile=self.kafka_ca,
            ssl_certfile=self.kafka_cert,
            ssl_keyfile=self.kafka_key
        )

    def __create_ssl_consumer(
        self, client='msa-client', group='msa-group'
    ) -> KafkaConsumer:
        return KafkaConsumer(
            self.kafka_topic,
            auto_offset_reset='earliest',
            bootstrap_servers=self.kafka_host,
            client_id=client,
            group_id=group,
            security_protocol='SSL',
            ssl_cafile=self.kafka_ca,
            ssl_certfile=self.kafka_cert,
            ssl_keyfile=self.kafka_key
        )
