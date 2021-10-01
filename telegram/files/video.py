#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2021
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Telegram Video."""

from typing import TYPE_CHECKING, Any

from telegram import PhotoSize
from telegram.files.basemedium import _BaseMedium
from telegram.files.mediaattrmixins import (
    _DurationMixin,
    _FileNameMixin,
    _MimeTypeMixin,
    _ThumbPsMixin,
    _WidthHeightMixin,
)

if TYPE_CHECKING:
    from telegram import Bot

Ancestors = (
    _BaseMedium,
    _DurationMixin,
    _FileNameMixin,
    _MimeTypeMixin,
    _ThumbPsMixin,
    _WidthHeightMixin,
)


class Video(*Ancestors):  # type: ignore[too-many-ancestors, misc]
    """This object represents a video file.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        width (:obj:`int`): Video width as defined by sender.
        height (:obj:`int`): Video height as defined by sender.
        duration (:obj:`int`): Duration of the video in seconds as defined by sender.
        thumb (:class:`telegram.PhotoSize`, optional): Video thumbnail.
        file_name (:obj:`str`, optional): Original filename as defined by sender.
        mime_type (:obj:`str`, optional): Mime type of a file as defined by sender.
        file_size (:obj:`int`, optional): File size.
        bot (:class:`telegram.Bot`, optional): The Bot to use for instance methods.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    Attributes:
        file_id (:obj:`str`): Identifier for this file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        width (:obj:`int`): Video width as defined by sender.
        height (:obj:`int`): Video height as defined by sender.
        duration (:obj:`int`): Duration of the video in seconds as defined by sender.
        thumb (:class:`telegram.PhotoSize`): Optional. Video thumbnail.
        file_name (:obj:`str`): Optional. Original filename as defined by sender.
        mime_type (:obj:`str`): Optional. Mime type of a file as defined by sender.
        file_size (:obj:`int`): Optional. File size.
        bot (:class:`telegram.Bot`): Optional. The Bot to use for instance methods.

    """

    __slots__ = ('duration', 'height', 'mime_type', 'thumb', 'width')

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        duration: int,
        thumb: PhotoSize = None,
        mime_type: str = None,
        file_size: int = None,
        bot: 'Bot' = None,
        file_name: str = None,
        **_kwargs: Any,
    ):
        super().__init__(file_id, file_unique_id, file_size, bot)
        _DurationMixin.__init__(self, duration)
        _FileNameMixin.__init__(self, file_name)
        _MimeTypeMixin.__init__(self, mime_type)
        _ThumbPsMixin.__init__(self, thumb)
        _WidthHeightMixin.__init__(self, width, height)
