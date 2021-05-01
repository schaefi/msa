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
           [--log-file=<logfile>]
           [--verbose]
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

    --log-file=<logfile>
        Optional log file setup

    --verbose
        Include log information from external modules
"""
from apscheduler.schedulers.background import BlockingScheduler
from typing import List
from docopt import docopt
from msa.version import __version__
from msa.kafka import MSAKafka
from msa.database import MSADataBase
from msa.defaults import Defaults
from msa.logger import MSALogger
from msa.exceptions import exception_handler

log = MSALogger.get_logger()


@exception_handler
def main() -> None:
    args = docopt(
        __doc__,
        version='MSA (store) version ' + __version__,
        options_first=True
    )
    if args['--verbose']:
        MSALogger.activate_global_info_logging()
    if args['--log-file']:
        MSALogger.set_logfile(args['--log-file'])

    log.info('Opening database connection...')
    db = MSADataBase(
        config_file=Defaults.get_db_config()
    )

    if args['--dump-db']:
        log.info('Database has the following entries:')
        for entry in db.dump_table():
            log.info(entry)
        return

    log.info('Opening kafka messaging...')
    kafka = MSAKafka(
        config_file=Defaults.get_kafka_config()
    )

    store_to_database(kafka.read(), db)
    if args['--single-shot']:
        return

    db_scheduler = BlockingScheduler()
    db_scheduler.add_job(
        lambda: store_to_database(kafka.read(), db),
        'interval', seconds=args['--update-interval'] or 30
    )
    db_scheduler.start()


def store_to_database(messages: List, db: MSADataBase):
    for message in messages:
        log.info('Writing message to database...')
        log.info(f'--> {message}')
        db.insert(
            message['page'],
            message['date'],
            message['status'],
            message['rtime'],
            message['tag']
        )
