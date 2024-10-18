from flask import current_app
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

csrf = CSRFProtect()


def create_login_form():
    class LoginForm(FlaskForm):
        username = StringField(
            "Username",
            validators=[
                DataRequired(),
                Regexp(
                    current_app.config["USERNAME_REGEX"],
                    message="Username must be in the format Firstname_Lastname (e.g., John_Doe)",
                ),
            ],
        )
        submit = SubmitField("Login")

    return LoginForm()
