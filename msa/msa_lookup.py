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
usage: msa-lookup -h | --help
       msa-lookup --page=<uri>
           [--regexp=<expression>]

options:
    --regexp=<expression>
        Optional expression to match against the page content.
"""
from docopt import docopt
from msa.version import __version__
from msa.metrics import MSAMetrics
from msa.kafka import MSAKafka
from msa.defaults import Defaults


def main() -> None:
    args = docopt(
        __doc__,
        version='MSA (lookup) version ' + __version__,
        options_first=True
    )

    metrics = MSAMetrics(
        url=args['--page'], matches=args['--regexp']
    )

    kafka = MSAKafka(
        config_file=Defaults.get_kafka_config()
    )
    kafka.send(metrics)
