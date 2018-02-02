import ast
import dateutil.parser
import hashlib

from ..database import db
from ..models import (
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
from ..exc import SoftwareTitleNotFound


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
