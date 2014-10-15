import re

from fields import __base__
from fields import Callable
from fields import Factory


class ValidationError(Exception):
    pass


def regex_validation_sealer(required, defaults, everything, RegexType=type(re.compile(""))):
    """
    Example sealer that just does regex-based validation.
    """
    if required:
        raise TypeError("regex_validation_sealer doesn't support required arguments")

    klass = None
    kwarg_validators = dict(
        (key, val if isinstance(val, RegexType) else re.compile(val)) for key, val in defaults.items()
    )
    arg_validators = list(
        kwarg_validators[key] for key in everything
    )

    def __init__(self, *args, **kwargs):
        for pos, (value, validator) in enumerate(zip(args, arg_validators)):
            if not validator.match(value):
                raise ValidationError("Positional argument %s failed validation. %r doesn't match regex %r" % (
                    pos, value, validator.pattern
                ))
        for key, value in kwargs.items():
            if key in kwarg_validators:
                validator = kwarg_validators[key]
                if not validator.match(value):
                    raise ValidationError("Keyword argument %r failed validation. %r doesn't match regex %r" % (
                        key, value, validator.pattern
                    ))
        super(klass, self).__init__(*args, **kwargs)

    klass = type("RegexValidateBase", (__base__,), dict(
        __init__=__init__,
    ))
    return klass

RegexValidate = Factory(sealer=Callable(regex_validation_sealer))
