class LookupAlreadyRegistered(Exception):
    "Exception when trying to register a lookup which is already registered."


class LookupNotRegistered(Exception):
    "Exception when trying use a lookup which is not registered."


class LookupInvalid(Exception):
    "Exception when register an invalid lookup class."
