from flask import Blueprint
from flask import current_app as app
from flask import make_response, redirect, render_template, session, url_for

from forms.login_form import create_login_form
from utils.cookie_handler import delete_cookie, get_cookie, set_cookie

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    """Handle user login."""
    username = get_cookie("username")
    if username:
        return redirect(url_for("user.user_profile"))

    form = create_login_form()
    if form.validate_on_submit():
        username = form.username.data
        app.logger.info(f"User {username} logged in successfully")
        response = make_response(redirect(url_for("user.user_profile")))
        set_cookie(response, "username", username)
        session["visit_count"] = 0  # Initialize visit count
        return response
    return render_template(
        "login.html", form=form, username_regex=app.config["USERNAME_REGEX"]
    )


@auth_blueprint.route("/logout")
def logout_user():
    """Handle user logout."""
    app.logger.info("User logged out")
    response = make_response(redirect(url_for("auth.login_page")))
    delete_cookie(response, "username")
    session.clear()  # Clear the session
    return response
