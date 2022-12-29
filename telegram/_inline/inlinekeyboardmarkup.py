#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
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
"""This module contains an object that represents a Telegram InlineKeyboardMarkup."""
from typing import TYPE_CHECKING, List, Optional, Sequence

from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._telegramobject import TelegramObject
from telegram._utils.markup import check_keyboard_type
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class InlineKeyboardMarkup(TelegramObject):
    """
    This object represents an inline keyboard that appears right next to the message it belongs to.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their size of :attr:`inline_keyboard` and all the buttons are equal.

    Examples:
        * :any:`Inline Keyboard 1 <examples.inlinekeyboard>`
        * :any:`Inline Keyboard 2 <examples.inlinekeyboard2>`

    Args:
        inline_keyboard (Sequence[Sequence[:class:`telegram.InlineKeyboardButton`]]): Sequence of
            button rows, each represented by a sequence of :class:`~telegram.InlineKeyboardButton`
            objects.

            .. versionchanged:: 20.0
                |sequenceclassargs|

    Attributes:
        inline_keyboard (Tuple[Tuple[:class:`telegram.InlineKeyboardButton`]]): Tuple of
            button rows, each represented by a tuple of :class:`~telegram.InlineKeyboardButton`
            objects.

            .. versionchanged:: 20.0
                |tupleclassattrs|

    """

    __slots__ = ("inline_keyboard",)

    def __init__(
        self,
        inline_keyboard: Sequence[Sequence[InlineKeyboardButton]],
        *,
        api_kwargs: JSONDict = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        if not check_keyboard_type(inline_keyboard):
            raise ValueError(
                "The parameter `inline_keyboard` should be a sequence of sequences of "
                "InlineKeyboardButtons"
            )
        # Required
        self.inline_keyboard = tuple(tuple(row) for row in inline_keyboard)

        self._id_attrs = (self.inline_keyboard,)

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["InlineKeyboardMarkup"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        if not data:
            return None

        keyboard = []
        for row in data["inline_keyboard"]:
            tmp = []
            for col in row:
                btn = InlineKeyboardButton.de_json(col, bot)
                if btn:
                    tmp.append(btn)
            keyboard.append(tmp)

        return cls(keyboard)

    @classmethod
    def from_button(cls, button: InlineKeyboardButton, **kwargs: object) -> "InlineKeyboardMarkup":
        """Shortcut for::

            InlineKeyboardMarkup([[button]], **kwargs)

        Return an InlineKeyboardMarkup from a single InlineKeyboardButton

        Args:
            button (:class:`telegram.InlineKeyboardButton`): The button to use in the markup

        """
        return cls([[button]], **kwargs)  # type: ignore[arg-type]

    @classmethod
    def from_row(
        cls, button_row: Sequence[InlineKeyboardButton], **kwargs: object
    ) -> "InlineKeyboardMarkup":
        """Shortcut for::

            InlineKeyboardMarkup([button_row], **kwargs)

        Return an InlineKeyboardMarkup from a single row of InlineKeyboardButtons

        Args:
            button_row (Sequence[:class:`telegram.InlineKeyboardButton`]): The button to use
                in the markup

                .. versionchanged:: 20.0
                    Accept :obj:`Sequence` instead of :obj:`List`.

        """
        return cls([button_row], **kwargs)  # type: ignore[arg-type]

    @classmethod
    def from_column(
        cls, button_column: Sequence[InlineKeyboardButton], **kwargs: object
    ) -> "InlineKeyboardMarkup":
        """Shortcut for::

            InlineKeyboardMarkup([[button] for button in button_column], **kwargs)

        Return an InlineKeyboardMarkup from a single column of InlineKeyboardButtons

        Args:
            button_column (Sequence[:class:`telegram.InlineKeyboardButton`]): The button to use
                in the markup

                 .. versionchanged:: 20.0
                    Accept :obj:`Sequence` instead of :obj:`List`.

        """
        button_grid = [[button] for button in button_column]
        return cls(button_grid, **kwargs)  # type: ignore[arg-type]
