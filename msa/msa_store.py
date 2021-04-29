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
"""
from docopt import docopt
from msa.version import __version__

# 1. read from the kafka topic
# 2. store the information in the database


def main():
    args = docopt(
        __doc__,
        version='MSA (store) version ' + __version__,
        options_first=True
    )

    print(f'Here we go... {args}')
