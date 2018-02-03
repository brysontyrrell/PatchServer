from flask import blueprints, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from .. import __version__
from ..models import SoftwareTitle

blueprint = blueprints.Blueprint('web_ui', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html'), 200


@blueprint.route('/rss')
def rss_feed():
    feed = AtomFeed(
        'Patch Server Software Titles',
        feed_url=request.url,
        url=request.url_root,
        generator=('Patch Server', None, __version__))

    titles = SoftwareTitle.query.all()

    for title in titles:
        feed.add(
            title=title.name,
            author=title.publisher,
            content='<b>Version:</b> {} '
                    '<b>| App Name:</b> {} '
                    '<b>| Bundle ID:</b> {}'.format(
                        title.current_version, title.app_name, title.bundle_id),
            url=url_for(
                'patch_by_name_id', name_id=title.id_name, _external=True),
            updated=title.last_modified)

    return feed.get_response()
