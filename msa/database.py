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
from psycopg2.extras import RealDictCursor
import psycopg2
from textwrap import dedent
from datetime import datetime


class MSADataBase:
    def __init__(self, config_file: str) -> None:
        with open(config_file, 'r') as config:
            self.db_config = yaml.safe_load(config)
        self.db_connection = psycopg2.connect(self.db_config['db_uri'])
        self.db_cursor = self.db_connection.cursor(
            cursor_factory=RealDictCursor
        )

    def delete_table(self) -> None:
        delete_table_webcheck = dedent('''
            DROP TABLE webcheck
        ''').strip()
        self.__execute_and_commit(delete_table_webcheck)

    def create_table(self) -> None:
        create_table_webcheck = dedent('''
            CREATE TABLE webcheck
            (ID INT GENERATED ALWAYS AS IDENTITY,
            PAGE     TEXT        NOT NULL,
            DATE     TIMESTAMP   NOT NULL,
            STATUS   INTEGER     NOT NULL,
            RTIME    REAL        NOT NULL,
            TAG      TEXT)
        ''').strip()
        self.__execute_and_commit(create_table_webcheck)

    def dump_table(self) -> List:
        dump_table_webcheck = dedent('''
            SELECT * FROM webcheck
        ''').strip()
        self.db_cursor.execute(dump_table_webcheck)
        return self.db_cursor.fetchall()

    def insert(
        self, url: str, date: str, status_code: int,
        response_time: float, tag: str = None
    ) -> None:
        request_date = datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S+00:00'
        )
        insert_into_webcheck = dedent('''
            INSERT INTO webcheck
            (PAGE, DATE, STATUS, RTIME, TAG)
            VALUES('{0}', '{1}', {2}, {3}, {4})
        ''').format(
            url,
            request_date,
            status_code,
            response_time,
            f'\'{tag}\'' if tag else 'NULL'
        ).strip()
        self.__execute_and_commit(insert_into_webcheck)

    def __execute_and_commit(self, query):
        self.db_cursor.execute(query)
        self.db_connection.commit()
