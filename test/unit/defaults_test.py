from mock import patch
from msa.defaults import Defaults


class TestDefaults:
    def test_get_db_config(self):
        with patch.dict('os.environ', {'HOME': 'users_home'}):
            assert Defaults.get_db_config() == \
                'users_home/.config/msa/db.yml'

    def test_get_kafka_config(self):
        with patch.dict('os.environ', {'HOME': 'users_home'}):
            assert Defaults.get_kafka_config() == \
                'users_home/.config/msa/kafka.yml'
