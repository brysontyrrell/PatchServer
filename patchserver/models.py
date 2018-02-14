from datetime import datetime
import hashlib
from operator import itemgetter
import uuid

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from .database import db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def datetime_to_iso(date):
    """Returns an ISO 8601 format
    2017-08-08T21:06:49Z

    :param datetime date: Datetime object
    """
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_token():
    """Created a 32 character token from a UUID"""
    return uuid.uuid4().hex


class ApiToken(db.Model):
    __tablename__ = 'api_token'

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.String(32), default=generate_token)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def sorted_criteria(criteria_list):
    sorted_list = sorted(criteria_list, key=itemgetter('index'))
    for item in sorted_list:
        del(item['index'])

    return sorted_list


class SoftwareTitle(db.Model):
    __tablename__ = 'software_titles'

    id = db.Column(db.Integer, primary_key=True)

    id_name = db.Column(db.String, unique=True)

    name = db.Column(db.String)
    publisher = db.Column(db.String)
    app_name = db.Column(db.String)
    bundle_id = db.Column(db.String)

    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requirements = db.relationship(
        "SoftwareTitleCriteria",
        back_populates="software_title",
        cascade='all, delete, delete-orphan')

    patches = db.relationship(
        "Patch",
        back_populates="software_title",
        order_by='desc(Patch.id)',
        cascade='all, delete')

    extension_attributes = db.relationship(
        "ExtensionAttribute",
        back_populates="software_title",
        cascade='all, delete')

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
        requirements = [
                criteria.serialize for criteria in self.requirements
            ]
        return {
            'name': self.name,
            'publisher': self.publisher,
            'appName': self.app_name,
            'bundleId': self.bundle_id,
            'lastModified': datetime_to_iso(self.last_modified),
            'currentVersion': self.current_version,
            'requirements': sorted_criteria(requirements),
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
        cascade='all, delete')

    components = db.relationship(
        "PatchComponent",
        back_populates="patch",
        cascade='all, delete')

    capabilities = db.relationship(
        "PatchCriteria",
        back_populates="patch",
        cascade='all, delete, delete-orphan')

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
            ]
            # 'dependencies': []
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

    criteria = db.relationship(
        "PatchCompontentCriteria",
        back_populates="patch_component",
        cascade='all, delete, delete-orphan')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'version': self.version,
            'criteria': [
                criteria.serialize for criteria in self.criteria
            ]
        }


class Criteria(db.Model):
    __tablename__ = 'criteria'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    operator = db.Column(db.String)
    value = db.Column(db.String)
    type_ = db.Column(db.String)
    and_ = db.Column(db.Boolean, default=True)

    hash = db.Column(db.String, unique=True)

    software_title = db.relationship(
        'SoftwareTitleCriteria', back_populates='criteria')

    patch = db.relationship('PatchCriteria', back_populates='criteria')

    patch_component = db.relationship(
        'PatchCompontentCriteria', back_populates='criteria')

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
    def orphaned(self):
        if (
            len(self.software_title) +
            len(self.patch) +
            len(self.patch_component)
        ) == 0:
            return True
        else:
            return False

    @property
    def serialize(self):
        return {
            'name': self.name,
            'operator': self.operator,
            'value': self.value,
            'type': self.type_,
            'and': self.and_
        }


class SoftwareTitleCriteria(db.Model):
    """Association table for linking sets of criteria to a software title."""
    __tablename__ = 'software_title_criteria'

    title_id = db.Column(
        db.Integer, db.ForeignKey('software_titles.id'), primary_key=True)
    criteria_id = db.Column(
        db.Integer, db.ForeignKey('criteria.id'), primary_key=True)

    index = db.Column(db.Integer)

    software_title = db.relationship(
        'SoftwareTitle', back_populates='requirements')

    criteria = db.relationship(
        'Criteria', back_populates='software_title')

    @property
    def serialize(self):
        data = self.criteria.serialize
        data['index'] = self.index
        return data


class PatchCriteria(db.Model):
    """Association table for linking sets of criteria to a patch."""
    __tablename__ = 'patch_criteria'

    patch_id = db.Column(
        db.Integer, db.ForeignKey('patches.id'), primary_key=True)
    criteria_id = db.Column(
        db.Integer, db.ForeignKey('criteria.id'), primary_key=True)

    index = db.Column(db.Integer)

    patch = db.relationship(
        'Patch', back_populates='capabilities')

    criteria = db.relationship(
        'Criteria', back_populates='patch')

    @property
    def serialize(self):
        return self.criteria.serialize


class PatchCompontentCriteria(db.Model):
    """Association table for linking sets of criteria to a patch."""
    __tablename__ = 'patch_component_criteria'

    component_id = db.Column(
        db.Integer, db.ForeignKey('patch_components.id'), primary_key=True)
    criteria_id = db.Column(
        db.Integer, db.ForeignKey('criteria.id'), primary_key=True)

    index = db.Column(db.Integer)

    patch_component = db.relationship(
        'PatchComponent', back_populates='criteria')

    criteria = db.relationship(
        'Criteria', back_populates='patch_component')

    @property
    def serialize(self):
        return self.criteria.serialize


@event.listens_for(SoftwareTitle.requirements, 'append')
@event.listens_for(SoftwareTitle.requirements, 'remove')
@event.listens_for(SoftwareTitle.patches, 'append')
@event.listens_for(SoftwareTitle.patches, 'remove')
@event.listens_for(SoftwareTitle.requirements, 'append')
@event.listens_for(SoftwareTitle.requirements, 'remove')
def software_title_child_update(target, value, initiator):
    target.last_modified = datetime.utcnow()


@event.listens_for(Session, 'after_flush')
def delete_ophaned_criteria(session, ctx):
    check = False

    for instance in session.deleted:
        if isinstance(instance, (SoftwareTitle, Patch, PatchComponent)):
            check = True

    if check:
        session.query(Criteria).filter(
            ~Criteria.software_title.any(),
            ~Criteria.patch.any(),
            ~Criteria.patch_component.any()).delete(synchronize_session=False)
