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
import logging


class MSALogger:
    @staticmethod
    def get_logger(level=logging.INFO):
        log = logging.getLogger('msa')
        log.setLevel(level)
        channel = logging.StreamHandler()
        channel.setLevel(level)
        log.addHandler(channel)
        return log

    @staticmethod
    def activate_global_info_logging():
        logging.basicConfig(level=logging.INFO)
