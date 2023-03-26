#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
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
"""This module contains the classes that represent Telegram InlineQueryResultVenue."""

from typing import TYPE_CHECKING, Optional

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._utils.types import JSONDict
from telegram._utils.warnings_transition import (
    warn_about_deprecated_arg_return_new_arg,
    warn_about_deprecated_attr_in_property,
)
from telegram.constants import InlineQueryResultType

if TYPE_CHECKING:
    from telegram import InputMessageContent


class InlineQueryResultVenue(InlineQueryResult):
    """
    Represents a venue. By default, the venue will be sent by the user. Alternatively, you can
    use :attr:`input_message_content` to send a message with the specified content instead of the
    venue.

    Note:
      Foursquare details and Google Pace details are mutually exclusive. However, this
      behaviour is undocumented and might be changed by Telegram.

    Args:
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        latitude (:obj:`float`): Latitude of the venue location in degrees.
        longitude (:obj:`float`): Longitude of the venue location in degrees.
        title (:obj:`str`): Title of the venue.
        address (:obj:`str`): Address of the venue.
        foursquare_id (:obj:`str`, optional): Foursquare identifier of the venue if known.
        foursquare_type (:obj:`str`, optional): Foursquare type of the venue, if known.
            (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or
            "food/icecream".)
        google_place_id (:obj:`str`, optional): Google Places identifier of the venue.
        google_place_type (:obj:`str`, optional): Google Places type of the venue. (See
            `supported types <https://developers.google.com/maps/documentation/places/web-service\
            /supported_types>`_.)
        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the venue.
        thumb_url (:obj:`str`, optional): Url of the thumbnail for the result.

            .. deprecated:: 20.2
               |thumbargumentdeprecation| :paramref:`thumbnail_url`.
        thumb_width (:obj:`int`, optional): Thumbnail width.

            .. deprecated:: 20.2
               |thumbargumentdeprecation| :paramref:`thumbnail_width`.
        thumb_height (:obj:`int`, optional): Thumbnail height.

            .. deprecated:: 20.2
               |thumbargumentdeprecation| :paramref:`thumbnail_height`.
        thumbnail_url (:obj:`str`, optional): Url of the thumbnail for the result.

            .. versionadded:: 20.2
        thumbnail_width (:obj:`int`, optional): Thumbnail width.

            .. versionadded:: 20.2
        thumbnail_height (:obj:`int`, optional): Thumbnail height.

            .. versionadded:: 20.2

    Attributes:
        type (:obj:`str`): :tg-const:`telegram.constants.InlineQueryResultType.VENUE`.
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        latitude (:obj:`float`): Latitude of the venue location in degrees.
        longitude (:obj:`float`): Longitude of the venue location in degrees.
        title (:obj:`str`): Title of the venue.
        address (:obj:`str`): Address of the venue.
        foursquare_id (:obj:`str`): Optional. Foursquare identifier of the venue if known.
        foursquare_type (:obj:`str`): Optional. Foursquare type of the venue, if known.
            (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or
            "food/icecream".)
        google_place_id (:obj:`str`): Optional. Google Places identifier of the venue.
        google_place_type (:obj:`str`): Optional. Google Places type of the venue. (See
            `supported types <https://developers.google.com/maps/documentation/places/web-service\
            /supported_types>`_.)
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the venue.
        thumbnail_url (:obj:`str`): Optional. Url of the thumbnail for the result.

            .. versionadded:: 20.2
        thumbnail_width (:obj:`int`): Optional. Thumbnail width.

            .. versionadded:: 20.2
        thumbnail_height (:obj:`int`): Optional. Thumbnail height.

            .. versionadded:: 20.2

    """

    __slots__ = (
        "longitude",
        "reply_markup",
        "google_place_type",
        "thumbnail_width",
        "thumbnail_height",
        "title",
        "address",
        "foursquare_id",
        "foursquare_type",
        "google_place_id",
        "input_message_content",
        "latitude",
        "thumbnail_url",
    )

    def __init__(
        self,
        id: str,  # pylint: disable=redefined-builtin
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: str = None,
        foursquare_type: str = None,
        reply_markup: InlineKeyboardMarkup = None,
        input_message_content: "InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = None,
        thumb_height: int = None,
        google_place_id: str = None,
        google_place_type: str = None,
        thumbnail_url: str = None,
        thumbnail_width: int = None,
        thumbnail_height: int = None,
        *,
        api_kwargs: JSONDict = None,
    ):
        # Required
        super().__init__(InlineQueryResultType.VENUE, id, api_kwargs=api_kwargs)
        with self._unfrozen():
            self.latitude: float = latitude
            self.longitude: float = longitude
            self.title: str = title
            self.address: str = address

            # Optional
            self.foursquare_id: Optional[str] = foursquare_id
            self.foursquare_type: Optional[str] = foursquare_type
            self.google_place_id: Optional[str] = google_place_id
            self.google_place_type: Optional[str] = google_place_type
            self.reply_markup: Optional[InlineKeyboardMarkup] = reply_markup
            self.input_message_content: Optional[InputMessageContent] = input_message_content
            self.thumbnail_url: Optional[str] = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_url,
                new_arg=thumbnail_url,
                deprecated_arg_name="thumb_url",
                new_arg_name="thumbnail_url",
                bot_api_version="6.6",
            )
            self.thumbnail_width: Optional[int] = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_width,
                new_arg=thumbnail_width,
                deprecated_arg_name="thumb_width",
                new_arg_name="thumbnail_width",
                bot_api_version="6.6",
            )
            self.thumbnail_height: Optional[int] = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_height,
                new_arg=thumbnail_height,
                deprecated_arg_name="thumb_height",
                new_arg_name="thumbnail_height",
                bot_api_version="6.6",
            )

    @property
    def thumb_url(self) -> Optional[str]:
        """:obj:`str`: Optional. Url of the thumbnail for the result.

        .. deprecated:: 20.2
           |thumbattributedeprecation| :attr:`thumbnail_url`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_url",
            new_attr_name="thumbnail_url",
            bot_api_version="6.6",
        )
        return self.thumbnail_url

    @property
    def thumb_width(self) -> Optional[int]:
        """:obj:`str`: Optional. Thumbnail width.

        .. deprecated:: 20.2
           |thumbattributedeprecation| :attr:`thumbnail_width`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_width",
            new_attr_name="thumbnail_width",
            bot_api_version="6.6",
        )
        return self.thumbnail_width

    @property
    def thumb_height(self) -> Optional[int]:
        """:obj:`str`: Optional. Thumbnail height.

        .. deprecated:: 20.2
           |thumbattributedeprecation| :attr:`thumbnail_height`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_height",
            new_attr_name="thumbnail_height",
            bot_api_version="6.6",
        )
        return self.thumbnail_height
