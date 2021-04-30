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
usage: msa-init -h | --help
       msa-init
           [--init-db]
           [--verbose]

options:
    --init-db
        Optional init the database. Note, this will drop the
        eventually existing table

    --verbose
        Include log information from external modules
"""
from docopt import docopt
from msa.version import __version__
from msa.metrics import MSAMetrics
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
        version='MSA (lookup) version ' + __version__,
        options_first=True
    )
    if args['--verbose']:
        MSALogger.activate_global_info_logging()

    # add setup of kafka and database services here
    # ...

    # check kafka connectivity
    log.info('Connecting to Kafka...')
    metrics = MSAMetrics(url='https://www.google.de')
    kafka = MSAKafka(
        config_file=Defaults.get_kafka_config()
    )
    log.info('--> Sending/Receiving Google metrics for testing...')
    kafka.send(metrics)
    log.info(f'--> {kafka.read()}')
    log.info('OK')

    # check database connectivity
    log.info('Connecting to PostgreSQL...')
    db = MSADataBase(
        config_file=Defaults.get_db_config()
    )
    if args['--init-db']:
        log.info('--> Recreate DB table setup')
        db.delete_table()
        db.create_table()
    log.info('OK')
