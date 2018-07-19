class PatchServerException(Exception):
    pass


class Unauthorized(PatchServerException):
    pass


class InvalidPatchDefinitionError(PatchServerException):
    pass


class SoftwareTitleNotFound(PatchServerException):
    pass


class InvalidWebhook(PatchServerException):
    pass


class PatchArchiveRestoreFailure(PatchServerException):
    pass
