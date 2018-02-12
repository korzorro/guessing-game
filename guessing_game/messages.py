# Static Messages
guess_tutorial = (
    'To make a guess, type !guess <number>. You can only make one guess per '
    'round.'
)
results_tutorial = (
    'To show the results, type !results <number>. The person with the closest '
    'guess wins. If there is a tie, each person that is tied will win.'
)
new_game = 'A new round has started! ' + guess_tutorial
guessing_disabled = 'Guessing for this game is now disabled.'
guessing_enabled = 'Guessing for this game is now enabled.'
no_win = 'There are no winners because there aren\'t any guesses'


# Message Formats
win_format = '{user} won with a guess of {guess}'
tie_format = (
    'We have a {count} way tie with a guess of {guess}! The winners are '
    '{winner_list_str}.'
)
token_generated_format = (
    '<pre>Your token is {token}\nPlace this token in the url. '
    'Nightbot example below...\n\n'
    '!guess $(urlfetch http://{base_url}{guess_route}?token={token}'
    'user=$(user)&guess=$(1))\n\n'
    '!newgame $(urlfetch http://{base_url}{new_route}?token={token})\n\n'
    '!disableguessing $(urlfetch http://{base_url}{disable_guessing_route}?'
    'token={token})\n\n'
    '!enableguessing $(urlfetch http://{base_url}{enable_guessing_route}?'
    'token={token})\n\n'
    '!results $(urlfetch http://{base_url}{results_route}?token={token}&'
    'answer=$(1))\n<pre>'
)
invalid_token_format = (
    'Your token is missing or invalid. Obtain a valid token at {url}'
)
guess_confirm_format = '{user}, your guess of {guess} has been submitted.'
