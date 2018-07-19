import json
import os

from jsonschema import validate, ValidationError

from patchserver.exc import InvalidPatchDefinitionError

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, 'schema_full_definition.json'), 'r') as f_obj:
    patch_schema = json.load(f_obj)

with open(os.path.join(dir_path, 'schema_version.json'), 'r') as f_obj:
    version_schema = json.load(f_obj)


def validate_json(data, schema=None):
    """Takes a dictionary object and validates it against a JSON schema.

    :param dict data: The JSON to validate as a dictionary object.
    :param str schema: Which schema to validate against. Valid options are:
        patch or version.

    :raises: InvalidPatchDefinitionError
    """
    if schema not in ('patch', 'version'):
        raise ValueError("Argument 'schema' must be 'patch' or 'version'")

    if schema == 'patch':
        use_schema = patch_schema
    else:
        use_schema = version_schema

    try:
        validate(data, use_schema)
    except ValidationError as error:
        message = "Validation error encountered with submitted JSON: {} for " \
                  "item: /{}".format(
                      str(error.message),
                      '/'.join([str(i) for i in error.path]))
        raise InvalidPatchDefinitionError(message)
