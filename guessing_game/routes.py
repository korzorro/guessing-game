from flask import request, url_for, g
from functools import wraps
from guessing_game import app, messages, db
from .models import Token, Guess


def is_int(n):
    try:
        n = int(n)
        return True
    except ValueError:
        return False

def token_auth(fn):
    @wraps(fn)
    def _token_auth(*args, **kwargs):
        token_string = request.args.get('token')
        if token_string:
            token = Token.query.get(token_string)
            if token:
                g.token = token
                return fn(*args, **kwargs)
        return messages.invalid_token_format.format(url=url_for('generate_token'))
    return _token_auth

def get_winners(answer, guesses):
    if len(guesses) == 0:
        return list()
    winners = [guesses[0]]
    winning_guess = winners[0].guess
    for guess in guesses[1:]:
        guess_diff = abs(guess.guess - answer)
        winning_diff = abs(winning_guess - answer)
        if guess_diff < winning_diff:
            winners = [guess]
            winning_guess = guess.guess
        elif guess_diff == winning_diff:
            winners.append(guess)
    return winners

@app.route('/')
def index():
    return messages.guess_tutorial

@app.route('/token/generate')
def generate_token():
    token_string = Token.generate()

    while Token.query.get(token_string):
        token_string = Token.generate()

    token = Token(token=token_string)
    token.add_to_db()

    return messages.token_generated_format.format(token=token.token)

@app.route('/guess')
@token_auth
def guess():
    guess = request.args.get('guess')
    user = request.args.get('user')
    
    if not guess or not user or not is_int(guess):
        return messages.guess_tutorial
    
    if not g.token.guessing_enabled or \
       g.token.guesses.filter_by(user=user).count() >= 1:
        return ''

    guess = Guess(token=g.token.token, guess=int(guess), user=user)
    guess.add_to_db()
    
    return messages.guess_confirm_format.format(user=user, guess=guess.guess)

@app.route('/new')
@token_auth
def new_game():
    g.token.guesses.delete()
    g.token.enable_guessing()
    return messages.new_game

@app.route('/disable-guessing')
@token_auth
def disable_guessing():
    g.token.disable_guessing()
    return messages.guessing_disabled

@app.route('/enable-guessing')
@token_auth
def enable_guessing():
    g.token.enable_guessing()
    return messages.guessing_enabled

@app.route('/results')
@token_auth
def results():
    answer = request.args.get('answer')

    if not answer or not is_int(answer):
        return messages.results_tutorial
    
    winners = get_winners(int(answer), g.token.guesses.all())
    
    if len(winners) == 0:
        return messages.no_win

    winning_guess = winners[0].guess
    
    if len(winners) == 1:
        return messages.win_format.format(
            user=winners[0].user, guess=winning_guess)

    if len(winners) == 2:
        winner_list_str = winners[0].user + ' and ' + winners[1].user
        return messages.tie_format.format(
            count=2, guess=winning_guess, winner_list_str=winner_list_str)

    winner_list_str = str()
    for winner in winners[:-1]:
        winner_list_str += winner.user + ', '
    winner_list_str += 'and ' + winners[-1].user
        
    return messages.tie_format.format(
        count=len(winners),
        guess=winning_guess,
        winner_list_str=winner_list_str
    )
