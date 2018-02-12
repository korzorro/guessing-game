from unittest import TestCase
from flask import url_for
from flask_fixtures import FixturesMixin, log
from guessing_game import app, db, messages
from guessing_game.models import Token, Guess
from guessing_game.routes import token_auth


log.propagate = False
app.config.from_object('config.TestConfig')


class GuessingGameTestCase(TestCase, FixturesMixin):

    fixtures = ['guessing_game.yaml']
    app = app
    db = db

    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @app.route('/test-auth-route')
    @token_auth
    def test_auth_route():
        return ''

    def test_index(self):
        resp = self.client.get(url_for('index'))
        assert resp.get_data(as_text=True) == messages.guess_tutorial

    def test_route_with_missing_or_invalid_token(self):
        resp = self.client.get(url_for('test_auth_route'))
        message = resp.get_data(as_text=True)
        target_message = messages.invalid_token_format.format(
            url=url_for('generate_token'))
        assert message == target_message
        resp = self.client.get(
            url_for('test_auth_route'), query_string={'token': 'invalid'})
        message = resp.get_data(as_text=True)
        assert message == target_message

    def test_route_with_valid_token(self):
        resp = self.client.get(
            url_for('test_auth_route'), query_string={'token': '123abc'})
        message = resp.get_data(as_text=True)
        assert message == ''

    def test_generate_token(self):
        def get_token_from_message(message):
            start_str = 'Your token is '
            start = message.find(start_str) + len(start_str)
            end = message.find('\n', start)
            token_string = message[start:end]
            return token_string

        resp = self.client.get(url_for('generate_token'))
        message = resp.get_data(as_text=True)
        token = get_token_from_message(message)
        assert Token.query.get(token)

    def test_guess_success(self):
        guess_data = {
            'guess': 3,
            'user': 'uniqueuser',
            'token': '123abc'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == messages.guess_confirm_format.format(
            user=guess_data['user'], guess=guess_data['guess'])
        assert Guess.query.filter_by(
            user=guess_data['user'], token=guess_data['token']).count() == 1

    def test_duplicate_guess_not_saved(self):
        guess_data = {
            'guess': 1,
            'user': 'a',
            'token': '123abc'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == ' '
        assert Guess.query.filter_by(
            user=guess_data['user'], token=guess_data['token']).count() == 1

    def test_guess_while_guessing_disabled(self):
        guess_data = {
            'guess': 1,
            'user': 'uniqueuser',
            'token': '345cde'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == ' '
        assert Guess.query.filter_by(
            user=guess_data['user'], token=guess_data['token']).count() == 0

    def test_guess_with_missing_user(self):
        guess_data = {
            'guess': 1,
            'token': '123abc'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == messages.guess_tutorial
        assert Guess.query.filter_by(
            token=guess_data['token'], user=None).count() == 0

    def test_guess_with_missing_guess(self):
        guess_data = {
            'user': 'uniqueuser',
            'token': '123abc'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == messages.guess_tutorial
        assert Guess.query.filter_by(
            token=guess_data['token'], user='uniqueuser').count() == 0

    def test_guess_with_noninteger_guess(self):
        guess_data = {
            'guess': 'a',
            'user': 'uniqueuser',
            'token': '123abc'
        }

        resp = self.client.get(url_for('guess'), query_string=guess_data)
        message = resp.get_data(as_text=True)
        assert message == messages.guess_tutorial
        assert Guess.query.filter_by(
            token=guess_data['token'], user='uniqueuser').count() == 0

    def test_new_game(self):
        data = {'token': '345cde'}
        token = Token.query.get(data['token'])
        assert Guess.query.filter_by(token=data['token']).count() >= 1
        assert not token.guessing_enabled
        resp = self.client.get(url_for('new_game'), query_string=data)
        message = resp.get_data(as_text=True)
        token = Token.query.get(data['token'])
        assert message == messages.new_game
        assert Guess.query.filter_by(token=data['token']).count() == 0
        assert Guess.query.count() >= 1
        assert token.guessing_enabled

    def test_disable_guessing(self):
        data = {'token': '123abc'}
        assert Token.query.get(data['token']).guessing_enabled
        resp = self.client.get(
            url_for('disable_guessing'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.guessing_disabled
        assert not Token.query.get(data['token']).guessing_enabled

    def test_enable_guessing(self):
        data = {'token': '345cde'}
        assert not Token.query.get(data['token']).guessing_enabled
        resp = self.client.get(
            url_for('enable_guessing'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.guessing_enabled
        assert Token.query.get(data['token']).guessing_enabled

    def test_results_with_no_answer(self):
        data = {'token': '456def'}
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.results_tutorial

    def test_results_with_non_integer_answer(self):
        data = {
            'token': '456def',
            'answer': 'a'
        }
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.results_tutorial

    def test_results_with_no_guesses(self):
        data = {
            'token': '456def',
            'answer': 1
        }
        assert Guess.query.filter_by(token=data['token']).count() == 0
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.no_win

    def test_results_with_one_guess(self):
        data = {
            'token': '345cde',
            'answer': 1
        }
        base_query = Guess.query.filter_by(token=data['token'])
        assert base_query.count() == 1
        guess = base_query.filter_by(guess=data['answer']).first()
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.win_format.format(
            user=guess.user, guess=guess.guess)

    def test_results_with_multiple_guesses(self):
        data = {
            'token': '123abc',
            'answer': 1
        }
        base_query = Guess.query.filter_by(token=data['token'])
        assert base_query.count() > 1
        guess = base_query.filter_by(guess=data['answer']).first()
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert message == messages.win_format.format(
            user=guess.user, guess=guess.guess)

    def test_results_with_two_way_tie(self):
        data = {
            'token': '123abc',
            'answer': 4
        }
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert '2 way tie' in message

    def test_results_with_three_way_tie(self):
        data = {
            'token': '123abc',
            'answer': 3
        }
        resp = self.client.get(url_for('results'), query_string=data)
        message = resp.get_data(as_text=True)
        assert '3 way tie' in message
