import yaml
from psycopg2.extras import RealDictCursor
import psycopg2
from textwrap import dedent
from datetime import datetime


class MSADataBase:
    def __init__(self, config_file: str) -> None:
        with open(config_file, 'r') as config:
            self.db_config = yaml.safe_load(config)
        self.db_connection = psycopg2.connect(self.db_config.get('db_uri'))
        self.db_cursor = self.db_connection.cursor(
            cursor_factory=RealDictCursor
        )

    def delete_table(self) -> None:
        delete_table_webcheck = dedent('''
            DROP TABLE webcheck
        ''').strip()
        self.db_cursor.execute(delete_table_webcheck)
        self.db_connection.commit()

    def create_table(self) -> None:
        create_table_webcheck = dedent('''
            CREATE TABLE webcheck
            (ID INT GENERATED ALWAYS AS IDENTITY,
            PAGE     TEXT        NOT NULL,
            RQAT     TIMESTAMP   NOT NULL,
            STATUS   INTEGER     NOT NULL,
            RTIME    REAL        NOT NULL,
            TAG      TEXT)
        ''').strip()
        self.db_cursor.execute(create_table_webcheck)
        self.db_connection.commit()

    def insert(
        self, url: str, date: str, status_code: int,
        response_time: float, flag: str = None
    ) -> None:
        request_date = datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S+00:00'
        )
        insert_into_webcheck = dedent('''
            INSERT INTO webcheck
            (PAGE, RQAT, STATUS, RTIME, TAG)
            VALUES('{0}', '{1}', {2}, {3}, {4})
        ''').format(
            url,
            request_date,
            status_code,
            response_time,
            f'\'{flag}\'' if flag else 'NULL'
        ).strip()
        self.db_cursor.execute(insert_into_webcheck)
        self.db_connection.commit()
