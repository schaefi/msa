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
"""
usage: msa-store -h | --help
       msa-store
           [--update-interval=<time_sec>]
           [--single-shot]
       msa-store --dump-db

options:
    --dump-db
        Print the database

    --single-shot
        Optionally run once, read present messages and store them
        in the database.

    --update-interval=<time_sec>
        Optional update interval to check for messages and
        writing into the database. Default is 30sec
"""
from typing import List
from docopt import docopt
from msa.version import __version__
from msa.kafka import MSAKafka
from msa.database import MSADataBase
from msa.defaults import Defaults
from msa.logger import MSALogger

log = MSALogger.get_logger()


def main() -> None:
    args = docopt(
        __doc__,
        version='MSA (store) version ' + __version__,
        options_first=True
    )

    db = MSADataBase(
        config_file=Defaults.get_db_config()
    )

    if args['--dump-db']:
        for entry in db.dump_table():
            log.info(entry)
        return

    kafka = MSAKafka(
        config_file=Defaults.get_kafka_config()
    )

    if args['--single-shot']:
        store_to_database(kafka.read(), db)
        return

    # print(kafka.read())
    # TODO: implement interval timer,
    # store the information in the database,
    # fork as a daemon


def store_to_database(messages: List, db: MSADataBase):
    for message in messages:
        log.info('Writing message to database...')
        log.info(f'--> {message}')
        db.insert(
            message.get('page'), message.get('date'),
            message.get('status'), message.get('rtime'),
            message.get('tag')
        )
