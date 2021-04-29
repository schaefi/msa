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

# 1. lookup the metrics of the web site
# 2. store the information as a message in kafka


def main():
    args = docopt(
        __doc__,
        version='MSA (lookup) version ' + __version__,
        options_first=True
    )

    metrics = MSAMetrics(url=args['--page'])

    print(f'Status: {metrics.get_status_code()}')
    print(f'Time(sec): {metrics.get_response_time()}')
    print(f'Date: {metrics.get_response_date()}')
    if args['--regexp']:
        print(f'Tag: {metrics.get_flag_status(args["--regexp"])}')

    # store the information as a message in kafka
    # Something like
    # kafka = MSAKafka(metrics)
    # kafka.send()
