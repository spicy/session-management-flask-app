from flask import Blueprint, redirect, render_template, session, url_for

from utils.cookie_handler import get_cookie

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/")
def home_page():
    """Render the home page if user is logged in, otherwise redirect to login."""
    username = get_cookie("username")
    if username:
        return render_template("home.html", username=username)
    return redirect(url_for("auth.login_page"))


@user_blueprint.route("/profile")
def user_profile():
    """Render the user profile page, tracking visit count."""
    username = get_cookie("username")
    if not username:
        return redirect(url_for("auth.login_page"))

    visit_count = session.get("visit_count", 0) + 1
    session["visit_count"] = visit_count
    return render_template("profile.html", username=username, visits=visit_count)
