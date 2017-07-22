#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2017
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
"""This module contains the classes that represent Telegram InlineQueryResultCachedVoice"""

from telegram import InlineQueryResult, InlineKeyboardMarkup, InputMessageContent


class InlineQueryResultCachedVoice(InlineQueryResult):
    """
    Represents a link to a voice message stored on the Telegram servers. By default, this voice
    message will be sent by the user. Alternatively, you can use :attr:`input_message_content` to
    send a message with the specified content instead of the voice message.

    Attributes:
        type (:obj:`str`): 'voice'.
        id (:obj:`str`): Unique identifier for this result, 1-64 bytes.
        voice_file_id (:obj:`str`): A valid file identifier for the voice message.
        title (:obj:`str`): Voice message title.
        caption (:obj:`str`): Optional. Caption, 0-200 characters.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the voice.

    Args:
        id (:obj:`str`): Unique identifier for this result, 1-64 bytes.
        voice_file_id (:obj:`str`): A valid file identifier for the voice message.
        title (:obj:`str`): Voice message title.
        caption (:obj:`str`, optional): Caption, 0-200 characters.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the voice.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.
    """

    def __init__(self,
                 id,
                 voice_file_id,
                 title,
                 caption=None,
                 reply_markup=None,
                 input_message_content=None,
                 **kwargs):
        # Required
        super(InlineQueryResultCachedVoice, self).__init__('voice', id)
        self.voice_file_id = voice_file_id
        self.title = title

        # Optionals
        if caption:
            self.caption = caption
        if reply_markup:
            self.reply_markup = reply_markup
        if input_message_content:
            self.input_message_content = input_message_content

    @staticmethod
    def de_json(data, bot):
        data = super(InlineQueryResultCachedVoice, InlineQueryResultCachedVoice).de_json(data, bot)

        data['reply_markup'] = InlineKeyboardMarkup.de_json(data.get('reply_markup'), bot)
        data['input_message_content'] = InputMessageContent.de_json(
            data.get('input_message_content'), bot)

        return InlineQueryResultCachedVoice(**data)
