from mock import (
    Mock, patch
)
from textwrap import dedent
from msa.database import MSADataBase


class TestMSADataBase:
    @patch('psycopg2.connect')
    def setup(self, mock_psycopg2_connect):
        self.db_connection = Mock()
        mock_psycopg2_connect.return_value = self.db_connection
        self.msa_db = MSADataBase('../data/db.yml')

    def test_delete_table(self):
        self.msa_db.delete_table()
        self.msa_db.db_cursor.execute.assert_called_once_with(
            'DROP TABLE webcheck'
        )

    def test_create_table(self):
        self.msa_db.create_table()
        create_table_webcheck = dedent('''
            CREATE TABLE webcheck
            (ID INT GENERATED ALWAYS AS IDENTITY,
            RQAT     TIMESTAMP   NOT NULL,
            STATUS   INTEGER     NOT NULL,
            RTIME    REAL        NOT NULL,
            TAG      TEXT);
        ''').strip()
        self.msa_db.db_cursor.execute.assert_called_once_with(
            create_table_webcheck
        )

    @patch('msa.database.datetime')
    def test_insert_table(self, mock_datetime):
        strftime = Mock()
        strftime.strftime = Mock(return_value='current_date')
        mock_datetime.utcnow = Mock(
            return_value=strftime
        )
        # test on insert with NULL type tag
        self.msa_db.insert(404, 42)
        insert_into_webcheck = dedent('''
            INSERT INTO webcheck
            (RQAT, STATUS, RTIME, TAG) VALUES ('current_date', 404, 42, NULL)
        ''').strip()
        self.msa_db.db_cursor.execute.assert_called_once_with(
            insert_into_webcheck
        )
        # test on insert with some tag
        self.msa_db.db_cursor.execute.reset_mock()
        self.msa_db.insert(404, 42, 'tag')
        insert_into_webcheck = dedent('''
            INSERT INTO webcheck
            (RQAT, STATUS, RTIME, TAG) VALUES ('current_date', 404, 42, 'tag')
        ''').strip()
        self.msa_db.db_cursor.execute.assert_called_once_with(
            insert_into_webcheck
        )
