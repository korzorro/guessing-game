from guessing_game import db
from secrets import token_urlsafe


class ModelMixin():

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()


class Token(db.Model, ModelMixin):

    token = db.Column(db.String, primary_key=True)
    guessing_enabled = db.Column(db.Boolean, default=True)
    guesses = db.relationship('Guess', lazy='dynamic')

    def generate():
        return token_urlsafe(16)

    def enable_guessing(self):
        self.guessing_enabled = True
        db.session.commit()

    def disable_guessing(self):
        self.guessing_enabled = False
        db.session.commit()


class Guess(db.Model, ModelMixin):

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(16), db.ForeignKey('token.token'), nullable=False)
    guess = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(26), nullable=False)
