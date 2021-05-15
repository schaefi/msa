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
from msa.exceptions import (
    MSAConfigFileNotFoundError,
    MSADatabaseQueryException,
    MSADatabaseConnectionException
)


class MSADataBase:
    """
    Implements PostgreSQL database handling
    """
    def __init__(self, config_file: str) -> None:
        """
        Create new instance of MSADataBase

        At creation time the connection to the database
        is established

        :param str config_file: DB credentials file

            .. code:: yaml

                db_uri: postgres://...
        """
        try:
            with open(config_file, 'r') as config:
                self.db_config = yaml.safe_load(config)
        except Exception as issue:
            raise MSAConfigFileNotFoundError(issue)
        try:
            self.db_connection = psycopg2.connect(self.db_config['db_uri'])
            self.db_cursor = self.db_connection.cursor(
                cursor_factory=RealDictCursor
            )
        except Exception as issue:
            raise MSADatabaseConnectionException(
                f'Database connection failed with: {issue!r}'
            )
        self.metrics_table_name = 'webcheck'

    def delete_table(self) -> None:
        """
        Delete Table
        """
        delete_table = dedent('''
            DROP TABLE IF EXISTS {table}
        ''').format(table=self.metrics_table_name).strip()
        self.__execute(delete_table)

    def create_table(self) -> None:
        """
        Create table

        ID | PAGE | DATE | STATUS | RTIME | TAG

        * ID: Self generated entry id
        * PAGE: Web page URI
        * DATE: Date
        * STATUS: Request status code
        * RTIME: Request response time
        * TAG: Free form tag data associated with request content
        """
        create_table = dedent('''
            CREATE TABLE {table}
            (ID INT GENERATED ALWAYS AS IDENTITY,
            PAGE     TEXT        NOT NULL,
            DATE     TIMESTAMP   NOT NULL,
            STATUS   INTEGER     NOT NULL,
            RTIME    REAL        NOT NULL,
            TAG      TEXT)
        ''').format(table=self.metrics_table_name).strip()
        self.__execute(create_table)

    def dump_table(self) -> List:
        """
        Select from table and returns its contents

        :return: Returns a list of RealDictRow entries

        :rtype: list
        """
        dump_table = dedent('''
            SELECT * FROM {table}
        ''').format(table=self.metrics_table_name).strip()
        self.__execute(dump_table, commit=False)
        return self.db_cursor.fetchall()

    def insert(
        self, url: str, date: str, status_code: int,
        response_time: float, tag: str = None
    ) -> None:
        """
        Insert into table

        :param str url: Web page URI
        :param str date: date of the format: %Y-%m-%dT%H:%M:%S+00:00
        :param int status_code: request status code
        :param float response_time: request response time
        :param str tag: free form tag data associated with request content
        """
        request_date = datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S+00:00'
        )
        insert_into = dedent('''
            INSERT INTO {table}
            (PAGE, DATE, STATUS, RTIME, TAG)
            VALUES($${page}$$, '{date}', {status}, {rtime}, $${tag}$$)
        ''').format(
            table=self.metrics_table_name,
            page=url,
            date=request_date,
            status=status_code,
            rtime=response_time,
            tag=tag if tag else 'NULL'
        ).strip()
        self.__execute(insert_into)

    def __execute(self, query: str, commit: bool = True) -> None:
        """
        Execute and optionally commit a given query

        :param str query: SQL query
        :param bool commit: For write actions, commit into DB
        """
        try:
            self.db_cursor.execute(query)
            if commit:
                self.db_connection.commit()
        except Exception as issue:
            raise MSADatabaseQueryException(
                f'Database transaction failed with: {issue!r}'
            )
