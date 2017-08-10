from datetime import datetime
import hashlib

from sqlalchemy import event

from . import db


def datetime_to_iso(date):
    """Returns an ISO 8601 format
    2017-08-08T21:06:49Z

    :param datetime date: Datetime object
    """
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


class SoftwareTitle(db.Model):
    __tablename__ = 'software_titles'

    id = db.Column(db.Integer, primary_key=True)

    id_name = db.Column(db.String, unique=True)

    name = db.Column(db.String)
    publisher = db.Column(db.String)
    app_name = db.Column(db.String)
    bundle_id = db.Column(db.String)

    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    requirements = db.relationship(
        "SoftwareTitleCriteria",
        back_populates="software_title",
        cascade='delete')

    patches = db.relationship(
        "Patch",
        back_populates="software_title",
        order_by='desc(Patch.id)',
        cascade='delete')

    extension_attributes = db.relationship(
        "ExtensionAttribute",
        back_populates="software_title",
        cascade='delete')

    @property
    def current_version(self):
        if not self.patches:
            return None
        else:
            return self.patches[0].version

    @property
    def serialize_short(self):
        return {
            'name': self.name,
            'publisher': self.publisher,
            'lastModified': datetime_to_iso(self.last_modified),
            'currentVersion': self.current_version,
            'id': self.id_name
        }

    @property
    def serialize(self):
        return {
            'name': self.name,
            'publisher': self.publisher,
            'appName': self.app_name,
            'bundleId': self.bundle_id,
            'lastModified': datetime_to_iso(self.last_modified),
            'currentVersion': self.current_version,
            'requirements': [
                criteria.serialize for criteria in self.requirements
            ],
            'patches': [patch.serialize for patch in self.patches],
            'extensionAttributes': [
                ext_att.serialize for ext_att in self.extension_attributes
            ],
            'id': self.id_name
        }


class ExtensionAttribute(db.Model):
    __tablename__ = 'extension_attributes'

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String)
    value = db.Column(db.Text)
    display_name = db.Column(db.String)

    software_title_id = db.Column(
        db.Integer, db.ForeignKey('software_titles.id'))

    software_title = db.relationship(
        'SoftwareTitle', back_populates='extension_attributes')

    @property
    def serialize(self):
        return {
            'key': self.key,
            'value': self.value,
            'displayName': self.display_name
        }


class Patch(db.Model):
    __tablename__ = 'patches'

    id = db.Column(db.Integer, primary_key=True)

    version = db.Column(db.String)
    standalone = db.Column(db.Boolean, default=True)
    minimum_operating_system = db.Column(db.String)
    reboot = db.Column(db.Boolean, default=False)

    release_date = db.Column(db.DateTime)

    software_title_id = db.Column(
        db.Integer, db.ForeignKey('software_titles.id'))

    software_title = db.relationship(
        'SoftwareTitle', back_populates='patches')

    kill_apps = db.relationship(
        "PatchKillApps",
        back_populates="patch",
        cascade='delete')

    components = db.relationship(
        "PatchComponent",
        back_populates="patch",
        cascade='delete')

    capabilities = db.relationship(
        "Criteria",
        back_populates="patch",
        cascade='delete')

    dependencies = None  # Not used

    @property
    def serialize(self):
        return {
            'version': self.version,
            'releaseDate': datetime_to_iso(self.release_date),
            'standalone': self.standalone,
            'minimumOperatingSystem': self.minimum_operating_system,
            'reboot': self.reboot,
            'killApps': [
                killApp.serialize for killApp in self.kill_apps
            ],
            'components': [
                component.serialize for component in self.components
            ],
            'capabilities': [
                criteria.serialize for criteria in self.capabilities
            ],
            'dependencies': []
        }


class SoftwareTitleCriteria(db.Model):
    """Association table for linking sets of criteria to a software title."""
    __tablename__ = 'software_title_criteria'

    title_id = db.Column(
        db.Integer, db.ForeignKey('software_titles.id'), primary_key=True)
    criteria_id = db.Column(
        db.Integer, db.ForeignKey('criteria.id'), primary_key=True)

    software_title = db.relationship(
        'SoftwareTitle', back_populates='requirements')

    criteria = db.relationship(
        'Criteria', back_populates='software_title')

    @property
    def serialize(self):
        return self.criteria.serialize


class Criteria(db.Model):
    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    operator = db.Column(db.String)
    value = db.Column(db.String)
    type_ = db.Column(db.String)
    and_ = db.Column(db.Boolean, default=True)

    hash = db.Column(db.String, unique=True)

    patch_id = db.Column(db.Integer, db.ForeignKey('patches.id'))

    patch_component_id = db.Column(
        db.Integer, db.ForeignKey('patch_components.id'))

    software_title = db.relationship(
        'SoftwareTitleCriteria', back_populates='criteria')

    patch = db.relationship('Patch', back_populates='capabilities')

    patch_component = db.relationship(
        'PatchComponent', back_populates='criteria')

    def __init__(self, **kwargs):
        super(Criteria, self).__init__(**kwargs)

        self.hash = hashlib.sha1(
            self.name +
            self.operator +
            self.value +
            self.type_ +
            str(self.and_)
        ).hexdigest()

    @property
    def serialize(self):
        return {
            'name': self.name,
            'operator': self.operator,
            'value': self.value,
            'type': self.type_,
            'and': self.and_
        }


class PatchKillApps(db.Model):
    __tablename__ = 'patch_kill_apps'

    id = db.Column(db.Integer, primary_key=True)

    bundleId = db.Column(db.String)
    appName = db.Column(db.String)

    patch_id = db.Column(db.Integer, db.ForeignKey('patches.id'))

    patch = db.relationship('Patch', back_populates='kill_apps')

    @property
    def serialize(self):
        return {
            'bundleId': self.bundleId,
            'appName': self.appName
        }


class PatchComponent(db.Model):
    __tablename__ = 'patch_components'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    version = db.Column(db.String)

    patch_id = db.Column(db.Integer, db.ForeignKey('patches.id'))
    patch = db.relationship('Patch', back_populates='components')

    criteria = db.relationship("Criteria", back_populates="patch_component")

    @property
    def serialize(self):
        return {
            'name': self.name,
            'version': self.version,
            'criteria': [
                criteria.serialize for criteria in self.criteria
            ]
        }


@event.listens_for(SoftwareTitle.requirements, 'append')
@event.listens_for(SoftwareTitle.requirements, 'remove')
@event.listens_for(SoftwareTitle.patches, 'append')
@event.listens_for(SoftwareTitle.patches, 'remove')
def software_title_child_update(target, value, initiator):
    target.last_modified = datetime.utcnow()
