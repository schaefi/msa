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
from logging import Logger


class MSALogger:
    """
    Implements the "msa" logger
    """
    @staticmethod
    def get_logger(level: int = logging.INFO) -> Logger:
        """
        Configure "msa" logger

        Simple logger responding to logging.INFO level by default
        The logger is only created once, thus multiple get_logger()
        calls are allowed

        :param int level: log level

        :return: log handler

        :rtype: Logger
        """
        log = logging.getLogger('msa')
        if not log.hasHandlers():
            log.setLevel(level)
            channel = logging.StreamHandler()
            channel.setLevel(level)
            log.addHandler(channel)
        return log

    @staticmethod
    def activate_global_info_logging() -> None:
        """
        Configure applicaton global log level

        Sets the global log level to logging.INFO. This causes
        all modules, also outside of the msa scope, to show
        their info logs
        """
        logging.basicConfig(level=logging.INFO)
