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

import pytest

from telegram import CallbackQuery, User, Message, Chat, Audio, Bot
from tests.conftest import check_shortcut_signature, check_shortcut_call, check_defaults_handling


@pytest.fixture(scope='function', params=['message', 'inline'])
def callback_query(bot, request):
    cbq = CallbackQuery(
        TestCallbackQuery.id_,
        TestCallbackQuery.from_user,
        TestCallbackQuery.chat_instance,
        data=TestCallbackQuery.data,
        game_short_name=TestCallbackQuery.game_short_name,
        bot=bot,
    )
    if request.param == 'message':
        cbq.message = TestCallbackQuery.message
        cbq.message.bot = bot
    else:
        cbq.inline_message_id = TestCallbackQuery.inline_message_id
    return cbq


class TestCallbackQuery:
    id_ = 'id'
    from_user = User(1, 'test_user', False)
    chat_instance = 'chat_instance'
    message = Message(3, None, Chat(4, 'private'), from_user=User(5, 'bot', False))
    data = 'data'
    inline_message_id = 'inline_message_id'
    game_short_name = 'the_game'

    def test_slot_behaviour(self, callback_query, recwarn, mro_slots):
        for attr in callback_query.__slots__:
            assert getattr(callback_query, attr, 'err') != 'err', f"got extra slot '{attr}'"
        assert not callback_query.__dict__, f"got missing slot(s): {callback_query.__dict__}"
        assert len(mro_slots(callback_query)) == len(set(mro_slots(callback_query))), "same slot"
        callback_query.custom, callback_query.id = 'should give warning', self.id_
        assert len(recwarn) == 1 and 'custom' in str(recwarn[0].message), recwarn.list

    @staticmethod
    def skip_params(callback_query: CallbackQuery):
        if callback_query.inline_message_id:
            return {'message_id', 'chat_id'}
        return {'inline_message_id'}

    @staticmethod
    def shortcut_kwargs(callback_query: CallbackQuery):
        if not callback_query.inline_message_id:
            return {'message_id', 'chat_id'}
        return {'inline_message_id'}

    @staticmethod
    def check_passed_ids(callback_query: CallbackQuery, kwargs):
        if callback_query.inline_message_id:
            id_ = kwargs['inline_message_id'] == callback_query.inline_message_id
            chat_id = kwargs['chat_id'] is None
            message_id = kwargs['message_id'] is None
        else:
            id_ = kwargs['inline_message_id'] is None
            chat_id = kwargs['chat_id'] == callback_query.message.chat_id
            message_id = kwargs['message_id'] == callback_query.message.message_id
        return id_ and chat_id and message_id

    def test_de_json(self, bot):
        json_dict = {
            'id': self.id_,
            'from': self.from_user.to_dict(),
            'chat_instance': self.chat_instance,
            'message': self.message.to_dict(),
            'data': self.data,
            'inline_message_id': self.inline_message_id,
            'game_short_name': self.game_short_name,
        }
        callback_query = CallbackQuery.de_json(json_dict, bot)

        assert callback_query.id == self.id_
        assert callback_query.from_user == self.from_user
        assert callback_query.chat_instance == self.chat_instance
        assert callback_query.message == self.message
        assert callback_query.data == self.data
        assert callback_query.inline_message_id == self.inline_message_id
        assert callback_query.game_short_name == self.game_short_name

    def test_to_dict(self, callback_query):
        callback_query_dict = callback_query.to_dict()

        assert isinstance(callback_query_dict, dict)
        assert callback_query_dict['id'] == callback_query.id
        assert callback_query_dict['from'] == callback_query.from_user.to_dict()
        assert callback_query_dict['chat_instance'] == callback_query.chat_instance
        if callback_query.message:
            assert callback_query_dict['message'] == callback_query.message.to_dict()
        else:
            assert callback_query_dict['inline_message_id'] == callback_query.inline_message_id
        assert callback_query_dict['data'] == callback_query.data
        assert callback_query_dict['game_short_name'] == callback_query.game_short_name

    def test_answer(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            return kwargs['callback_query_id'] == callback_query.id

        assert check_shortcut_signature(
            CallbackQuery.answer, Bot.answer_callback_query, ['callback_query_id'], []
        )
        assert check_shortcut_call(
            callback_query.answer, callback_query.bot, 'answer_callback_query'
        )
        assert check_defaults_handling(callback_query.answer, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'answer_callback_query', make_assertion)
        # TODO: PEP8
        assert callback_query.answer()

    def test_edit_message_text(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            text = kwargs['text'] == 'test'
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and text

        assert check_shortcut_signature(
            CallbackQuery.edit_message_text,
            Bot.edit_message_text,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.edit_message_text,
            callback_query.bot,
            'edit_message_text',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(callback_query.edit_message_text, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'edit_message_text', make_assertion)
        assert callback_query.edit_message_text(text='test')
        assert callback_query.edit_message_text('test')

    def test_edit_message_caption(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            caption = kwargs['caption'] == 'new caption'
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and caption

        assert check_shortcut_signature(
            CallbackQuery.edit_message_caption,
            Bot.edit_message_caption,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.edit_message_caption,
            callback_query.bot,
            'edit_message_caption',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(callback_query.edit_message_caption, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'edit_message_caption', make_assertion)
        assert callback_query.edit_message_caption(caption='new caption')
        assert callback_query.edit_message_caption('new caption')

    def test_edit_message_reply_markup(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            reply_markup = kwargs['reply_markup'] == [['1', '2']]
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and reply_markup

        assert check_shortcut_signature(
            CallbackQuery.edit_message_reply_markup,
            Bot.edit_message_reply_markup,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.edit_message_reply_markup,
            callback_query.bot,
            'edit_message_reply_markup',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(
            callback_query.edit_message_reply_markup, callback_query.bot
        )

        monkeypatch.setattr(callback_query.bot, 'edit_message_reply_markup', make_assertion)
        assert callback_query.edit_message_reply_markup(reply_markup=[['1', '2']])
        assert callback_query.edit_message_reply_markup([['1', '2']])

    def test_edit_message_media(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            message_media = kwargs.get('media') == [['1', '2']]
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and message_media

        assert check_shortcut_signature(
            CallbackQuery.edit_message_media,
            Bot.edit_message_media,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.edit_message_media,
            callback_query.bot,
            'edit_message_media',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(callback_query.edit_message_media, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'edit_message_media', make_assertion)
        assert callback_query.edit_message_media(media=[['1', '2']])
        assert callback_query.edit_message_media([['1', '2']])

    def test_edit_message_live_location(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            latitude = kwargs.get('latitude') == 1
            longitude = kwargs.get('longitude') == 2
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and latitude and longitude

        assert check_shortcut_signature(
            CallbackQuery.edit_message_live_location,
            Bot.edit_message_live_location,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.edit_message_live_location,
            callback_query.bot,
            'edit_message_live_location',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(
            callback_query.edit_message_live_location, callback_query.bot
        )

        monkeypatch.setattr(callback_query.bot, 'edit_message_live_location', make_assertion)
        assert callback_query.edit_message_live_location(latitude=1, longitude=2)
        assert callback_query.edit_message_live_location(1, 2)

    def test_stop_message_live_location(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            return self.check_passed_ids(callback_query, kwargs)

        assert check_shortcut_signature(
            CallbackQuery.stop_message_live_location,
            Bot.stop_message_live_location,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.stop_message_live_location,
            callback_query.bot,
            'stop_message_live_location',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(
            callback_query.stop_message_live_location, callback_query.bot
        )

        monkeypatch.setattr(callback_query.bot, 'stop_message_live_location', make_assertion)
        assert callback_query.stop_message_live_location()

    def test_set_game_score(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            user_id = kwargs.get('user_id') == 1
            score = kwargs.get('score') == 2
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and user_id and score

        assert check_shortcut_signature(
            CallbackQuery.set_game_score,
            Bot.set_game_score,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.set_game_score,
            callback_query.bot,
            'set_game_score',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(callback_query.set_game_score, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'set_game_score', make_assertion)
        assert callback_query.set_game_score(user_id=1, score=2)
        assert callback_query.set_game_score(1, 2)

    def test_get_game_high_scores(self, monkeypatch, callback_query):
        def make_assertion(*_, **kwargs):
            user_id = kwargs.get('user_id') == 1
            ids = self.check_passed_ids(callback_query, kwargs)
            return ids and user_id

        assert check_shortcut_signature(
            CallbackQuery.get_game_high_scores,
            Bot.get_game_high_scores,
            ['inline_message_id', 'message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.get_game_high_scores,
            callback_query.bot,
            'get_game_high_scores',
            skip_params=self.skip_params(callback_query),
            shortcut_kwargs=self.shortcut_kwargs(callback_query),
        )
        assert check_defaults_handling(callback_query.get_game_high_scores, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'get_game_high_scores', make_assertion)
        assert callback_query.get_game_high_scores(user_id=1)
        assert callback_query.get_game_high_scores(1)

    def test_delete_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't delete inline messages")

        def make_assertion(*args, **kwargs):
            id_ = kwargs['chat_id'] == callback_query.message.chat_id
            message = kwargs['message_id'] == callback_query.message.message_id
            return id_ and message

        assert check_shortcut_signature(
            CallbackQuery.delete_message,
            Bot.delete_message,
            ['message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.delete_message, callback_query.bot, 'delete_message'
        )
        assert check_defaults_handling(callback_query.delete_message, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'delete_message', make_assertion)
        assert callback_query.delete_message()

    def test_pin_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't pin inline messages")

        def make_assertion(*args, **kwargs):
            return kwargs['chat_id'] == callback_query.message.chat_id

        assert check_shortcut_signature(
            CallbackQuery.pin_message,
            Bot.pin_chat_message,
            ['message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.pin_message, callback_query.bot, 'pin_chat_message'
        )
        assert check_defaults_handling(callback_query.pin_message, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'pin_chat_message', make_assertion)
        assert callback_query.pin_message()

    def test_unpin_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't unpin inline messages")

        def make_assertion(*args, **kwargs):
            return kwargs['chat_id'] == callback_query.message.chat_id

        assert check_shortcut_signature(
            CallbackQuery.unpin_message,
            Bot.unpin_chat_message,
            ['message_id', 'chat_id'],
            [],
        )
        assert check_shortcut_call(
            callback_query.unpin_message,
            callback_query.bot,
            'unpin_chat_message',
            shortcut_kwargs=['message_id', 'chat_id'],
        )
        assert check_defaults_handling(callback_query.unpin_message, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'unpin_chat_message', make_assertion)
        assert callback_query.unpin_message()

    def test_copy_message(self, monkeypatch, callback_query):
        if callback_query.inline_message_id:
            pytest.skip("Can't copy inline messages")

        def make_assertion(*args, **kwargs):
            id_ = kwargs['from_chat_id'] == callback_query.message.chat_id
            chat_id = kwargs['chat_id'] == 1
            message = kwargs['message_id'] == callback_query.message.message_id
            return id_ and message and chat_id

        assert check_shortcut_signature(
            CallbackQuery.copy_message,
            Bot.copy_message,
            ['message_id', 'from_chat_id'],
            [],
        )
        assert check_shortcut_call(callback_query.copy_message, callback_query.bot, 'copy_message')
        assert check_defaults_handling(callback_query.copy_message, callback_query.bot)

        monkeypatch.setattr(callback_query.bot, 'copy_message', make_assertion)
        assert callback_query.copy_message(1)

    def test_equality(self):
        a = CallbackQuery(self.id_, self.from_user, 'chat')
        b = CallbackQuery(self.id_, self.from_user, 'chat')
        c = CallbackQuery(self.id_, None, '')
        d = CallbackQuery('', None, 'chat')
        e = Audio(self.id_, 'unique_id', 1)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
