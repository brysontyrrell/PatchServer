from flask import blueprints, render_template, request, url_for

blueprint = blueprints.Blueprint("web_ui", __name__)


@blueprint.route("/")
def index():
    return render_template("index.html"), 200
