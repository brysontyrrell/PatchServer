class PatchServerException(Exception):
    pass


class InvalidPatchDefinitionError(PatchServerException):
    pass


class SoftwareTitleNotFound(PatchServerException):
    pass
