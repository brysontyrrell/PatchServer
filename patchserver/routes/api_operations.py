import ast
import dateutil.parser
import hashlib
import json
import os
import tempfile
import shutil
import zipfile

from patchserver.database import db
from patchserver.models import (
    Criteria,
    ExtensionAttribute,
    Patch,
    PatchComponent,
    PatchCompontentCriteria,
    PatchCriteria,
    PatchKillApps,
    SoftwareTitle,
    SoftwareTitleCriteria
)
from patchserver.exc import (
    InvalidPatchDefinitionError,
    PatchArchiveRestoreFailure,
    SoftwareTitleNotFound
)
from patchserver.routes.validator import validate_json


def lookup_software_title(name_id):
    title = SoftwareTitle.query.filter_by(id_name=name_id).first()
    if not title:
        raise SoftwareTitleNotFound(name_id)
    else:
        return title


def get_last_index_value(model, model_attribute, filter_arg):
    result = model.query.with_entities(
        model.index).filter(
        getattr(model, model_attribute) == filter_arg).order_by(
        model.index.desc()).first()

    return result[0] if result else 0


def create_title(data):
    new_title = SoftwareTitle(
        id_name=data['id'],
        name=data['name'],
        publisher=data['publisher'],
        app_name=data['appName'],
        bundle_id=data['bundleId']
    )
    db.session.add(new_title)

    if data.get('requirements'):
        create_criteria_objects(
            data['requirements'], software_title=new_title)

    if data.get('patches'):
        create_patch_objects(
            list(reversed(data['patches'])), software_title=new_title)

    if data.get('extensionAttributes'):
        create_extension_attributes(
            data['extensionAttributes'], new_title)

    db.session.commit()
    return new_title


def create_criteria_objects(criteria_list, software_title=None,
                            patch_object=None, patch_component=None):
    """
    [
        <criteria_object_1>,
        <criteria_object_2>,
        <criteria_object_3>
    ]
    """
    def eval_bool(value):
        try:
            return ast.literal_eval(value)
        except ValueError:
            return bool(value)

    for criterion in criteria_list:
        criteria_hash = hashlib.sha1(
            criterion['name'] +
            criterion['operator'] +
            criterion['value'] +
            criterion['type'] +
            str(eval_bool(criterion.get('and', True)))
        ).hexdigest()

        criteria = Criteria.query.filter_by(hash=criteria_hash).first()
        if not criteria:
            criteria = Criteria(
                name=criterion['name'],
                operator=criterion['operator'],
                value=criterion['value'],
                type_=criterion['type'],
                and_=eval_bool(criterion.get('and', True))
            )

        if software_title:
            last_index = get_last_index_value(
                SoftwareTitleCriteria,
                'software_title',
                software_title)

            db.session.add(
                SoftwareTitleCriteria(
                    software_title=software_title,
                    criteria=criteria,
                    index=last_index + 1
                )
            )
        elif patch_object:
            last_index = get_last_index_value(
                PatchCriteria,
                'patch',
                patch_object)

            db.session.add(
                PatchCriteria(
                    patch=patch_object,
                    criteria=criteria,
                    index=last_index + 1
                )
            )
        elif patch_component:
            last_index = get_last_index_value(
                PatchCompontentCriteria,
                'patch_component',
                patch_component)

            db.session.add(
                PatchCompontentCriteria(
                    patch_component=patch_component,
                    criteria=criteria,
                    index=last_index + 1
                )
            )

        db.session.add(criteria)


def create_extension_attributes(ext_att_list, software_title):
    for ext_att in ext_att_list:
        db.session.add(
            ExtensionAttribute(
                key=ext_att['key'],
                value=ext_att['value'],
                display_name=ext_att['displayName'],
                software_title=software_title
            )
        )


def create_patch_objects(patch_list, software_title):
    """"""
    for patch in patch_list:
        new_patch = Patch(
            version=patch['version'],
            release_date=dateutil.parser.parse(patch['releaseDate']),
            standalone=patch['standalone'],
            minimum_operating_system=patch['minimumOperatingSystem'],
            reboot=patch['reboot'],
            software_title=software_title
        )
        db.session.add(new_patch)

        if patch.get('capabilities'):
            create_criteria_objects(
                patch['capabilities'], patch_object=new_patch)

        if patch.get('components'):
            create_patch_object_components(
                patch['components'], patch_object=new_patch)

        if patch.get('killApps'):
            create_patch_object_kill_apps(
                patch['killApps'], patch_object=new_patch)


def create_patch_object_components(component_list, patch_object):
    for component in component_list:
        new_component = PatchComponent(
            name=component['name'],
            version=component['version'],
            patch=patch_object
        )
        db.session.add(new_component)

        if component.get('criteria'):
            create_criteria_objects(
                component['criteria'], patch_component=new_component)


def create_patch_object_kill_apps(kill_apps_list, patch_object):
    for kill_app in kill_apps_list:
        new_kill_app = PatchKillApps(
            bundleId=kill_app['bundleId'],
            appName=kill_app['appName'],
            patch=patch_object
        )
        db.session.add(new_kill_app)


def create_backup_archive():
    titles = SoftwareTitle.query.all()
    tempdir = tempfile.mkdtemp(prefix='patch-dump-')

    for title in titles:
        filename = '{}.json'.format(title.id_name)
        with open(os.path.join(tempdir, filename), 'w') as f_obj:
            json.dump(title.serialize, f_obj)

    archive_list = os.listdir(tempdir)
    archive_path = tempfile.mkstemp(prefix='patch-archive-')[1]

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip:
        for filename in archive_list:
            zip.write(
                os.path.join(tempdir, filename),
                os.path.join('patch_archive', filename)
            )

    shutil.rmtree(tempdir)
    return archive_path


def restore_backup_archive(uploaded_archive):
    if os.path.splitext(uploaded_archive.filename)[-1] != '.zip':
        raise PatchArchiveRestoreFailure(
            'The submitted file is not a .zip archive')

    if len(SoftwareTitle.query.all()) != 0:
        raise PatchArchiveRestoreFailure(
            'Definitions already exist on this server')

    definitions_to_restore = list()

    with zipfile.ZipFile(uploaded_archive, 'r') as zip_file:
        for file_ in zip_file.namelist():
            data = json.loads(zip_file.read(file_))

            try:
                validate_json(data, 'patch')
            except InvalidPatchDefinitionError:
                raise PatchArchiveRestoreFailure(
                    'A definition in the archive failed validation')

            definitions_to_restore.append(data)

    saved_definitions = list()

    for definition in definitions_to_restore:
        saved_def = create_title(definition)
        saved_definitions.append(
            {
                "database_id": saved_def.id,
                "id": saved_def.id_name
            }
        )

    return saved_definitions
