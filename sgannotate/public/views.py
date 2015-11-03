# -*- coding: utf-8 -*-
"""Public section, including homepage and login."""
from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, current_app, make_response)
from flask.ext.login import login_user, login_required, logout_user

from sgannotate.extensions import login_manager, db
from sgannotate.user.models import User

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route('/', methods=["GET", "POST"])
def home():
    return render_template("public/home.html")


@blueprint.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """

    authomatic = Authomatic(
        current_app.config['AUTHOMATIC'],
        current_app.config['SECRET_KEY'],
        report_errors=False)

    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            if not (result.user.first_name and result.user.last_name and result.user.id and result.user.email):
                # We need to update the user to get more info.
                result.user.update()
            if not result.user.email.endswith("@thenewmotion.com"):
                return current_app.login_manager.unauthorized()
            user = User.query.filter_by(email=result.user.email).first()
            if not user:
                user = User(result.user.email,
                            first_name=result.user.first_name,
                            last_name=result.user.last_name,
                            active=True)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            flash("Logged in successfully.", category="success")
            # The rest happens inside the template.
            return redirect(request.args.get('next') or url_for('public.home'))

    # Don't forget to return the response.
    return response


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")
