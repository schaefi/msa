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
import os


class Defaults:
    @staticmethod
    def get_db_config():
        return os.path.join(Defaults.__conf_path(), 'db.yml')

    @staticmethod
    def get_kafka_config():
        return os.path.join(Defaults.__conf_path(), 'kafka.yml')

    @staticmethod
    def __conf_path():
        return os.path.join(
            os.environ.get('HOME'), '.config/msa'
        )
